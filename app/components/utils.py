import hashlib
import uuid
from db_setup import get_db_connection
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import re


def hash_password(password):
    """Hashes a password for secure storage."""
    salt = uuid.uuid4().hex
    hashed = hashlib.sha256((password + salt).encode()).hexdigest()
    return f"{hashed}${salt}"


def verify_password(password, hashed):
    """Verifies a password against a stored hash."""
    try:
        hash_part, salt = hashed.split('$')
        return hashlib.sha256((password + salt).encode()).hexdigest() == hash_part
    except ValueError:
        return False
    
def update_user_password(user_id, new_password):
    """Update a user's password in the database."""
    if len(new_password) < 8:
        raise ValueError("Password must be at least 8 characters long.")
    
    # Hash the new password
    new_password_hash = hash_password(new_password)
    conn = get_db_connection()
    cursor = conn.cursor()
    # Update the password in the database
    cursor.execute(
        """
        UPDATE users
        SET password_hash = ?
        WHERE id = ?
        """,
        (new_password_hash, user_id)
    )
    conn.commit()
    conn.close()
    print(f"Password updated successfully for user_id {user_id}.")
    return new_password_hash


def authenticate_user(email, password):
    """Authenticates a user by email and password."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Retrieve the user record and their roles by email
    query = """
    SELECT u.id, u.username, u.email, u.password_hash, r.role
    FROM users u
    LEFT JOIN user_roles ur ON u.id = ur.user_id
    LEFT JOIN roles r ON ur.role_id = r.id
    WHERE u.email = ?
    """
    cursor.execute(query, (email,))
    rows = cursor.fetchall()
    conn.close()

    # If no user is found, return None
    if not rows:
        return None

    # Extract the user's data (assumes user data is consistent across rows)
    user_data = {
        "id": rows[0]["id"],
        "username": rows[0]["username"],
        "email": rows[0]["email"],
        "password_hash": rows[0]["password_hash"],
        "roles": [row["role"] for row in rows if row["role"]]  # Collect all roles
    }

    # Verify the password
    if verify_password(password, user_data["password_hash"]):
        # Remove the password_hash before returning user data for security reasons
        user_data.pop("password_hash")
        return user_data
    else:
        return None


def add_user(username, email, password, role):
    """Adds a new user to the SQLite database."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if email already exists
    cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
    if cursor.fetchone():
        conn.close()
        return None  # Email already exists

    # Hash the password
    password_hash = hash_password(password)

    # Insert new user into the database
    cursor.execute("""
    INSERT INTO users (username, email, password_hash, role)
    VALUES (?, ?, ?, ?)
    """, (username, email, password_hash, role))

    # Commit the transaction and retrieve the new user ID
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()

    return user_id  # Return the new user's ID

def delete_user_account(user_id):
    """Delete a user's account from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    # Delete the user account
    cursor.execute(
        """
        DELETE FROM users
        WHERE id = ?
        """,
        (user_id,)
    )
    conn.commit()
    conn.close()
    print(f"User account with user_id {user_id} deleted successfully.")
    

# Function to scrape property data
def scrape_data_to_dict(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    browser = webdriver.Chrome(options=chrome_options)

    data_dict = {}
    try:
        browser.get(url)
        soup = BeautifulSoup(browser.page_source, 'html.parser')

        # Extract type, size, and location
        for s in soup.find_all("div", {"class": "title"}):
            p = s.find("h1")
            if p:
                title_text = p.text.strip()
                type_match = re.match(r"^(.*?)(\d)", title_text)
                if type_match:
                    property_type = type_match.group(1).strip()
                size_match = re.search(r"\d+", title_text)
                if size_match:
                    property_size = size_match.group()
            l = s.find("h3")
            if l:
                property_location = l.text.strip()

        price_div = soup.find("div", {"class": "price"})
        if price_div:
            price_text = price_div.text
            property_price = price_text.replace("€", "").replace(",", "").replace(" ", "").replace(".", "").strip()

        spm_div = soup.find("div", {"class": "price-square-meter"})
        if spm_div:
            spm_text = spm_div.text
            price_per_sqm = spm_text.replace("€", "").replace("/", "").replace("sq.m.", "").replace(".", "").strip()

        data_dict.update({
            'property_type': property_type,
            'property_size': property_size,
            'property_location': property_location,
            'property_price': property_price,
            'price_per_sqm': price_per_sqm,
        })

        characteristics = {}
        for li in soup.find_all('li', class_='cell large-6', attrs={'data-testid': 'characteristic'}):
            text = li.get_text(strip=True).split(':', 1)
            if len(text) == 2:
                characteristics[text[0].strip()] = text[1].strip()
            else:
                characteristics[text[0].strip()] = ""
        data_dict['characteristics'] = characteristics

        statistics = {}
        stats_section = soup.find('section', {'data-testid': 'statistics'})
        if stats_section:
            for p in stats_section.find_all('p'):
                if ':' in p.text:
                    label, _, value = p.text.partition(':')
                    statistics[label.strip()] = value.strip()
        data_dict['statistics'] = statistics

        try:
            button = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH, '//button[@data-testid="image-count-icon"]'))
            )
            browser.execute_script("arguments[0].click();", button)
            WebDriverWait(browser, 10).until(lambda driver: len(driver.find_elements(By.TAG_NAME, 'img')) > 0)
            soup = BeautifulSoup(browser.page_source, 'html.parser')
        except Exception as e:
            print(f"Error clicking button or loading images: {e}")

        # Extract images with alt text containing the title text (case-insensitive) and unique src URLs
        unique_images = set()
        images = []
        for img in soup.find_all("img", alt=True):
            src = img.get("src")
            alt = img.get("alt")
            
            if alt and title_text.lower() in alt.lower():
                
                if src not in unique_images:
                    unique_images.add(src)
                    images.append({"src": src, "alt": alt})
        data_dict['images'] = images

        return data_dict
    finally:
        browser.quit()



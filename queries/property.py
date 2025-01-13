from db_setup import get_db_connection
from app.components.utils import hash_password  # Assuming you have the hash_password function in utils.py
import sqlite3
import streamlit as st
import json

# Save property data to the database

def save_property_to_db(property_data, user_id):
    """
    Save property data to the database.
    :param property_data: Dictionary containing property details.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Insert the property
        cursor.execute("""
        INSERT INTO properties (
            friendly_name, property_type, property_size, property_location, property_price,
            price_per_sqm, bedrooms, bathrooms, floor, year_built, condition,
            renovation_year, energy_class, availability, available_from,
            heating_method, zone, creation_method, user_id, interest_count
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
        )
        """, (
            property_data.get("friendly_name"),
            property_data.get("property_type"),
            property_data.get("property_size"),
            property_data.get("property_location"),
            property_data.get("property_price"),
            property_data.get("price_per_sqm"),
            property_data.get("bedrooms"),
            property_data.get("bathrooms"),
            property_data.get("floor"),
            property_data.get("year_built"),
            property_data.get("condition"),
            property_data.get("renovation_year"),
            property_data.get("energy_class"),
            property_data.get("availability"),
            property_data.get("available_from"),
            property_data.get("heating_method"),
            property_data.get("zone"),
            property_data.get("creation_method", "manual"),
            property_data.get("interest_count", 0),
            user_id
        ))
        conn.commit()
        return cursor.lastrowid  #
    # Return the ID of the newly created property
    except sqlite3.IntegrityError as e:
        # Provide more specific error details
        raise ValueError(
            "A property with these characteristics already exists. "
            "Ensure that location, size, type, floor, and bedrooms are unique."
        ) from e
    except sqlite3.Error as e:
        raise ValueError(f"Database error while saving property: {e}")
    finally:
        conn.close()


# Load all properties from the database for a specific user

def load_properties_by_user(user_id, role=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        query = """
        SELECT p.*, (
            SELECT json_group_array(
                json_object(
                    'src', COALESCE(pi.image_src, '')
                )
            )
            FROM property_images pi
            WHERE pi.property_id = p.id
        ) AS images
        FROM properties p
        INNER JOIN property_ownership po ON p.id = po.property_id
        WHERE po.user_id = ?
        """
        params = [user_id]
        if role:
            query += " AND po.role = ?"
            params.append(role)
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        properties = []
        for row in rows:
            property_data = dict(row)
            # Parse the images JSON string
            if property_data.get("images"):
                property_data["images"] = json.loads(property_data["images"])
            else:
                property_data["images"] = []  # Default to an empty list if no images
            properties.append(property_data)
        return properties
    
    except sqlite3.Error as e:
        raise ValueError(f"Database error while loading properties for user: {e}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Error decoding JSON for property images: {e}")
    finally:
        conn.close()
        

def load_property_by_id(property_id):
    """
    Load a property by its ID.
    :param property_id: ID of the property to load.
    :return: A dictionary containing property details, or None if not found.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        SELECT id, friendly_name, property_type, property_size, property_location, property_price, 
               price_per_sqm, bedrooms, bathrooms, floor, year_built, condition,
               renovation_year, energy_class, availability, available_from,
               heating_method, zone, creation_method, interest_count
        FROM properties
        WHERE id = ?
        """, (property_id,))
        property_data = cursor.fetchone()

        if property_data:
            return dict(property_data)
        return None
    except sqlite3.Error as e:
        raise ValueError(f"Database error while loading property: {e}")
    finally:
        conn.close()

def update_property_in_db(property_id, updated_data, user_id):
    """
    Update property details in the database.
    :param property_id: ID of the property to update.
    :param updated_data: Dictionary containing updated property details.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        UPDATE properties
        SET friendly_name = ?, property_type = ?, property_size = ?, property_location = ?, 
            property_price = ?, price_per_sqm = ?, bedrooms = ?, bathrooms = ?, 
            floor = ?, year_built = ?, condition = ?, renovation_year = ?, 
            energy_class = ?, availability = ?, available_from = ?, 
            heating_method = ?, zone = ?, creation_method = ?, interest_count = ?
        WHERE id = ?
        """, (
            updated_data.get("friendly_name"),
            updated_data.get("property_type"),
            updated_data.get("property_size"),
            updated_data.get("property_location"),
            updated_data.get("property_price"),
            updated_data.get("price_per_sqm"),
            updated_data.get("bedrooms"),
            updated_data.get("bathrooms"),
            updated_data.get("floor"),
            updated_data.get("year_built"),
            updated_data.get("condition"),
            updated_data.get("renovation_year"),
            updated_data.get("energy_class"),
            updated_data.get("availability"),
            updated_data.get("available_from"),
            updated_data.get("heating_method"),
            updated_data.get("zone"),
            updated_data.get("creation_method", "manual"),
            updated_data.get("interest_count"),
            user_id 
        ))
        conn.commit()
    except sqlite3.Error as e:
        raise ValueError(f"Database error while updating property: {e}")
    finally:
        conn.close()
        
def delete_property_from_db(property_id):
    """
    Delete a property from the database.
    :param property_id: ID of the property to delete.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("DELETE FROM properties WHERE id = ?", (property_id,))
        conn.commit()
    except sqlite3.Error as e:
        raise ValueError(f"Database error while deleting property: {e}")
    finally:
        conn.close()


# Save the relationship between a property and a user (landlord or agent)

def save_property_ownership(property_id, user_id, role):
    """
    Save the relationship between a property and a user (landlord or agent).
    :param property_id: ID of the property.
    :param user_id: ID of the landlord or agent.
    :param role: Role of the user ('landlord' or 'agent').
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Check if ownership already exists
        cursor.execute("""
        SELECT 1 FROM property_ownership
        WHERE property_id = ? AND user_id = ? AND role = ?
        """, (property_id, user_id, role))
        if cursor.fetchone():
            return  # Relationship already exists, no need to insert
        
        # Insert ownership
        cursor.execute("""
        INSERT INTO property_ownership (property_id, user_id, role)
        VALUES (?, ?, ?)
        """, (property_id, user_id, role))
        conn.commit()
    except sqlite3.Error as e:
        raise ValueError(f"Database error while saving property ownership: {e}")
    finally:
        conn.close()
        

def get_users_for_similar_properties(property_id):
    """
    Fetch users (landlords and agents) associated with properties having similar characteristics.
    :param property_id: The ID of the reference property.
    :return: List of dictionaries containing user details and roles.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Fetch the characteristics of the reference property
        query = """
        SELECT property_type, property_size, property_location, floor, bedrooms
        FROM properties
        WHERE id = ?
        """
        cursor.execute(query, (property_id,))
        reference_property = cursor.fetchone()

        if not reference_property:
            raise ValueError(f"Property ID {property_id} not found.")

        # Find all properties with the same characteristics
        query = """
        SELECT id FROM properties
        WHERE property_type = ? AND property_size = ? AND property_location = ? AND floor = ? AND bedrooms = ?
        """
        cursor.execute(query, reference_property)
        similar_property_ids = [row["id"] for row in cursor.fetchall()]

        if not similar_property_ids:
            return []

        # Fetch users associated with the similar properties
        query = """
        SELECT u.username, u.email, po.role
        FROM property_ownership po
        JOIN users u ON po.user_id = u.id
        WHERE po.property_id IN ({})
        """.format(", ".join(["?"] * len(similar_property_ids)))  # Dynamically generate the placeholders
        cursor.execute(query, similar_property_ids)
        rows = cursor.fetchall()
        return [{"username": row["username"], "email": row["email"], "role": row["role"]} for row in rows]

    except Exception as e:
        raise ValueError(f"Error loading users for similar properties: {e}")
    finally:
        conn.close()


# SAVE PROPERTY IMAGES TO THE DATABASE

def save_property_image_to_db(property_id, user_id, images):
    """
    Save property images (URLs or binary data) to the database.
    :param property_id: ID of the associated property.
    :param user_id: ID of the user uploading the images.
    :param images: List of dictionaries containing 'src' or 'blob'.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        for image in images:
            cursor.execute("""
                INSERT INTO property_images (property_id, user_id, image_src, image_blob)
                VALUES (?, ?, ?, ?)
            """, (
                property_id,
                user_id,
                image.get("src"),
                image.get("blob"),
            ))
        conn.commit()
    except sqlite3.Error as e:
        raise ValueError(f"Error saving property images: {e}")
    finally:
        conn.close()
                

def load_property_images(property_id):
    """
    Load property images for a given property ID.
    :param property_id: ID of the property to load images for.
    :return: A list of image dictionaries, or an empty list if no images are found.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        SELECT image_src, image_blob
        FROM property_images
        WHERE property_id = ?
        """, (property_id,))
        rows = cursor.fetchall()
        images = [{"src": row["image_src"], "blob": row["image_blob"]} for row in rows]
        return images
    except sqlite3.Error as e:
        raise ValueError(f"Database error while loading property images: {e}")
    finally:
        conn.close()
        

        
def replace_property_images(property_id, user_id, images):
    """
    Replace all images for a given property.
    :param property_id: ID of the property.
    :param user_id: ID of the user uploading the images.
    :param images: List of dictionaries containing 'src' or 'blob'.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Delete existing images for the property
        cursor.execute("""
        DELETE FROM property_images WHERE property_id = ?
        """, (property_id,))
        
        # Insert new images
        for image in images:
            cursor.execute("""
            INSERT INTO property_images (property_id, user_id, image_src, image_blob)
            VALUES (?, ?, ?, ?)
            """, (
                property_id,
                user_id,
                image.get("src"),
                image.get("blob"),
            ))
        conn.commit()
    except sqlite3.Error as e:
        raise ValueError(f"Database error while replacing property images: {e}")
    finally:
        conn.close()


# Load property images including BLOBs
def load_property_images_with_blobs(property_id):
    """
    Load property images including BLOBs.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
        SELECT image_src, image_blob
        FROM property_images
        WHERE property_id = ?
        """, (property_id,))
        rows = cursor.fetchall()
        images = [{"src": row["image_src"], "blob": row["image_blob"]} for row in rows]
        return images
    except sqlite3.Error as e:
        raise ValueError(f"Database error while loading property images with blobs: {e}")
    finally:
        conn.close()

# save property interest to the database
        
def save_property_interest(property_id, user_id):
    """
    Save a user's interest in a property.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Insert the user's interest in the property
        cursor.execute("""
        INSERT INTO property_interest (property_id, user_id)
        VALUES (?, ?)
        """, (property_id, user_id))

        conn.commit()
        return True

    except sqlite3.IntegrityError:
        # The user already expressed interest in this property
        return False

    finally:
        conn.close()
        

# Delete property interest from the database
        
def delete_property_interest(property_id, user_id):
    """
    Remove a user's interest in a property.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        DELETE FROM property_interest
        WHERE property_id = ? AND user_id = ?
        """, (property_id, user_id))

        if cursor.rowcount > 0:  # Check if any rows were deleted
            conn.commit()
            return True  # Successfully removed interest
        else:
            return False  # No interest to delete

    finally:
        conn.close()
        
def update_renter_interest_status(property_id, user_id, status):
    """
    Update the status of a renter's interest in a property.

    :param property_id: The ID of the property.
    :param user_id: The ID of the renter.
    :param status: The new status ('Accepted' or 'Rejected').
    :return: bool: True if the update was successful, False otherwise.
    """
    conn = get_db_connection()
    
    try:
        cursor = conn.cursor()

        # Ensure the status is either 'Accepted' or 'Rejected'
        if status not in ['Accepted', 'Rejected']:
            raise ValueError("Status must be 'Accepted' or 'Rejected'.")

        # Update the status in the property_interest table
        cursor.execute("""
        UPDATE property_interest
        SET status = ?
        WHERE property_id = ? AND user_id = ?
        """, (status, property_id, user_id))

        if cursor.rowcount > 0:
            conn.commit()
            print(f"Status for user_id {user_id} on property_id {property_id} updated to '{status}'.")
            return True
        else:
            print(f"No interest found for user_id {user_id} on property_id {property_id}.")
            return False

    except sqlite3.Error as e:
        conn.rollback()  # Rollback changes on error
        print(f"Error updating status for user_id {user_id} on property_id {property_id}: {e}")
        return False

    finally:
        conn.close()

def load_renters_by_interest_status(property_id, status):
    """
    Load all renters who have a specific status for a given property.

    :param property_id: The ID of the property.
    :param status: The status to filter by ('Pending', 'Accepted', or 'Rejected').
    :return: list: A list of renter user IDs with the specified status.
    """
    conn = get_db_connection()
    
    try:
        cursor = conn.cursor()

        # Query renters with the specified status
        cursor.execute("""
        SELECT user_id
        FROM property_interest
        WHERE property_id = ? AND status = ?
        """, (property_id, status))

        rows = cursor.fetchall()
        conn.close()

        # Extract user IDs from the rows
        user_ids = [row[0] for row in rows]
        print(f"{len(user_ids)} renters with status '{status}' found for property_id {property_id}.")
        return user_ids

    except sqlite3.Error as e:
        print(f"Error loading renters with status '{status}' for property_id {property_id}: {e}")
        return []

    finally:
        conn.close()



def has_expressed_interest(property_id, user_id):
    """
    Check if a user has already expressed interest in a property.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("""
        SELECT 1 FROM property_interest
        WHERE property_id = ? AND user_id = ?
        """, (property_id, user_id))
        return cursor.fetchone() is not None  # True if interest exists

    finally:
        conn.close()
        
def load_renter_ids_for_property(property_id):
    """
    Load all user IDs of renters who have expressed interest in a specific property.

    :param property_id: The ID of the property.
    :return: A list of user IDs.
    """
    conn = get_db_connection()
    
    try:
        cursor = conn.cursor()

        # Query to fetch user IDs
        cursor.execute("""
        SELECT user_id
        FROM property_interest
        WHERE property_id = ?
        """, (property_id,))

        rows = cursor.fetchall()
        conn.close()

        # Extract user IDs from the rows
        user_ids = [row[0] for row in rows]

        print(f"{len(user_ids)} renters found for property_id {property_id}.")
        return user_ids

    except sqlite3.Error as e:
        print(f"Error loading renter IDs for property_id {property_id}: {e}")
        return []

    finally:
        conn.close()
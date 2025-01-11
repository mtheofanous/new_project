import sqlite3
from db_setup import get_db_connection


# Save a favorite item to the user's favorites

def save_to_favorites(user_id, favorite_type, favorite_id):
    """
    Save an item (renter, landlord, agent, or property) to the user's favorites.

    :param user_id: The ID of the user marking the favorite.
    :param favorite_type: The type of the favorite ('renter', 'landlord', 'agent', 'property').
    :param favorite_id: The ID of the favorited item.
    :return: bool: True if the favorite was saved successfully, False if it already exists.
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        # Insert into favorites table
        cursor.execute("""
        INSERT INTO favorites (user_id, favorite_type, favorite_id)
        VALUES (?, ?, ?)
        """, (user_id, favorite_type, favorite_id))

        conn.commit()
        print(f"Favorite saved: User {user_id} favorited {favorite_type} {favorite_id}.")
        return True

    except sqlite3.IntegrityError:
        print(f"Favorite already exists: User {user_id} already favorited {favorite_type} {favorite_id}.")
        return False

    except sqlite3.Error as e:
        print(f"Error saving favorite: {e}")
        return False

    finally:
        conn.close()
        
        
# Remove a favorite item from the user's favorites

def remove_from_favorites(user_id, favorite_type, favorite_id):
    """
    Remove an item (renter, landlord, agent, or property) from the user's favorites.

    :param user_id: The ID of the user removing the favorite.
    :param favorite_type: The type of the favorite ('renter', 'landlord', 'agent', 'property').
    :param favorite_id: The ID of the favorited item.
    :return: bool: True if the favorite was removed successfully, False otherwise.
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        # Delete from favorites table
        cursor.execute("""
        DELETE FROM favorites
        WHERE user_id = ? AND favorite_type = ? AND favorite_id = ?
        """, (user_id, favorite_type, favorite_id))

        if cursor.rowcount > 0:
            conn.commit()
            print(f"Favorite removed: User {user_id} unfavorited {favorite_type} {favorite_id}.")
            return True
        else:
            print(f"No favorite found for User {user_id} and {favorite_type} {favorite_id}.")
            return False

    except sqlite3.Error as e:
        print(f"Error removing favorite: {e}")
        return False

    finally:
        conn.close()


# Load all favorites for a specific user

def load_favorites(user_id):
    """
    Load all favorites for a specific user.

    :param user_id: The ID of the user whose favorites are being retrieved.
    :return: list of dict: A list of the user's favorites.
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        # Fetch favorites for the user
        cursor.execute("""
        SELECT favorite_type, favorite_id, created_at
        FROM favorites
        WHERE user_id = ?
        """, (user_id,))

        rows = cursor.fetchall()
        return [
            {
                "favorite_type": row[0],
                "favorite_id": row[1],
                "created_at": row[2]
            }
            for row in rows
        ]

    except sqlite3.Error as e:
        print(f"Error loading favorites for user {user_id}: {e}")
        return []

    finally:
        conn.close()


# Check if an item is already favorited by a user

def is_favorited(user_id, favorite_type, favorite_id):
    """
    Check if an item is already favorited by the user.

    :param user_id: The ID of the user.
    :param favorite_type: The type of the favorite ('renter', 'landlord', 'agent', 'property').
    :param favorite_id: The ID of the item to check.
    :return: bool: True if the item is favorited, False otherwise.
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        # Check for existence in favorites table
        cursor.execute("""
        SELECT 1
        FROM favorites
        WHERE user_id = ? AND favorite_type = ? AND favorite_id = ?
        """, (user_id, favorite_type, favorite_id))

        return cursor.fetchone() is not None

    except sqlite3.Error as e:
        print(f"Error checking favorite: {e}")
        return False

    finally:
        conn.close()

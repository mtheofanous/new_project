import json
from db_setup import get_db_connection
import sqlite3

def find_matching_properties_dict(filter_options):
    """
    Find all properties matching the given filter options.
    Returns a list of dictionaries containing property details.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        # Base query
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
        WHERE 1=1
        """
        params = []

        # Dynamically add filters based on filter_options
        if "budget_min" in filter_options and filter_options["budget_min"] is not None:
            query += " AND p.property_price >= ?"
            params.append(filter_options["budget_min"])

        if "budget_max" in filter_options and filter_options["budget_max"] is not None:
            query += " AND p.property_price <= ?"
            params.append(filter_options["budget_max"])

        if "property_type" in filter_options and filter_options["property_type"]:
            query += " AND p.property_type = ?"
            params.append(filter_options["property_type"])

        if "property_size_min" in filter_options and filter_options["property_size_min"] is not None:
            query += " AND p.property_size >= ?"
            params.append(filter_options["property_size_min"])

        if "property_size_max" in filter_options and filter_options["property_size_max"] is not None:
            query += " AND p.property_size <= ?"
            params.append(filter_options["property_size_max"])

        if "bedrooms" in filter_options and filter_options["bedrooms"] is not None:
            query += " AND p.bedrooms >= ?"
            params.append(filter_options["bedrooms"])

        if "bathrooms" in filter_options and filter_options["bathrooms"] is not None:
            query += " AND p.bathrooms >= ?"
            params.append(filter_options["bathrooms"])

        if "floor" in filter_options and filter_options["floor"] is not None:
            query += " AND p.floor >= ?"
            params.append(filter_options["floor"])

        # Execute the query
        cursor.execute(query, params)
        rows = cursor.fetchall()

        # Parse rows into dictionaries
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
        raise ValueError(f"Database error while finding properties: {e}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Error decoding JSON for property images: {e}")
    finally:
        conn.close()

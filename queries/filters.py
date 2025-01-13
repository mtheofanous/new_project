import json
from db_setup import get_db_connection
import sqlite3
import base64


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

def find_matching_renters_dict(filter_options):
    """
    Find renters that match the given filter options.
    Returns a list of dictionaries with the renter profile and rental preferences.

    :param filter_options: A dictionary containing filter criteria.
    :return: A list of dictionaries with matching renter profiles and rental preferences.
    """
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # Base query
        query = """
        SELECT 
            rp.id AS profile_id,
            rp.user_id,
            rp.profile_pic,
            rp.tagline,
            rp.age,
            rp.phone,
            rp.nationality,
            rp.occupation,
            rp.contract_type,
            rp.income,
            rp.work_mode,
            rp.bio,
            rp.hobbies,
            rp.social_media,
            rp.created_at AS profile_created_at,
            rp.updated_at AS profile_updated_at,
            rpfs.preferred_city,
            rpfs.preferred_area,
            rpfs.budget_min,
            rpfs.budget_max,
            rpfs.property_type,
            rpfs.property_size_min,
            rpfs.property_size_max,
            rpfs.bedrooms,
            rpfs.bathrooms,
            rpfs.floor,
            rpfs.number_of_people,
            rpfs.move_in_date,
            rpfs.pets,
            rpfs.pet_type,
            rpfs.lease_duration,
            rpfs.created_at AS preferences_created_at,
            rpfs.updated_at AS preferences_updated_at
        FROM renter_profiles rp
        LEFT JOIN rental_preferences rpfs ON rp.id = rpfs.profile_id
        WHERE 1=1
        """
        params = []

        # Filters for Renter Profiles
        profile_filters = {
            "min_age": " AND rp.age >= ?",
            "max_age": " AND rp.age <= ?",
            "nationality": " AND LOWER(rp.nationality) LIKE ?",
            "contract_type": " AND LOWER(rp.contract_type) LIKE ?",
            "min_income": " AND rp.income >= ?",
            "max_income": " AND rp.income <= ?",
            "work_mode": " AND LOWER(rp.work_mode) LIKE ?"
        }

        for key, condition in profile_filters.items():
            if key in filter_options and filter_options[key]:
                query += condition
                if "LIKE" in condition:
                    params.append(f"%{filter_options[key].lower()}%")
                else:
                    params.append(filter_options[key])

        # Filters for Rental Preferences
        preference_filters = {
            "preferred_city": " AND LOWER(rpfs.preferred_city) LIKE ?",
            "preferred_area": " AND LOWER(rpfs.preferred_area) LIKE ?",
            "budget_min": " AND rpfs.budget_min >= ?",
            "budget_max": " AND rpfs.budget_max <= ?",
            "property_type": " AND rpfs.property_type = ?",
            "bedrooms": " AND rpfs.bedrooms >= ?",
            "bathrooms": " AND rpfs.bathrooms >= ?",
            "floor": " AND rpfs.floor >= ?",
            "number_of_people": " AND rpfs.number_of_people >= ?",
            "move_in_date": " AND rpfs.move_in_date >= ?",
            "pets": " AND rpfs.pets = ?",
            "lease_duration": " AND rpfs.lease_duration = ?"
        }

        for key, condition in preference_filters.items():
            if key in filter_options and filter_options[key] not in [None, "Any"]:
                query += condition
                if "LIKE" in condition:
                    params.append(f"%{filter_options[key].lower()}%")
                elif key == "pets":
                    params.append(1 if filter_options[key] == "Yes" else 0)
                else:
                    params.append(filter_options[key])

        # Execute the query
        cursor.execute(query, params)
        rows = cursor.fetchall()

        # Parse results into a list of dictionaries
        def process_profile_pic(blob):
            return base64.b64encode(blob).decode() if blob else None

        renters = []
        for row in rows:
            renter_data = dict(row)
            renter_data["profile_pic"] = process_profile_pic(renter_data["profile_pic"])
            renters.append(renter_data)

        return renters

    except sqlite3.Error as e:
        raise ValueError(f"Error finding matching renters: {e}, Query: {query}, Params: {params}")
    finally:
        conn.close()


from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig
import psycopg2
from dotenv import load_dotenv
from .schema import Items
import os


load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


@tool
def fetch_menu(config: RunnableConfig) -> list[dict]:
    """
    Fetches the pizza menu from the database and returns the items as a list of dictionaries.

    This function retrieves all the menu items from the 'menu' table, including details 
    like category and item name. It requires the customer's name to be provided in 
    the configuration. The function returns a list of dictionaries, where each dictionary 
    represents a menu item with its associated details.

    Args:
        config (RunnableConfig): Configuration object containing customer details.

    Returns:
        list[dict]: A list of dictionaries, each containing details of a menu item (e.g., category, item name).
    """
    
    configuration = config.get("configurable", {})
    customer_name = configuration.get("customer_name", None)
    if not customer_name:
        raise ValueError("No passenger ID configured.")

    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        # Fetch category and item_name
        cursor.execute("SELECT * FROM menu;")
        rows = cursor.fetchall()
        rows = [row for row in rows]
        column_names = [column[0] for column in cursor.description]
        results = [dict(zip(column_names, row)) for row in rows]
    except Exception as e:
        print("An error occurred:", e)

    finally:
        if conn:
            conn.close()
        if cursor:
            cursor.close()
    return results


@tool
def order_food(items:Items, config: RunnableConfig) -> list[dict]:
    """
    Processes the customer's food order and inserts the order details into the database.

    This function creates a new order in the database for the specified customer, 
    generating an order ID. It then inserts the items ordered (with their quantity 
    and total price) into the 'order_items' table. The customer's name must be 
    provided in the configuration. The function returns the generated order ID.

    Args:
        items (Items): An object containing a list of items with their details 
                       (item_id, quantity, total_price).
        config (RunnableConfig): Configuration object containing customer details.

    Returns:
        int: The generated order ID.
    """
    
    configuration = config.get("configurable", {})
    customer_name = configuration.get("customer_name", None)
    if not customer_name:
        raise ValueError("No passenger ID configured.")

    conn = psycopg2.connect(DATABASE_URL)
    cursor = conn.cursor()

    try:
        query = """INSERT INTO orders (customer_name) VALUES (%s) RETURNING order_id"""
        cursor.execute(query, (customer_name,))
        order_id = cursor.fetchone()[0]
        items = items.items
        items = [(order_id,) + (item.item_id, item.quantity, item.total_price) for item in items]
        query = """INSERT INTO order_items (order_id, item_id, quantity, total_price) VALUES (%s, %s, %s, %s)"""
        cursor.executemany(query, items)
        conn.commit()
    except Exception as e:
        print("An error occurred:", e)

    finally:
        if conn:
            conn.close()
        if cursor:
            cursor.close()
    return order_id


@tool
def fetch_user_order_information(config: RunnableConfig) -> list[dict]:
    """
    Fetches the most recent order details for a specific customer from the database.
    
    This function retrieves the order ID, customer name, order date, item ID, 
    quantity, and total price for the latest order placed by the specified customer. 
    The customer's name must be provided in the configuration. The function returns 
    a list of dictionaries containing the order information.

    Returns:
        list[dict]: A list of dictionaries with order details, including item IDs, 
                    quantities, and total prices.
    """

    configuration = config.get("configurable", {})
    customer_name = configuration.get("customer_name", None)
    if not customer_name:
        raise ValueError("No passenger ID configured.")

    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()

        query = """
        SELECT orders.order_id, orders.customer_name, orders.order_date, order_items.item_id, order_items.quantity, order_items.total_price
        FROM orders
        JOIN order_items ON orders.order_id = order_items.order_id
        WHERE orders.order_date = (SELECT MAX(orders.order_date) FROM orders) AND orders.customer_name = %s
        """
        cursor.execute(query, (customer_name,))
        rows = cursor.fetchall()
        rows = [row for row in rows]
        column_names = [column[0] for column in cursor.description]
        results = [dict(zip(column_names, row)) for row in rows]
    except Exception as e:
        print("An error occurred:", e)

    finally:
        if conn:
            conn.close()
        if cursor:
            cursor.close()
    return results

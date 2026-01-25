from flask import Flask, request, jsonify, render_template
import mysql.connector

app = Flask(__name__)


def create_connection():
    return mysql.connector.connect(
        host='127.0.0.1',
        port=3306,
        user='root',  
        password='P@ssw0rd',  
        database='zomato'
    )


# Home route
@app.route('/')
def home():
    return render_template('home.html')


# Place an order (POST)
@app.route('/place_order', methods=['POST'])
def place_order():
    cursor = None
    connection = None
    try:
        order_data = request.get_json()  # Get the JSON data sent by the frontend

        first_name = order_data.get('first_name')
        last_name = order_data.get('last_name')
        email = order_data.get('email')
        phone = order_data.get('phone')
        cart = order_data.get('cart')  # The cart is an array of items
        address = order_data.get('address')  # The delivery address

        if not cart or not address or not first_name or not last_name or not email or not phone:
            return jsonify({"error": "Missing required fields: user details, cart, or address."}), 400

        if '@' not in email:
            return jsonify({"error": "Invalid email format."}), 400

        connection = create_connection()
        cursor = connection.cursor()

        # Check if user exists by email
        cursor.execute("SELECT user_id FROM customers WHERE email = %s", (email,))
        existing_user = cursor.fetchone()

        if existing_user:
            user_id = existing_user[0]
            # Fetch name for response
            cursor.execute("SELECT first_name, last_name FROM customers WHERE user_id = %s", (user_id,))
            user_result = cursor.fetchone()
            full_name = f"{user_result[0]} {user_result[1]}"
        else:
            # Get next user_id
            cursor.execute("SELECT MAX(user_id) FROM customers")
            max_id_result = cursor.fetchone()
            new_user_id = (max_id_result[0] or 0) + 1

            # Insert new customer
            insert_user_sql = """
                INSERT INTO customers (user_id, first_name, last_name, phone_number, email)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(insert_user_sql, (new_user_id, first_name, last_name, phone, email))
            user_id = new_user_id
            full_name = f"{first_name} {last_name}"

        # Calculate total quantity
        total_quantity = sum(int(item['quantity']) for item in cart)

        # Insert the order into the database
        sql_order = """
            INSERT INTO orders (user_id, delivery_address, quantity)
            VALUES (%s, %s, %s)
        """
        cursor.execute(sql_order, (user_id, address, total_quantity))
        order_id = cursor.lastrowid

        # Insert each item in the cart into order_items
        for item in cart:
            item_name = item['name']
            quantity = item['quantity']

            cursor.execute("SELECT item_id, price FROM items WHERE item_name = %s", (item_name,))
            result = cursor.fetchone()

            if not result:
                connection.rollback()
                return jsonify({"error": f"Item {item_name} not found."}), 400

            item_id, price = result

            # SQL query to insert the order item
            sql_item = """
                INSERT INTO order_items (order_id, item_id, quantity, price)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(sql_item, (order_id, item_id, quantity, price))

        connection.commit()
        return jsonify({"message": f"Order placed successfully for {full_name}!"}), 200

    except mysql.connector.errors.IntegrityError as e :
        connection.rollback()
        return jsonify({"error": "User with this email already exists or database constraint violation."}), 400
    except Exception as e:
        if connection:
            connection.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()



# Get all orders (GET)
@app.route('/orders', methods=['GET'])
def get_orders():
    cursor = None
    connection = None
    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM orders")
        orders = cursor.fetchall()

        return jsonify({"orders": orders}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


# Get menu data (GET)
@app.route('/api/menu', methods=['GET'])
def get_menu():
    cursor = None
    connection = None
    try:
        connection = create_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT i.item_name, i.price, c.category_name, 
                   CASE WHEN c.category_id = 1 THEN true ELSE false END as veg
            FROM items i
            JOIN categories c ON i.category_id = c.category_id
            ORDER BY c.category_id, i.item_id
        """)
        items = cursor.fetchall()

        # Group items by category
        sections = {}
        for item in items:
            cat_name = item['category_name']
            if cat_name not in sections:
                sections[cat_name] = []
            sections[cat_name].append({
                "labels": [{"displayName": item['item_name']}],
                "attributes": {
                    "price": {"currencyCode": "INR", "units": str(int(item['price']))},
                    "spiciness": "MEDIUM",  # Default, can be extended
                    "veg": item['veg'],
                    "description": f"Delicious {item['item_name'].lower()}"  # Placeholder
                },
                "mediaKeys": [f"{item['item_name'].lower().replace(' ', '_')}.jpg"]  # Placeholder
            })

        menu_data = {
            "labels": [{"displayName": "Food Menu", "languageCode": "en"}],
            "cuisines": ["INDIAN"],
            "sections": [
                {
                    "labels": [{"displayName": cat_name}],
                    "items": items_list
                }
                for cat_name, items_list in sections.items()
            ]
        }
        return jsonify(menu_data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


@app.route('/menu')
def menu_page():
    return render_template('index.html')

@app.route('/contact')
def contact_page():
    return render_template('contact.html')

@app.route('/cart', methods=['GET', 'POST'])
def cart_page():
    orders = []
    error = None
    if request.method == 'POST':
        search_term = request.form.get('search', '').strip()
        if search_term:
            cursor = None
            connection = None
            try:
                connection = create_connection()
                cursor = connection.cursor(dictionary=True)
                # Join orders with customers
                query = """
                    SELECT o.order_id, o.quantity as total_quantity, o.delivery_address as address, o.order_date,
                           c.first_name, c.last_name, c.email, c.phone_number as phone
                    FROM orders o
                    JOIN customers c ON o.user_id = c.user_id
                    WHERE c.first_name LIKE %s OR c.last_name LIKE %s OR c.email LIKE %s
                """
                cursor.execute(query, (f'%{search_term}%', f'%{search_term}%', f'%{search_term}%'))
                db_orders = cursor.fetchall()
                for order in db_orders:
                    # Fetch order items for this order
                    cursor.execute("""
                        SELECT i.item_name, oi.quantity
                        FROM order_items oi
                        JOIN items i ON oi.item_id = i.item_id
                        WHERE oi.order_id = %s
                    """, (order['order_id'],))
                    items = cursor.fetchall()
                    order['cart'] = [{'name': item['item_name'], 'quantity': item['quantity']} for item in items]
                    orders.append(order)
            except Exception as e:
                error = f"Error searching orders: {str(e)}"
            finally:
                if cursor:
                    cursor.close()
                if connection:
                    connection.close()
        else:
            error = "Please enter a search term."
    return render_template('cart.html', orders=orders, error=error)

if __name__ == '__main__':
    app.run(debug=True)

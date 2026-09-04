import sqlite3

class OrderService:
    def __init__(self, db_path="database/inventory.db"):
        self.db_path = db_path

    def create_order(self, customer_name):

        connect = sqlite3.connect(self.db_path)
        cr = connect.cursor()

        cr.execute('INSERT INTO orders (customer_name, total_amount) VALUES (?, ?)', (customer_name, 0.0))

        connect.commit()
        order_id= cr.lastrowid
        connect.close()

        return order_id

    def add_order_item(self, order_id, product_id, quantity):

        connect = sqlite3.connect(self.db_path)
        cr = connect.cursor()

        try: 
            cr.execute('SELECT price, stock FROM products WHERE id = ?', (product_id,))
            product = cr.fetchone()

            if not product:
                raise ValueError(f"Product ID {product_id} does not exist.")

            price = product[0]
            current_stock = product[1]

            if current_stock < quantity :
                raise ValueError(f"Insufficient stock! Only {current_stock} available.")

            cr.execute('''
            INSERT INTO order_items (order_id, product_id, quantity, price_at_sale)
            VALUES (?, ?, ?, ?)''', (order_id, product_id, quantity, price))

            new_stock = current_stock - quantity
            cr.execute('UPDATE products SET stock = ? WHERE id = ?',(new_stock, product_id))

            item_total_price = quantity * price
            cr.execute('UPDATE orders SET total_amount = total_amount + ? WHERE id = ? ', (item_total_price, order_id))

            connect.commit()
            return True

        except Exception as e:
            connect.rollback()
            raise e 

        finally:
            connect.close()

    def get_order_summary(self, order_id):

        connect = sqlite3.connect(self.db_path)
        cr = connect.cursor()

        cr.execute('SELECT id, customer_name, created_at, total_amount FROM orders WHERE id = ?', (order_id,))

        order = cr.fetchone()

        if not order :
            raise ValueError (f"Order ID {order_id} Not available.")

        cr.execute('''
            SELECT products.name, order_items.quantity, order_items.price_at_sale
            FROM order_items
            JOIN products ON order_items.product_id = products.id
            WHERE order_items.order_id = ?
            ''', (order_id,))

        items = cr.fetchall()

        order_summary = {
            "order_id" : order[0],
            "customer_name" : order[1],
            "created_at" : order[2],
            "total_amount" : order[3],
            "items" : []
        }

        for item in items:
            order_summary["items"].append({
                "product_name" : item[0],
                "quantity" : item[1],
                "price_at_sale" : item[2]
            })

        connect.close()
        return order_summary
    


        
    

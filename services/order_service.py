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



        
    

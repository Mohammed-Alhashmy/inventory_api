import sqlite3

class ProductService:
    def __init__(self, db_path="database/inventory.db"):
        self.db_path = db_path

    def add_product(self, name, price, stock=0):

        if price <= 0:
            raise ValueError("Price must be greater than zero.")
        if stock < 0 :
            raise ValueError("Stock cannot be negative.")

        connect = sqlite3.connect(self.db_path)
        cr = connect.cursor()

        cr.execute('''
            INSERT INTO products (name, price, stock)
            VALUES (?, ?, ?)
        
        ''', (name, price, stock))

        connect.commit()
        product_id = cr.lastrowid
        connect.close()

        return product_id

    def get_all_products(self):

        connect = sqlite3.connect(self.db_path)
        cr = connect.cursor()

        cr.execute('SELECT id, name, price, stock FROM products')
        rows = cr.fetchall()
        connect.close()

        products = []

        for row in rows:
            products.append({
                "id": row[0],
                "name": row[1],
                "price": row[2],
                "stock": row[3]
            })
        return products

    def update_stock(self, product_id, amount_change):

        connect = sqlite3.connect(self.db_path)
        cr = connect.cursor()

        cr.execute('SELECT stock FROM products WHERE id = ?', (product_id,))
        result = cr.fetchone()

        if not result :
            connect.close()
            raise ValueError(f"Product with ID {product_id} dose not exist.")

        current_stock = result[0]
        new_stock = current_stock + amount_change

        if new_stock < 0:
            connect.close()
            raise ValueError(f"Insufficient stock! Current stock {current_stock}")

        cr.execute('UPDATE products SET stock = ? WHERE id = ?', (new_stock, product_id))

        connect.commit()
        connect.close()
        return new_stock
        

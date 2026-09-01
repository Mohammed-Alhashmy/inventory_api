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

        cr.execute('SELECT id, name, price, stock, FROM products')
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
    

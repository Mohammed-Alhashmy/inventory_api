from services.product_service import ProductService

service = ProductService()
try:
    product_id = service.add_product("Laptop", 1200.50, 10)
    print(f"Product added successfully with ID: {product_id}")
except Exception as e:
    print(f"Error: {e}")
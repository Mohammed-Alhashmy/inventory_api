from services.order_service import OrderService
from services.product_service import ProductService

order_service = OrderService()
product_service = ProductService()

# try:
#     print("Creating new order...")
#     order_id = order_service.create_order(customer_name="Ali")
#     print(f"Order created successfully with ID: {order_id}")

#     print("\nAdding 2 items of Product ID 1 to the order...")
#     order_service.add_order_item(order_id=order_id, product_id=1, quantity=2)
#     print("Items added, stock deducted, and order total updated successfully!")

#     print("\nCurrent Products State:")
#     print(product_service.get_all_products())

# except Exception as e:
#     print(f"Transaction Failed: {e}")


#     #note 
    #This test product from ai :)



try:
    summary = order_service.get_order_summary(3)
    print("Order Invoice:")
    print(summary)
except Exception as e:
    print(f"Error fetching summary: {e}")
from app.database import get_order_count


count = get_order_count()

print(f"Total orders in PostgreSQL: {count}")
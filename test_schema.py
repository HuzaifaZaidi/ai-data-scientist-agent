from app.database import get_database_schema


schema = get_database_schema()

print("DATABASE SCHEMA")
print("=" * 50)

for table_name, columns in schema.items():
    print(f"\nTable: {table_name}")

    for column in columns:
        print(
            f"  - {column['column']} "
            f"({column['data_type']})"
        )
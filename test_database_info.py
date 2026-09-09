from app.database import get_database_info


database_info = get_database_info()

print("DATABASE INFORMATION")
print("=" * 60)

print("\nSCHEMA")
print("-" * 60)

for table_name, columns in database_info["schema"].items():
    print(f"\nTable: {table_name}")

    for column in columns:
        print(
            f"  - {column['column']} "
            f"({column['data_type']})"
        )


print("\n\nRELATIONSHIPS")
print("-" * 60)

for relationship in database_info["relationships"]:
    print(
        f"{relationship['child_table']}."
        f"{relationship['child_column']}"
        f"  →  "
        f"{relationship['parent_table']}."
        f"{relationship['parent_column']}"
    )
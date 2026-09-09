from app.database import get_database_relationships


relationships = get_database_relationships()

print("DATABASE RELATIONSHIPS")
print("=" * 50)

for relationship in relationships:
    print(
        f"{relationship['child_table']}."
        f"{relationship['child_column']}"
        f"  →  "
        f"{relationship['parent_table']}."
        f"{relationship['parent_column']}"
    )
# SQL tables

```sql
CREATE TABLE "users" (
    "id" INTEGER NOT NULL,
    "nickname" TEXT NOT NULL,
    "password" TEXT NOT NULL,
    PRIMARY KEY("id")
)
```

Here's how to delete a table
```sql
DROP TABLE "users"
```
# Left Join explanation

Consider two tables, A and B:

LEFT JOIN Example:

```SQL
SELECT A.*, B.*
FROM A
LEFT JOIN B ON A.id = B.a_id;
```

This query includes all records from table A (left table) and matches
records from table B (right table). If there are rows in A that do not
have corresponding rows in B, those rows in A will still appear in the
result, with NULLs for columns from B.


```markdown
A (Left Table)        B (Right Table)
+----+          +----+
| id |          | a_id |
+----+          +----+
| 1  |  <--\    | 1  |
| 2  |  <--|----| 2  |
| 3  |  <--/
```


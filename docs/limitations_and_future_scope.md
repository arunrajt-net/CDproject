# Limitations and Future Scope

## 1. Current Limitations
The **Mini SQL Compiler** was constructed specifically as an educational compiler front-end for a restricted SQL dialect. By deliberate design, the following boundaries exist:

1. **Restricted Query Syntax:**
   - Supports only `SELECT`, `FROM`, `WHERE`, and `ORDER BY` query structures.
   - Does not support `GROUP BY`, `HAVING`, `LIMIT`, `OFFSET`, or set operations (`UNION`, `INTERSECT`).
2. **Single Table Context:**
   - Queries can currently select from one table at a time with optional aliases (`FROM students s`).
   - Relational joins (`JOIN ... ON ...`) are not currently parsed.
3. **No Execution Engine / DBMS Storage:**
   - The compiler front end stops after semantic validation and AST generation. It does not physically execute queries on real disk partitions or retrieve row records.
4. **No DDL / DML:**
   - Data definition (`CREATE TABLE`) and data manipulation (`INSERT`, `UPDATE`, `DELETE`) are out of scope.

---

## 2. Future Enhancements

1. **Relational Joins Support:**
   - Extend CFG to support `FROM table1 JOIN table2 ON table1.id = table2.id`.
   - Update semantic analyzer to resolve multi-table qualified column names (e.g. `students.name`).
2. **Aggregations & Grouping:**
   - Integrate grammar rules for `COUNT(*)`, `SUM(col)`, `AVG(col)`.
   - Add `GROUP BY` and `HAVING` clause analysis.
3. **Query Optimization Phase (Intermediate Code Generation):**
   - Implement relational algebra tree transformations (e.g. pushing selections down the query tree: $\sigma_{\text{cond}}(R)$ before $\pi_{\text{cols}}(R)$).
4. **Physical In-Memory Execution Engine:**
   - Connect the validated AST to an in-memory Pandas or SQLite execution engine to return query result rows.
5. **Interactive Visual Tree Graph:**
   - Enhance the web UI with a D3.js or SVG node-link graph visualization for the Parse Tree.

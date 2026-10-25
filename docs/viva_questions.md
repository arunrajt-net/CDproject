# Viva Preparation Guide: 45 Questions & Answers

This guide is designed for B.Tech Computer Science students to ace their Compiler Design project viva and practical examination.

---

### Q1. What is a compiler?
**Answer:** A compiler is a specialized software program that translates source code written in a high-level programming language (e.g., C, Python, SQL) into a low-level target representation (e.g., machine code, bytecode, or an intermediate representation) without altering the program's meaning.

### Q2. What is a compiler front-end?
**Answer:** The compiler front-end is the analysis phase of a compiler. It reads the source code, validates its lexical structure, checks syntax against a formal grammar, constructs parse trees/ASTs, and performs semantic validation. It is independent of the target machine architecture.

### Q3. What is SQL?
**Answer:** SQL stands for Structured Query Language. It is a declarative domain-specific language used to store, manipulate, and retrieve structured data from relational database management systems.

### Q4. What is a Mini SQL Compiler?
**Answer:** A Mini SQL Compiler is an educational compiler front-end that accepts a restricted subset of SQL queries (specifically `SELECT`, `FROM`, `WHERE`, and `ORDER BY`), checks their validity, generates tokens and parse trees, and performs schema validation.

### Q5. What are the classical phases of a compiler?
**Answer:**
1. Lexical Analysis (Scanning)
2. Syntax Analysis (Parsing)
3. Semantic Analysis (Type & Scope Checking)
4. Intermediate Code Generation
5. Code Optimization
6. Target Code Generation

### Q6. What is Lexical Analysis?
**Answer:** Lexical analysis is the initial phase of a compiler. It reads the raw character stream of the source code from left to right and converts it into a sequence of meaningful minimal units called tokens, while stripping whitespace and comments.

### Q7. What is a Token?
**Answer:** A token is an abstract grammatical category returned by the lexer, consisting of a token type and an optional value (e.g., `KEYWORD`, `IDENTIFIER`, `NUMBER`, `OPERATOR`).

### Q8. What is a Lexeme?
**Answer:** A lexeme is the concrete character sequence in the source code that matches the pattern for a token. For example, `students` is the lexeme for token type `IDENTIFIER`.

### Q9. What is a Pattern in lexical analysis?
**Answer:** A pattern is the descriptive rule (usually specified via regular expressions) that defines which character sequences qualify as a particular token type.

### Q10. What is Syntax Analysis?
**Answer:** Syntax analysis (parsing) is the second phase of a compiler. It takes the token stream from the lexer and verifies whether the tokens conform to the structural rules defined by a Context-Free Grammar.

### Q11. What is a Context-Free Grammar (CFG)?
**Answer:** A CFG is a 4-tuple $G = (V, \Sigma, R, S)$ where:
- $V$ is a set of non-terminal symbols.
- $\Sigma$ is a set of terminal symbols (tokens).
- $R$ is a set of production rules of the form $A \to \alpha$.
- $S$ is the designated start symbol.

### Q12. What is Left Recursion in a grammar?
**Answer:** A grammar rule is left-recursive if a non-terminal $A$ derives a sentential form that begins with $A$ itself:
$$A \longrightarrow A\alpha \mid \beta$$

### Q13. Why is left recursion problematic for top-down parsers?
**Answer:** In top-down predictive parsers (like Recursive Descent), each non-terminal is mapped to a function. If $A$ immediately calls itself as its first action without consuming any token, it causes an infinite recursion loop, resulting in a stack overflow.

### Q14. How is immediate left recursion eliminated?
**Answer:** Using the standard algebraic transformation:
$$A \longrightarrow A\alpha \mid \beta \quad \implies \quad A \longrightarrow \beta A', \quad A' \longrightarrow \alpha A' \mid \varepsilon$$
This converts left recursion into right recursion.

### Q15. What is a Recursive Descent Parser?
**Answer:** A Recursive Descent Parser is a top-down parser where each non-terminal symbol in the grammar is implemented as a function in code. The execution flow mirrors the grammar productions directly through recursive or iterative function calls.

### Q16. What does $LL(1)$ stand for?
**Answer:**
- First **L**: Left-to-right scanning of the input.
- Second **L**: Produces a Leftmost derivation.
- **(1)**: Uses 1 token of lookahead to make deterministic parsing decisions without backtracking.

### Q17. What is a FIRST set?
**Answer:** $\text{FIRST}(\alpha)$ is the set of all terminal symbols that can appear as the first symbol of a string derived from $\alpha$. If $\alpha$ can derive $\varepsilon$, then $\varepsilon \in \text{FIRST}(\alpha)$.

### Q18. What is a FOLLOW set?
**Answer:** $\text{FOLLOW}(A)$ is the set of terminal symbols that can appear immediately to the right of non-terminal $A$ in some valid sentential form during derivation.

### Q19. What is a Parse Tree (Concrete Syntax Tree)?
**Answer:** A Parse Tree (CST) is a complete tree representation of a grammatical derivation. Every internal node is a non-terminal, and every leaf node is a terminal symbol (including punctuation like commas and semicolons).

### Q20. What is an Abstract Syntax Tree (AST)?
**Answer:** An AST is a condensed hierarchical tree that represents only the essential syntactic and semantic structure of the program, omitting redundant punctuation tokens like commas, semicolons, and structural grouping tokens.

### Q21. What is the difference between a Parse Tree and an AST?
**Answer:** A Parse Tree retains every grammar production rule and syntactic token (like commas and semicolons) used during parsing. An AST contains only operative nodes (expressions, conditions, identifiers) needed for semantic analysis and execution.

### Q22. How is the Parse Tree dynamically generated in our project?
**Answer:** In `compiler/parser.py`, as each grammar method executes, it instantiates a `ParseTreeNode`. When child non-terminals or tokens are matched, they are dynamically appended as child nodes (`add_child()`), building a genuine tree reflecting the exact query entered.

### Q23. What is Semantic Analysis?
**Answer:** Semantic analysis is the compiler phase that checks whether the syntactically valid parse tree makes logical sense with respect to scope, declarations, and type compatibility against a schema or symbol table.

### Q24. What is a Symbol Table?
**Answer:** A Symbol Table is a centralized data structure used by the compiler to store information about identifiers—such as table names, column names, data types, nullability, and primary keys.

### Q25. What is the difference between Syntax Analysis and Semantic Analysis?
**Answer:** Syntax analysis checks the grammatical structure of the statement (e.g., does `SELECT` have a `FROM` clause?). Semantic analysis checks meaning and contextual validity (e.g., does the table actually exist in the database? Are the column data types compatible?).

### Q26. What are Lexical Errors? Give an example.
**Answer:** Lexical errors occur when the scanner encounters characters that do not conform to any token pattern.
*Example:* `SELECT name FROM students @;` (the symbol `@` is illegal in this SQL subset).

### Q27. What are Syntax Errors? Give an example.
**Answer:** Syntax errors occur when the token sequence violates the CFG rules.
*Example:* `SELECT FROM students;` (missing column list after `SELECT`).

### Q28. What are Semantic Errors? Give an example.
**Answer:** Semantic errors occur when a grammatically correct query references nonexistent schema items or incompatible types.
*Example:* `SELECT salary FROM students;` (the column `salary` does not exist in table `students`).

### Q29. Why are SQL keywords case-insensitive?
**Answer:** Standard SQL is case-insensitive by design to improve readability and user convenience. Our lexer handles this by normalizing scanned keyword lexemes to uppercase before looking them up in the keyword dictionary.

### Q30. How does the compiler handle string literals and escape sequences?
**Answer:** The lexer detects strings enclosed in single quotes `'...'`. If a backslash `\` is encountered, it interprets valid escape characters (`\'`, `\"`, `\\`, `\n`, `\t`). If a string is not closed before newline or EOF, it raises a `LexicalError`.

### Q31. How does the SELECT clause work in our compiler?
**Answer:** The parser matches `SELECT`, checks for an optional `DISTINCT` keyword, and then parses either a wildcard `*` or a comma-separated list of column identifiers.

### Q32. How does the FROM clause work?
**Answer:** The parser matches `FROM`, consumes a table identifier, and checks for an optional table alias identifier (e.g., `FROM students s`).

### Q33. How does the WHERE clause work?
**Answer:** The parser matches `WHERE` and initiates condition parsing. It evaluates expressions according to operator precedence: `NOT` has highest precedence, followed by `AND`, followed by `OR`. Parentheses `(...)` allow custom grouping.

### Q34. How does the ORDER BY clause work?
**Answer:** The parser matches `ORDER BY`, followed by one or more comma-separated column names. Each column can optionally specify `ASC` or `DESC` (defaulting to `ASC` if omitted).

### Q35. How is SQL clause ordering validated?
**Answer:** The `parse()` method enforces a strict sequence: `SELECT` $\to$ `FROM` $\to$ `WHERE` $\to$ `ORDER BY`. If a `WHERE` token appears after `ORDER BY`, an explicit `SyntaxError` is immediately raised.

### Q36. What data types are supported in the mock schema?
**Answer:** The mock schema in `schema/sample_schema.json` supports `INT`, `FLOAT`, and `VARCHAR`.

### Q37. What type compatibility checks does the Semantic Analyzer perform?
**Answer:** It ensures that numeric columns (`INT`, `FLOAT`) are compared against numbers, and text columns (`VARCHAR`) are compared against string literals. Comparing a number to a string (e.g. `age = 'twenty'`) raises a `SemanticError`.

### Q38. How does the compiler provide "Did you mean?" suggestions?
**Answer:** In `compiler/symbol_table.py`, if a table or column name lookup fails, Python's `difflib.get_close_matches` algorithm compares the misspelled identifier against available schema names and suggests the closest match.

### Q39. What technology stack was chosen and why?
**Answer:**
- **Python 3:** Expressive data structures, clean object-oriented architecture, ideal for educational compiler demonstration.
- **Flask:** Lightweight, zero-boilerplate Python web framework for serving the compiler REST API.
- **HTML5/CSS3/Vanilla JS:** Clean, responsive dark-mode developer interface without bulky front-end dependencies.
- **Pytest:** High-speed automated unit and integration testing.

### Q40. Why did we build a hand-written Recursive Descent Parser instead of using Yacc/Bison/ANTLR?
**Answer:** A hand-written parser provides total control over error reporting, allows creating customized diagnostic suggestions with exact line/column offsets, and demonstrates genuine algorithmic understanding of top-down parsing for an undergraduate compiler project.

### Q41. How does our parser avoid backtracking?
**Answer:** Because our transformed grammar satisfies the $LL(1)$ condition, the parser never needs to backtrack. By looking ahead by just 1 token (`_peek()`), it can deterministically choose the correct grammar production.

### Q42. What happens if a query has a trailing semicolon or extra tokens?
**Answer:** The semicolon is recognized as an optional statement terminator. Any extra tokens appearing after the semicolon (or after the query end) trigger a `SyntaxError: Unexpected token found after query termination`.

### Q43. What is the role of `compiler/compiler.py`?
**Answer:** It is the master driver/facade that coordinates the entire pipeline: calls the Lexer, passes tokens to the Parser, forwards the AST to the Semantic Analyzer, logs execution time in milliseconds, and packages results into a `CompilationResult` object.

### Q44. How does the Web UI communicate with the compiler?
**Answer:** When the user clicks "Compile Query" (or presses `Ctrl+Enter`), the JavaScript controller makes an asynchronous `POST` request to `/api/compile` with the query string. The Flask backend runs the compiler and returns the complete result as JSON.

### Q45. What are the key limitations of this project?
**Answer:** It does not support DDL/DML (`INSERT`, `CREATE`), multi-table `JOIN` operations, aggregate functions (`COUNT`, `SUM`), `GROUP BY`, or physical disk execution. It is focused strictly as a front-end compiler.

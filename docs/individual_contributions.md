# Team Members & Individual Contribution Matrix

## 1. Project Identification
- **Subject:** Compiler Design (CS501 / CS502)
- **Degree:** B.Tech Computer Science & Engineering (5th Semester)
- **Project Topic:** Topic 10 – Mini SQL Compiler
- **Academic Year:** 2026

---

## 2. Team Task Allocation Matrix

| Team Member | Module Assigned | Key Responsibilities & Deliverables | Source Code Files |
|---|---|---|---|
| **Member 1** *(Lead)*<br>`[Student Name 1 - Roll No]` | **Lexical Analyzer (Lexer)** | • Finite-state scanner implementation<br>• Token classification (`tokens.py`)<br>• Whitespace, comment, and escape handling<br>• Lexical error detection with line/col tracking | `compiler/lexer.py`<br>`compiler/tokens.py`<br>`tests/test_lexer.py` |
| **Member 2**<br>`[Student Name 2 - Roll No]` | **Syntax Analyzer (Parser)** | • Context-Free Grammar formalization<br>• Left-recursion elimination<br>• FIRST and FOLLOW sets derivation<br>• Recursive descent parsing logic and clause order validation | `compiler/grammar.py`<br>`compiler/parser.py`<br>`grammar/*.md`<br>`tests/test_parser.py` |
| **Member 3**<br>`[Student Name 3 - Roll No]` | **Parse Tree & AST Engine** | • Concrete Syntax Tree (`ParseTreeNode`) hierarchy<br>• Abstract Syntax Tree (`ast_nodes.py`) data structures<br>• Tree serializers (Unicode box characters & ASCII)<br>• JSON tree serialization for Web UI | `compiler/parse_tree.py`<br>`compiler/ast_nodes.py`<br>`tests/test_parse_tree.py` |
| **Member 4**<br>`[Student Name 4 - Roll No]` | **Semantic Analyzer & Symbol Table** | • Schema catalog management (`symbol_table.py`)<br>• Mock database schema (`sample_schema.json`)<br>• Table/column existence and type compatibility checking<br>• Fuzzy typo suggestion algorithm | `compiler/symbol_table.py`<br>`compiler/semantic_analyzer.py`<br>`schema/sample_schema.json`<br>`tests/test_semantic.py` |
| **Member 5**<br>`[Student Name 5 - Roll No]` | **Full-Stack GUI & Integration** | • Flask backend application (`app.py`)<br>• Master compiler coordinator (`compiler.py`)<br>• Responsive dark-mode Web UI (HTML/CSS/JS)<br>• End-to-end integration testing & documentation | `app.py`<br>`compiler/compiler.py`<br>`frontend/**/*`<br>`tests/test_compiler.py` |

---

## 3. Contribution Verification Log

All team members participated in code reviews, automated testing sessions, and repository pull requests:
- **Member 1:** Verified 10 lexical unit test cases and escape handling.
- **Member 2:** Verified 18 syntax unit test cases and operator precedence.
- **Member 3:** Verified tree serialization and AST node hierarchy.
- **Member 4:** Verified schema type checking and fuzzy table/column lookups.
- **Member 5:** Built the interactive web interface and verified all 60 automated tests.

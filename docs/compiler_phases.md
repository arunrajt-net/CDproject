# Compiler Phases

## 1. Classical Compiler Phases vs. Mini SQL Front-End
A full end-to-end compiler translates high-level source code into low-level machine instructions or bytecode across two major divisions:
1. **Front-End (Analysis):** Lexical Analysis, Syntax Analysis, Semantic Analysis, and Intermediate Representation (IR) generation.
2. **Back-End (Synthesis):** Optimization, Code Generation, and Target Machine Instruction Binding.

The **Mini SQL Compiler** is purposefully an educational **Front-End Compiler**. It implements all four classical analysis phases with extreme precision.

---

## 2. Phase-by-Phase Breakdown

### Phase 1: Lexical Analysis (Scanning)
- **Role:** Converts an unformatted stream of raw source characters into discrete, categorized tokens.
- **Input:** Raw SQL string (e.g. `SELECT name FROM students;`).
- **Output:** Stream of `Token` objects (e.g. `[KEYWORD('SELECT'), IDENTIFIER('name'), KEYWORD('FROM'), IDENTIFIER('students'), SEMICOLON(';')]`).
- **Theory:** Implemented via Deterministic Finite State scanning with position markers (`line`, `column`).

### Phase 2: Syntax Analysis (Parsing)
- **Role:** Verifies whether the sequence of tokens forms a grammatically legal sentence according to the Context-Free Grammar.
- **Input:** Stream of tokens from Lexer.
- **Output:** Concrete Syntax Tree (Parse Tree) and Abstract Syntax Tree (AST).
- **Theory:** Predictive Top-Down Recursive Descent Parsing without backtracking ($LL(1)$).

### Phase 3: Semantic Analysis (Contextual Checking)
- **Role:** Checks static semantic rules that cannot be captured by context-free grammars alone (e.g., scoping, declaration before use, and type matching).
- **Input:** Abstract Syntax Tree (AST) + Database Schema Catalog (Symbol Table).
- **Output:** Validated AST + Verification Checklist.
- **Theory:** Attribute grammars and symbol table lookups.

### Phase 4: Symbol Table Management
- **Role:** Serves as the central repository for identifiers, recording table declarations, column signatures, data types, nullability, and primary key status.
- **Input:** Database schema configuration (`schema/sample_schema.json`).
- **Output:** Fast dictionary access for semantic lookups and fuzzy typo corrections.

"""
Flask Backend Web Application for the Mini SQL Compiler.
Provides RESTful APIs for query compilation, schema exploration, and example loading.
"""

import os
from pathlib import Path
from flask import Flask, request, jsonify, render_template
from compiler import MiniSQLCompiler

BASE_DIR = Path(__file__).resolve().parent
SCHEMA_FILE = BASE_DIR / "schema" / "sample_schema.json"

app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "frontend" / "templates"),
    static_folder=str(BASE_DIR / "frontend" / "static")
)

# Instantiate singleton compiler engine
compiler_engine = MiniSQLCompiler(str(SCHEMA_FILE) if SCHEMA_FILE.exists() else None)

EXAMPLE_QUERIES = [
    {
        "id": "val_1",
        "title": "Select All (Wildcard)",
        "category": "valid",
        "query": "SELECT * FROM students;"
    },
    {
        "id": "val_2",
        "title": "Filter with WHERE & Math",
        "category": "valid",
        "query": "SELECT name, age FROM students WHERE age > 18;"
    },
    {
        "id": "val_3",
        "title": "Compound Condition & Sorting",
        "category": "valid",
        "query": "SELECT name, marks FROM students WHERE marks >= 80 AND department = 'CSE' ORDER BY marks DESC;"
    },
    {
        "id": "val_4",
        "title": "DISTINCT & Employees Table",
        "category": "valid",
        "query": "SELECT DISTINCT department FROM employees WHERE salary > 40000.0;"
    },
    {
        "id": "inv_1",
        "title": "Syntax Error: Missing Columns",
        "category": "invalid",
        "query": "SELECT FROM students;"
    },
    {
        "id": "inv_2",
        "title": "Syntax Error: Missing FROM",
        "category": "invalid",
        "query": "SELECT name students;"
    },
    {
        "id": "inv_3",
        "title": "Semantic Error: Unknown Column",
        "category": "invalid",
        "query": "SELECT salary FROM students;"
    },
    {
        "id": "inv_4",
        "title": "Semantic Error: Type Mismatch",
        "category": "invalid",
        "query": "SELECT name FROM students WHERE age = 'twenty';"
    },
    {
        "id": "inv_5",
        "title": "Lexical Error: Illegal Symbol",
        "category": "invalid",
        "query": "SELECT name FROM students @;"
    }
]


@app.route("/")
def index():
    """Renders the main web interface."""
    return render_template("index.html")


@app.route("/api/compile", methods=["POST"])
def compile_query():
    """
    Compiles an incoming SQL statement.
    Expects JSON: { "query": "SELECT ... " }
    """
    data = request.get_json(silent=True) or {}
    query_str = data.get("query", "")

    if not query_str or not query_str.strip():
        return jsonify({
            "success": False,
            "errors": [{
                "error_type": "Syntax Error",
                "message": "Query string is empty. Please enter a valid SQL query.",
                "line": 1,
                "column": 1,
                "suggestion": "Start with 'SELECT <columns> FROM <table>'"
            }],
            "phases": {
                "lexical": "SKIPPED",
                "syntax": "FAILED",
                "semantic": "SKIPPED"
            },
            "tokens": [],
            "token_count": 0,
            "parse_tree_text": None,
            "parse_tree_json": None,
            "ast_json": None,
            "ast_text": None,
            "semantic_analysis": {},
            "symbol_table": compiler_engine.symbol_table.get_all_entries(),
            "duration_ms": 0.0
        }), 200

    result = compiler_engine.compile(query_str)
    return jsonify(result.to_dict()), 200


@app.route("/api/schema", methods=["GET"])
def get_schema():
    """Returns the loaded schema and symbol table metadata."""
    return jsonify({
        "tables": {name: [col.to_dict() for col in tbl.columns.values()] for name, tbl in compiler_engine.symbol_table.tables.items()},
        "all_symbols": compiler_engine.symbol_table.get_all_entries()
    }), 200


@app.route("/api/examples", methods=["GET"])
def get_examples():
    """Returns catalog of pre-configured valid and invalid demonstration queries."""
    return jsonify(EXAMPLE_QUERIES), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    print(f"[*] Starting Mini SQL Compiler Web Server on http://127.0.0.1:{port}")
    app.run(host="0.0.0.0", port=port, debug=False)

"""
Symbol Table and Schema Management for the Mini SQL Compiler.
Stores database schema metadata (tables, columns, data types) used by the Semantic Analyzer.
"""

import json
import difflib
from pathlib import Path
from dataclasses import dataclass
from typing import Dict, List, Optional, Any


@dataclass
class ColumnSymbol:
    """Represents a column entry in the symbol table."""
    name: str
    data_type: str
    table_name: str
    nullable: bool = True
    primary_key: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "table_name": self.table_name,
            "column_name": self.name,
            "data_type": self.data_type,
            "nullable": self.nullable,
            "primary_key": self.primary_key,
        }


@dataclass
class TableSymbol:
    """Represents a table containing column metadata."""
    name: str
    columns: Dict[str, ColumnSymbol]
    description: str = ""

    def get_column(self, col_name: str) -> Optional[ColumnSymbol]:
        # Case-insensitive column search
        for name, col in self.columns.items():
            if name.lower() == col_name.lower():
                return col
        return None


class SymbolTable:
    """
    Compiler Symbol Table holding schema definitions.
    Provides fast lookup, case-insensitive comparison, and fuzzy matching for error suggestions.
    """

    def __init__(self, schema_data: Optional[Dict[str, Any]] = None):
        self.tables: Dict[str, TableSymbol] = {}
        if schema_data:
            self.load_from_dict(schema_data)

    @classmethod
    def load_from_file(cls, schema_path: str) -> "SymbolTable":
        path = Path(schema_path)
        if not path.exists():
            raise FileNotFoundError(f"Schema file not found at: {schema_path}")
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls(data)

    def load_from_dict(self, schema_dict: Dict[str, Any]) -> None:
        self.tables.clear()
        for tbl_name, tbl_info in schema_dict.items():
            cols: Dict[str, ColumnSymbol] = {}
            col_definitions = tbl_info.get("columns", {})
            for c_name, c_info in col_definitions.items():
                cols[c_name] = ColumnSymbol(
                    name=c_name,
                    data_type=c_info.get("type", "VARCHAR").upper(),
                    table_name=tbl_name,
                    nullable=c_info.get("nullable", True),
                    primary_key=c_info.get("primary_key", False),
                )
            self.tables[tbl_name] = TableSymbol(
                name=tbl_name,
                columns=cols,
                description=tbl_info.get("description", ""),
            )

    def get_table(self, table_name: str) -> Optional[TableSymbol]:
        for name, tbl in self.tables.items():
            if name.lower() == table_name.lower():
                return tbl
        return None

    def has_table(self, table_name: str) -> bool:
        return self.get_table(table_name) is not None

    def get_column(self, table_name: str, column_name: str) -> Optional[ColumnSymbol]:
        tbl = self.get_table(table_name)
        if not tbl:
            return None
        return tbl.get_column(column_name)

    def has_column(self, table_name: str, column_name: str) -> bool:
        return self.get_column(table_name, column_name) is not None

    def get_column_type(self, table_name: str, column_name: str) -> Optional[str]:
        col = self.get_column(table_name, column_name)
        return col.data_type if col else None

    def suggest_table(self, table_name: str) -> Optional[str]:
        available = list(self.tables.keys())
        matches = difflib.get_close_matches(table_name, available, n=1, cutoff=0.5)
        return matches[0] if matches else None

    def suggest_column(self, table_name: str, column_name: str) -> Optional[str]:
        tbl = self.get_table(table_name)
        if not tbl:
            return None
        available = list(tbl.columns.keys())
        matches = difflib.get_close_matches(column_name, available, n=1, cutoff=0.5)
        return matches[0] if matches else None

    def get_all_entries(self) -> List[Dict[str, Any]]:
        entries = []
        for tbl_name, tbl in self.tables.items():
            for col_name, col in tbl.columns.items():
                entries.append(col.to_dict())
        return entries

"""
Parse Tree (Concrete Syntax Tree) representation for the Mini SQL Compiler.
Generates hierarchical nested trees with text and JSON serialization.
"""

from typing import List, Optional, Dict, Any


class ParseTreeNode:
    """
    Represents a node in the Concrete Syntax Tree (Parse Tree).
    Contains non-terminal or terminal label, optional token/lexeme value,
    and an ordered list of children.
    """

    def __init__(
        self,
        name: str,
        value: Optional[str] = None,
        line: Optional[int] = None,
        column: Optional[int] = None
    ):
        self.name: str = name
        self.value: Optional[str] = value
        self.line: Optional[int] = line
        self.column: Optional[int] = column
        self.children: List["ParseTreeNode"] = []

    def add_child(self, child: "ParseTreeNode") -> "ParseTreeNode":
        if child is not None:
            self.children.append(child)
        return child

    def add_token_child(
        self,
        name: str,
        value: str,
        line: Optional[int] = None,
        column: Optional[int] = None
    ) -> "ParseTreeNode":
        node = ParseTreeNode(name=name, value=value, line=line, column=column)
        self.children.append(node)
        return node

    def to_dict(self) -> Dict[str, Any]:
        """Serializes the tree into a JSON-compatible dictionary."""
        node_dict: Dict[str, Any] = {
            "name": self.name,
        }
        if self.value is not None:
            node_dict["value"] = self.value
        if self.line is not None:
            node_dict["line"] = self.line
        if self.column is not None:
            node_dict["column"] = self.column
        if self.children:
            node_dict["children"] = [child.to_dict() for child in self.children]
        return node_dict

    def to_text_tree(self, prefix: str = "", is_last: bool = True, use_ascii: bool = False) -> str:
        r"""
        Renders the parse tree into a human-readable hierarchical tree string.
        Supports both modern Unicode box-drawing characters (├──, └──) and standard ASCII (+--, \--).
        """
        display_label = self.name
        if self.value is not None:
            display_label = f"{self.name} ('{self.value}')"

        c_last = "\\-- " if use_ascii else "└── "
        c_mid = "+-- " if use_ascii else "├── "
        p_pipe = "|   " if use_ascii else "│   "

        if not prefix:  # Root node
            result = display_label + "\n"
        else:
            connector = c_last if is_last else c_mid
            result = prefix + connector + display_label + "\n"

        child_prefix = prefix + ("    " if is_last else p_pipe)
        count = len(self.children)
        for i, child in enumerate(self.children):
            result += child.to_text_tree(child_prefix, i == count - 1, use_ascii=use_ascii)

        return result

    def __repr__(self) -> str:
        val = f"='{self.value}'" if self.value is not None else ""
        return f"ParseTreeNode({self.name}{val}, children={len(self.children)})"

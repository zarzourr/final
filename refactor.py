import ast
import os

log = []

def has_docstring(func_node):
    return ast.get_docstring(func_node) is not None

def modify_file(path):
    with open(path, 'r') as f:
        code = f.read()

    tree = ast.parse(code)
    new_lines = code.split('\n')
    modified = False

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if not has_docstring(node):
                line_no = node.body[0].lineno - 1
                indent = ' ' * node.col_offset
                new_lines.insert(line_no, f'{indent}"""Auto-generated docstring."""')
                log.append(f"[Docstring added] {path}::{node.name}")
                modified = True

            if len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
                line_no = node.lineno - 1
                new_lines.insert(line_no, f"# TODO: implement {node.name}")
                log.append(f"[TODO comment] {path}::{node.name}")
                modified = True

    if modified:
        with open(path, 'w') as f:
            f.write('\n'.join(new_lines))

def refactor_all():
    for root, _, files in os.walk("."):
        for file in files:
            if file.endswith(".py") and file not in ["refactor.py"]:
                modify_file(os.path.join(root, file))

    with open("refactor_log.txt", "w") as logf:
        logf.write("\n".join(log) or "No changes made.")

if __name__ == "__main__":
    refactor_all()

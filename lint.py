#!/usr/bin/env python3
"""
lint.py - Enforces layer dependency rules for the puzzle game.

Rules enforced:
1. Every source file lives inside a layer directory
2. Imports respect the forward dependency direction
3. No file exceeds 300 lines

Layer dependency chain: types → config → repo → service → runtime → ui
Cross-cutting providers may import from: types, config, utils, providers
Utils is leaf - only imports itself
"""

import ast
import os
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple


# Define layer order (for import validation)
LAYER_ORDER = ["utils", "providers", "config", "types", "repo", "service", "runtime", "ui"]

# Define valid import sources for each layer
VALID_IMPORTS = {
    "types": {"types"},
    "config": {"types", "config"},
    "repo": {"types", "config", "repo"},
    "service": {"types", "config", "repo", "providers", "service"},
    "runtime": {"types", "config", "repo", "service", "providers", "runtime"},
    "ui": {"types", "config", "service", "runtime", "providers", "ui"},
    "providers": {"types", "config", "utils", "providers"},
    "utils": {"utils"},
}

# Expected layers
EXPECTED_LAYERS = set(LAYER_ORDER)

# Max lines per file
MAX_LINES = 300


class LintError:
    """Represents a linting error."""
    
    def __init__(self, file_path: str, line: int, message: str):
        self.file_path = file_path
        self.line = line
        self.message = message
    
    def __str__(self) -> str:
        return f"{self.file_path}:{self.line}: {self.message}"


def get_file_layer(file_path: Path) -> str | None:
    """Get the layer directory a file belongs to."""
    try:
        rel_path = file_path.relative_to(Path("src"))
        parts = rel_path.parts
        if len(parts) > 0:
            layer = parts[0]
            if layer in EXPECTED_LAYERS:
                return layer
    except ValueError:
        pass
    return None


def get_imports(file_path: Path) -> List[Tuple[str, int]]:
    """Extract all import statements from a Python file."""
    imports = []
    try:
        with open(file_path, "r") as f:
            content = f.read()
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.append((alias.name, node.lineno))
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.append((node.module, node.lineno))
    except SyntaxError:
        pass
    return imports


def get_module_base_name(module_name: str) -> str:
    """Get the base module name (first part of dotted path)."""
    return module_name.split(".")[0]


def validate_imports(file_path: Path, layer: str) -> List[LintError]:
    """Validate that imports respect layer dependency rules."""
    errors = []
    valid_sources = VALID_IMPORTS.get(layer, set())
    
    imports = get_imports(file_path)
    
    for module_name, line_num in imports:
        base_name = get_module_base_name(module_name)
        
        # Check if the imported module is in a valid layer
        # For relative imports or internal modules, check the layer
        imported_layer = None
        for expected_layer in EXPECTED_LAYERS:
            if base_name == expected_layer or base_name.startswith(expected_layer + "."):
                imported_layer = expected_layer
                break
        
        # If it's an internal layer import, validate it
        if imported_layer and imported_layer not in valid_sources:
            errors.append(LintError(
                str(file_path),
                line_num,
                f"Import '{module_name}' from layer '{imported_layer}' is not allowed. "
                f"Layer '{layer}' may only import from: {', '.join(sorted(valid_sources))}"
            ))
    
    return errors


def validate_line_count(file_path: Path) -> List[LintError]:
    """Validate that the file doesn't exceed MAX_LINES."""
    errors = []
    try:
        with open(file_path, "r") as f:
            line_count = sum(1 for _ in f)
        
        if line_count > MAX_LINES:
            errors.append(LintError(
                str(file_path),
                1,
                f"File exceeds {MAX_LINES} lines ({line_count} lines). "
                f"Split into smaller modules within the same layer."
            ))
    except Exception:
        pass
    return errors


def collect_python_files(src_dir: Path) -> List[Path]:
    """Collect all Python files under src/, excluding tests and __pycache__."""
    python_files = []
    for root, dirs, files in os.walk(src_dir):
        # Skip tests and __pycache__
        if "tests" in root or "__pycache__" in root:
            continue
        dirs[:] = [d for d in dirs if d not in {"tests", "__pycache__"}]
        
        for file in files:
            if file.endswith(".py"):
                python_files.append(Path(root) / file)
    
    return python_files


def run_lint() -> List[LintError]:
    """Run all lint checks and return errors."""
    errors = []
    src_dir = Path("src")
    
    if not src_dir.exists():
        return [LintError("lint.py", 1, "src/ directory not found")]
    
    python_files = collect_python_files(src_dir)
    
    for file_path in python_files:
        layer = get_file_layer(file_path)
        
        # Rule 1: Every file must be in a layer directory
        if layer is None:
            errors.append(LintError(
                str(file_path),
                1,
                "File is not inside a layer directory under src/"
            ))
            continue
        
        # Rule 2: Validate imports respect layer dependencies
        errors.extend(validate_imports(file_path, layer))
        
        # Rule 3: No file exceeds MAX_LINES
        errors.extend(validate_line_count(file_path))
    
    return errors


def main() -> int:
    """Main entry point."""
    errors = run_lint()
    
    if errors:
        print("Lint failed! Errors found:")
        for error in errors:
            print(f"  {error}")
        return 1
    else:
        print("Lint passed!")
        return 0


if __name__ == "__main__":
    sys.exit(main())

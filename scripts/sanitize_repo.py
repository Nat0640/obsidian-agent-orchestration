#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sanitization Script for Agent Harness Release
Removes personal and system-specific data from files in dist/ folder before public release.

Applies lessons: [L-20] UnicodeEncodeError prevention on Windows Python Console
"""

import os
import sys
import io
import re

# [L-20] Fix: Handle Unicode encoding for Windows console
if sys.stdout.encoding != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(SCRIPT_DIR)

# Dynamically target 'dist/' if it exists, otherwise fall back to repository root (e.g. on GitHub CI)
DIST_DIR = os.path.join(PROJECT_DIR, 'dist')
if not os.path.exists(DIST_DIR):
    DIST_DIR = PROJECT_DIR

# Replacement patterns - ordered by specificity to prevent partial matches
REPLACEMENTS = [
    # Full paths first (most specific)
    (r'D:\\obsidian\\para', './workspace'),
    (r'D:/obsidian/para', './workspace'),
    # Email addresses
    (r'nattapol\.s0640@gmail\.com', 'developer@example.com'),
    # Names (after paths to avoid partial replacement issues)
    (r'\bNattapol\b', 'AI Developer'),
]

# Text file extensions to process
TEXT_EXTENSIONS = {'.md', '.txt', '.svg', '.json', '.py', '.yml', '.yaml', '.xml', '.html', '.css', '.js', '.ts', '.csv'}

# Binary file extensions to skip
BINARY_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.gif', '.ico', '.pdf', '.zip', '.exe', '.dll', '.bin'}


def is_text_file(filepath):
    """Check if file is a text file based on extension."""
    ext = os.path.splitext(filepath)[1].lower()
    if ext in BINARY_EXTENSIONS:
        return False
    if ext in TEXT_EXTENSIONS:
        return True
    # Try to detect by reading first bytes
    try:
        with open(filepath, 'rb') as f:
            chunk = f.read(8192)
        chunk.decode('utf-8')
        return True
    except (UnicodeDecodeError, FileNotFoundError):
        return False


def sanitize_file(filepath):
    """Read, sanitize, and write back a text file if it contains sensitive data."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except (UnicodeDecodeError, FileNotFoundError) as e:
        print(f"[WARN] Could not read {filepath}: {e}")
        return False

    original_content = content
    for pattern, replacement in REPLACEMENTS:
        content = re.sub(pattern, replacement, content)

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"[SANITIZED] {filepath}")
        return True
    return False


def create_gitignore():
    """Create .gitignore in dist/ directory with standard patterns."""
    gitignore_path = os.path.join(DIST_DIR, '.gitignore')
    gitignore_content = """# Personal / System Data Protection
# Never commit sensitive information

# Environment and configuration
.env
.env.local
.env.*.local
*.local
config.local.*
secrets.*
secrets/

# Obsidian-specific patterns
.obsidian/
*.cache/

# Personal paths (Windows patterns)
D:\\\\*
D:/*

# Original workspace references (sanitized to ./workspace)
/workspace-backup/

# Build and temp files
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# IDE and editor
.vscode/
.idea/
*.swp
*.swo
*~

# OS files
.DS_Store
Thumbs.db
Desktop.ini

# Logs and sensitive output
logs/
*.log
*.log.*

# Node modules (if any JS examples added)
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
"""
    with open(gitignore_path, 'w', encoding='utf-8') as f:
        f.write(gitignore_content)
    print(f"[CREATED] {gitignore_path}")
    return True


def main():
    """Main entry point for sanitization."""
    print(f"[INFO] Starting sanitization of: {DIST_DIR}")

    if not os.path.exists(DIST_DIR):
        print(f"[ERROR] Dist directory does not exist: {DIST_DIR}")
        return 1

    # Process all text files in dist/
    sanitized_count = 0
    skipped_count = 0

    for root, dirs, files in os.walk(DIST_DIR):
        # Skip .git directory if it exists
        dirs[:] = [d for d in dirs if not d.startswith('.git')]

        for filename in files:
            filepath = os.path.join(root, filename)

            # Skip .gitignore and sanitize_repo.py itself
            if filename in ('.gitignore', 'sanitize_repo.py'):
                continue

            if is_text_file(filepath):
                if sanitize_file(filepath):
                    sanitized_count += 1
            else:
                skipped_count += 1
                print(f"[SKIPPED] {filepath} (binary file)")

    # Create .gitignore
    create_gitignore()

    print(f"[INFO] Sanitization complete: {sanitized_count} files sanitized, {skipped_count} binary files skipped")

    # Final verification
    print(f"[INFO] Verifying no sensitive data remains...")
    verify_patterns = [
        r'D:\\obsidian\\para',
        r'D:/obsidian/para',
        r'nattapol\.s0640@gmail\.com',
        r'\\bNattapol\\b'
    ]

    violations = []
    for root, dirs, files in os.walk(DIST_DIR):
        dirs[:] = [d for d in dirs if not d.startswith('.git')]
        for filename in files:
            if filename == 'sanitize_repo.py':
                continue
            filepath = os.path.join(root, filename)
            if is_text_file(filepath):
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    for pattern in verify_patterns:
                        if re.search(pattern, content):
                            violations.append(filepath)
                            print(f"[VIOLATION] Found sensitive data in: {filepath}")
                except (UnicodeDecodeError, FileNotFoundError):
                    pass

    if violations:
        print(f"[ERROR] {len(violations)} files still contain sensitive data!")
        return 1

    print(f"[SUCCESS] All files sanitized - ready for public release")
    return 0


if __name__ == '__main__':
    sys.exit(main())
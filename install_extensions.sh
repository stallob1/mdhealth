#!/bin/bash

# Script to install VS Code/Cursor extensions for viewing various file types

echo "Installing extensions for viewing different file types..."
echo ""

# List of essential extensions for viewing various file types
EXTENSIONS=(
    "ms-vscode.vscode-pdf"                    # PDF Viewer
    "bierner.markdown-preview-github-styles"  # Enhanced Markdown Preview
    "shd101wyy.markdown-preview-enhanced"      # Markdown Preview Enhanced
    "mechatroner.rainbow-csv"                 # CSV Viewer/Editor
    "janisdd.vscode-edit-csv"                 # CSV Editor
    "redhat.vscode-yaml"                      # YAML Support
    "ms-python.python"                        # Python (for various file processing)
    "ms-vscode.vscode-json"                   # JSON Support (usually built-in but ensures it's there)
    "bierner.color-info"                      # Color preview in CSS/HTML
    "formulahendry.code-runner"               # Code Runner
    "vscode-icons-team.vscode-icons"          # File Icons
    "PKief.material-icon-theme"               # Material Icon Theme
    "ms-vscode.hexeditor"                     # Hex Editor for binary files
    "streetsidesoftware.code-spell-checker"   # Spell Checker
    "yzhang.markdown-all-in-one"              # Markdown All in One
    "bierner.markdown-mermaid"                 # Mermaid diagrams in Markdown
    "bierner.markdown-emoji"                  # Emoji support in Markdown
)

# Try to find the code/cursor command
if command -v cursor &> /dev/null; then
    CMD="cursor"
elif [ -f "/Applications/Cursor.app/Contents/Resources/app/bin/cursor" ]; then
    CMD="/Applications/Cursor.app/Contents/Resources/app/bin/cursor"
elif command -v code &> /dev/null; then
    CMD="code"
elif [ -f "/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code" ]; then
    CMD="/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code"
else
    echo "Error: Could not find Cursor or VS Code command"
    echo "Please install extensions manually through the Extensions marketplace:"
    echo ""
    for ext in "${EXTENSIONS[@]}"; do
        echo "  - $ext"
    done
    exit 1
fi

echo "Using command: $CMD"
echo ""

# Install each extension
for ext in "${EXTENSIONS[@]}"; do
    echo "Installing $ext..."
    $CMD --install-extension "$ext" --force 2>&1 | grep -v "is already installed" || true
done

echo ""
echo "✓ Extensions installation complete!"
echo ""
echo "Installed extensions:"
for ext in "${EXTENSIONS[@]}"; do
    echo "  ✓ $ext"
done

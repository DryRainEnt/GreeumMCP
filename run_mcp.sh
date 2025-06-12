#!/bin/bash
# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if venv exists
if [ ! -d "venv/bin" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    pip install -e .
    pip install -r requirements.txt
else
    source venv/bin/activate
fi

# Use relative path for data directory
python -m greeummcp.server --data-dir "$SCRIPT_DIR/data" --transport stdio
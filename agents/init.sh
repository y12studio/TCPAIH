#!/bin/bash

confirm_existence() {
    # make sure uv is installed
    if ! command -v uv &> /dev/null
    then
        echo "uv could not be found, installing..."
        pip install uv
        echo "uv installed successfully."
    else
        echo "uv is already installed."
    fi
}

initialize_repository() {
    git clone https://github.com/y12studio/TCPAIH
    echo "Repository cloned successfully."
    cd TCPAIH/agents/adk1003-team || { echo "Failed to change directory"; exit 1; }
    uv sync
    echo "Sync completed successfully."
}

confirm_existence
initialize_repository
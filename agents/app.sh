#!/bin/bash

confirm_existence() {
    # make sure docker is installed
    if ! command -v docker &> /dev/null
    then
        echo "docker could not be found, installing..."
        apt-get update
        apt-get install -y docker.io
        echo "docker installed successfully."
    else
        echo "docker is already installed."
    fi
}

start() {
    docker compose build
    docker compose up -d
}

stop() {
    docker compose down 
}

confirm_existence
start
#!/bin/bash
echo "bash start."

while true; do
    echo "start parser_for_issue.py..."
    python parser_for_issue.py
    echo "sleep 60seconds..."
    sleep 60
done
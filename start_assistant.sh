#!/bin/bash

echo "======================================================================"
echo "Store Manager AI Assistant - Quick Start"
echo "======================================================================"
echo ""

# Check if Ollama is running
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "⚠️  Ollama is not running!"
    echo ""
    echo "Starting Ollama server..."
    ollama serve > /dev/null 2>&1 &
    sleep 3

    if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo "❌ Failed to start Ollama"
        echo "Please start it manually: ollama serve"
        exit 1
    fi
    echo "✓ Ollama server started"
else
    echo "✓ Ollama is already running"
fi

# Check if we have models
MODEL_COUNT=$(curl -s http://localhost:11434/api/tags | grep -o '"name"' | wc -l)
if [ "$MODEL_COUNT" -eq 0 ]; then
    echo ""
    echo "⚠️  No models found! Pulling llama3.2..."
    ollama pull llama3.2:1b
fi

echo ""
echo "======================================================================"
echo "Starting Store Manager AI Assistant..."
echo "======================================================================"
echo ""

# Run the multi-agent system (latest version)
python3 multi_agent_store_manager.py

# Other versions available:
# python3 store_manager_assistant_enhanced.py  (single agent with enhanced context)
# python3 store_manager_assistant.py  (original version)

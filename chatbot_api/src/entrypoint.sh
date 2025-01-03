#!/bin/bash

echo "Start run chatbot-rag-api service ...."

uvicorn main:app --host 0.0.0.0 --port 8000
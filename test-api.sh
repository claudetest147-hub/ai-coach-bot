#!/bin/bash
# Quick test script for the chatbot API

echo "🧪 Testing AI Coach Bot API..."
echo ""

# Test 1: Health check
echo "1️⃣ Health check..."
curl -s http://localhost:8000/health | jq
echo ""

# Test 2: Ask about pricing
echo "2️⃣ Testing chatbot - Asking about pricing..."
curl -s -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "What is your pricing?"}' | jq
echo ""

# Test 3: Ask about booking
echo "3️⃣ Testing chatbot - Asking about booking..."
curl -s -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "How do I book a call?"}' | jq
echo ""

echo "✅ Tests complete!"

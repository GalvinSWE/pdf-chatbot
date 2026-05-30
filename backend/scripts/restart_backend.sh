#!/bin/bash

echo "🔨 Building backend + worker..."
docker compose build backend worker

echo ""
echo "🚀 Restarting backend + worker..."
docker compose up -d backend worker

echo ""
echo "✅ Done"
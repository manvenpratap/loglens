#!/usr/bin/env bash
set -euo pipefail

# Ensure script runs from project root
cd "$(dirname "$0")"

MSG="${1:-}"
if [ -z "$MSG" ]; then
  echo "❌ Error: Please provide a commit message."
  echo "Usage: ./ship.sh \"<commit message>\""
  exit 1
fi

echo "=================================================="
echo "🚀 LogLens Automated Build & Ship Pipeline"
echo "=================================================="

# Step 1: Build distribution package
echo "📦 1. Building distribution package (dist/index.html)..."
node -e "const fs = require('fs'); fs.mkdirSync('dist', { recursive: true }); fs.copyFileSync('loglens.html', 'dist/index.html');"
echo "   ↳ Synchronized loglens.html -> dist/index.html ($(wc -c < dist/index.html | tr -d ' ') bytes)"

# Step 2: Stage core files and modifications
echo "📋 2. Staging files for commit..."
git add loglens.html dist/index.html .agents/PROJECT_CONTEXT.md .agents/AGENTS.md .gitignore package.json ship.sh tests/
git add -u

# Step 3: Commit
echo "💾 3. Committing changes: \"$MSG\""
git commit -m "$MSG"

# Step 4: Push to origin
echo "⬆️  4. Pushing to origin main..."
git push origin main

echo "=================================================="
echo "✅ Build and Ship Completed Successfully!"
echo "=================================================="

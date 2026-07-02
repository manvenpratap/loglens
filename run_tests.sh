#!/usr/bin/env bash
# =========================================================================
# run_tests.sh — LogLens Regression Test Runner
#
# Usage:
#   ./run_tests.sh             # run all tests
#   ./run_tests.sh smoke       # run smoke subset only
#   ./run_tests.sh tests/test_09_ai_insights.py   # run single module
#   ./run_tests.sh -k focus    # run tests matching keyword
#
# Requirements:
#   pip install -r tests/requirements.txt
#   playwright install chromium
# =========================================================================
set -e

cd "$(dirname "$0")"

ARGS="${@:-tests/}"

echo "╔══════════════════════════════════════════════════════════╗"
echo "║         LogLens Regression Test Suite                   ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""
echo "Target: $ARGS"
echo ""

python3 -m pytest $ARGS -v

EXIT_CODE=$?

echo ""
if [ $EXIT_CODE -eq 0 ]; then
  echo "✅ All tests passed."
else
  echo "❌ Some tests FAILED (exit code $EXIT_CODE)."
fi

exit $EXIT_CODE

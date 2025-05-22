#!/bin/bash

# quality_check.sh - Comprehensive code quality verification script
# This script performs:
# 1. Code style checks and auto-fixes
# 2. Test execution to verify functionality
# 3. Returns a single pass/fail result

echo "===== Running Code Quality Check ====="

# Step 1: Run ruff to check all Python code and fix common issues
echo "Step 1: Running code style checks..."
python -m ruff check . --fix

# Check exit code
if [ $? -ne 0 ]; then
    echo "❌ Code style checks failed. Please fix the issues that couldn't be automatically corrected."
    exit 1
fi
echo "✅ Code style checks passed."

# Step 2: Run tests to ensure everything still works
echo -e "\nStep 2: Running tests..."
python -m pytest

# Check exit code
if [ $? -ne 0 ]; then
    echo "❌ Tests failed! Please fix the failing tests."
    exit 1
fi
echo "✅ All tests passed."

echo -e "\n✨ Code quality check completed successfully! ✨"
exit 0 
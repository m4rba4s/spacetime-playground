#!/usr/bin/env bash
# ============================================================================
# spacetime-playground Test Runner for Linux/Mac
# ============================================================================

echo ""
echo "========================================================================"
echo "  SPACETIME-PLAYGROUND PRE-RELEASE TEST"
echo "========================================================================"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed or not in PATH"
    echo "Please install Python 3.10+ from python.org or your package manager"
    exit 1
fi

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "Found Python $PYTHON_VERSION"
echo ""

echo "Running comprehensive test suite..."
echo ""

# Run the test script
python3 test_before_release.py "$@"
TEST_EXIT_CODE=$?

echo ""
echo "========================================================================"
echo "Test complete!"
echo "========================================================================"
echo ""

exit $TEST_EXIT_CODE

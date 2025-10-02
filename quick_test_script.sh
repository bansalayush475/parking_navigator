#!/bin/bash
# Quick Test Script for Parking Navigator
# Run with: bash quick_test.sh

echo "================================"
echo "🚗 PARKING NAVIGATOR - QUICK TEST"
echo "================================"
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
TESTS_PASSED=0
TESTS_FAILED=0

# Function to print test result
test_result() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ PASS${NC}: $2"
        ((TESTS_PASSED++))
    else
        echo -e "${RED}❌ FAIL${NC}: $2"
        ((TESTS_FAILED++))
    fi
}

echo "📋 Step 1: Checking Python installation..."
if command -v python &> /dev/null; then
    PYTHON_VERSION=$(python --version 2>&1)
    test_result 0 "Python found: $PYTHON_VERSION"
else
    test_result 1 "Python not found"
    exit 1
fi
echo ""

echo "📋 Step 2: Checking required packages..."
python -c "import flask" 2>/dev/null
test_result $? "Flask installed"

python -c "import flask_login" 2>/dev/null
test_result $? "Flask-Login installed"

python -c "import flask_wtf" 2>/dev/null
test_result $? "Flask-WTF installed"

python -c "import flask_sqlalchemy" 2>/dev/null
test_result $? "Flask-SQLAlchemy installed"
echo ""

echo "📋 Step 3: Checking project structure..."
[ -f "app.py" ] && test_result 0 "app.py exists" || test_result 1 "app.py missing"
[ -f "models.py" ] && test_result 0 "models.py exists" || test_result 1 "models.py missing"
[ -f "auth.py" ] && test_result 0 "auth.py exists" || test_result 1 "auth.py missing"
[ -f "admin_routes.py" ] && test_result 0 "admin_routes.py exists" || test_result 1 "admin_routes.py missing"
[ -f "public_routes.py" ] && test_result 0 "public_routes.py exists" || test_result 1 "public_routes.py missing"
[ -f "config.py" ] && test_result 0 "config.py exists" || test_result 1 "config.py missing"
[ -f "forms.py" ] && test_result 0 "forms.py exists" || test_result 1 "forms.py missing"
[ -f "utils.py" ] && test_result 0 "utils.py exists" || test_result 1 "utils.py missing"
[ -f "requirements.txt" ] && test_result 0 "requirements.txt exists" || test_result 1 "requirements.txt missing"
echo ""

echo "📋 Step 4: Checking templates..."
[ -d "templates" ] && test_result 0 "templates/ directory exists" || test_result 1 "templates/ missing"
[ -f "templates/base.html" ] && test_result 0 "base.html exists" || test_result 1 "base.html missing"
[ -f "templates/index.html" ] && test_result 0 "index.html exists" || test_result 1 "index.html missing"
[ -f "templates/login.html" ] && test_result 0 "login.html exists" || test_result 1 "login.html missing"
[ -f "templates/admin.html" ] && test_result 0 "admin.html exists" || test_result 1 "admin.html missing"
echo ""

echo "📋 Step 5: Checking static files..."
[ -d "static" ] && test_result 0 "static/ directory exists" || test_result 1 "static/ missing"
[ -d "static/css" ] && test_result 0 "static/css/ exists" || test_result 1 "static/css/ missing"
[ -d "static/js" ] && test_result 0 "static/js/ exists" || test_result 1 "static/js/ missing"
[ -f "static/css/styles.css" ] && test_result 0 "styles.css exists" || test_result 1 "styles.css missing"
[ -f "static/js/main.js" ] && test_result 0 "main.js exists" || test_result 1 "main.js missing"
echo ""

echo "📋 Step 6: Checking syntax..."
python -m py_compile app.py 2>/dev/null
test_result $? "app.py syntax valid"

python -m py_compile models.py 2>/dev/null
test_result $? "models.py syntax valid"

python -m py_compile admin_routes.py 2>/dev/null
test_result $? "admin_routes.py syntax valid"
echo ""

echo "📋 Step 7: Checking database seeding..."
echo -e "${YELLOW}ℹ️  Running: flask seed${NC}"
flask seed > /dev/null 2>&1
if [ $? -eq 0 ] && [ -f "instance/parking.db" ]; then
    test_result 0 "Database seeded successfully"
else
    test_result 1 "Database seeding failed"
fi
echo ""

echo "================================"
echo "📊 TEST SUMMARY"
echo "================================"
echo -e "${GREEN}Passed: $TESTS_PASSED${NC}"
echo -e "${RED}Failed: $TESTS_FAILED${NC}"
echo ""

if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}🎉 ALL TESTS PASSED!${NC}"
    echo ""
    echo "================================"
    echo "🚀 NEXT STEPS"
    echo "================================"
    echo "1. Start the application:"
    echo "   python app.py"
    echo ""
    echo "2. Open your browser:"
    echo "   http://localhost:5000"
    echo ""
    echo "3. Login with:"
    echo "   Admin: admin@cu.edu / adminpass"
    echo "   User:  user@cu.edu / userpass"
    echo ""
    echo "4. Test the features:"
    echo "   - View parking areas"
    echo "   - Search functionality"
    echo "   - Admin dashboard"
    echo "   - Add/Edit/Delete areas"
    echo ""
    exit 0
else
    echo -e "${RED}❌ SOME TESTS FAILED${NC}"
    echo ""
    echo "Please fix the issues above before running the application."
    echo ""
    echo "Common fixes:"
    echo "1. Install missing packages: pip install -r requirements.txt"
    echo "2. Check file names and locations"
    echo "3. Fix syntax errors in Python files"
    echo ""
    exit 1
fi

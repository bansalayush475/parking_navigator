# 🧪 Complete Testing Guide - Parking Navigator

## 📋 Pre-Testing Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Initialize Database
```bash
# Seed database with sample data
flask seed
```

Expected output:
```
🌱 Starting database seeding...
✅ Created admin user: admin@cu.edu
✅ Created test user: user@cu.edu
✅ Created parking area: North Block with 2 vehicle types
✅ Created parking area: South Wing with 3 vehicle types
✅ Created parking area: East Plaza with 2 vehicle types
✅ Created parking area: West Ground with 3 vehicle types

✅ Database seeding completed successfully!

📊 Summary:
   - Users: 2
   - Parking Areas: 4
   - Vehicle Statuses: 10

🔑 Login Credentials:
   Admin: admin@cu.edu / adminpass
   User:  user@cu.edu / userpass
```

### 3. Start Application
```bash
python app.py
```

Expected output:
```
✅ Database tables created/verified
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://0.0.0.0:5000
```

---

## 🧪 Testing Checklist

### ✅ Phase 1: Public Access (No Login Required)

#### Test 1.1: Home Page
- **URL**: `http://localhost:5000/`
- **Expected**: 
  - ✅ 4 parking areas displayed
  - ✅ Search bar visible
  - ✅ Each area shows "Loading availability..." initially
  - ✅ After 2-3 seconds, real-time data appears
  - ✅ Available spots shown with green/red badges

**Test Steps:**
1. Open browser and navigate to home page
2. Wait for data to load
3. Verify North Block shows cars and bikes
4. Verify South Wing shows cars, bikes, and buses
5. Check that available spots are calculated correctly

#### Test 1.2: Search Functionality
- **Action**: Type in search bar
- **Test Cases**:
  - Search "North" → Should show only North Block
  - Search "Library" → Should show South Wing
  - Search "xyz123" → Should show no results
  - Clear search → Should show all areas again

**Test Steps:**
1. Type "North" in search box
2. Verify only North Block is visible
3. Clear and type "Library"
4. Verify only South Wing appears
5. Clear search and verify all areas return

#### Test 1.3: API Endpoints
- **URL**: `http://localhost:5000/api/status/1`
- **Expected**: JSON response with parking data

**Test Using Browser:**
```
http://localhost:5000/api/status/1
```

**Expected JSON:**
```json
{
  "areaId": 1,
  "areaName": "North Block",
  "location": "Near Main Gate - Building A",
  "statuses": [
    {
      "vehicle_type": "car",
      "capacity": 50,
      "occupied": 35,
      "available": 15
    },
    {
      "vehicle_type": "bike",
      "capacity": 100,
      "occupied": 75,
      "available": 25
    }
  ],
  "available_spots": 40,
  "last_updated": "2025-01-XX..."
}
```

#### Test 1.4: Auto-Refresh
- **Action**: Keep home page open
- **Expected**: Data refreshes every 10 seconds
- **Verification**: Check browser console for fetch requests

---

### ✅ Phase 2: Authentication

#### Test 2.1: User Registration
- **URL**: `http://localhost:5000/auth/register`

**Test Steps:**
1. Click "Register" in navbar
2. Fill form:
   - Email: `test@example.com`
   - Password: `password123`
   - Confirm Password: `password123`
3. Click "Register"
4. **Expected**: 
   - ✅ Success message: "🎉 Registration successful!"
   - ✅ Redirected to login page

**Edge Cases to Test:**
- Empty fields → Should show validation errors
- Password < 6 chars → Should show "Must be at least 6 characters"
- Mismatched passwords → Should show "Passwords must match"
- Duplicate email → Should show "⚠️ Email already registered"

#### Test 2.2: User Login (Regular User)
- **URL**: `http://localhost:5000/auth/login`

**Test Steps:**
1. Email: `user@cu.edu`
2. Password: `userpass`
3. Check "Remember Me"
4. Click "Login"
5. **Expected**:
   - ✅ Success message: "✅ Login successful!"
   - ✅ Redirected to home page
   - ✅ Navbar shows "Logout" (no admin link)

**Edge Cases:**
- Wrong password → Should show "❌ Invalid email or password"
- Wrong email → Should show "❌ Invalid email or password"
- Empty fields → Should show validation errors

#### Test 2.3: Admin Login
- **URL**: `http://localhost:5000/auth/login`

**Test Steps:**
1. Email: `admin@cu.edu`
2. Password: `adminpass`
3. Click "Login"
4. **Expected**:
   - ✅ Success message
   - ✅ Navbar shows "Admin Dashboard" and "Logout"
   - ✅ Redirected to home page OR admin dashboard

#### Test 2.4: Logout
**Test Steps:**
1. While logged in, click "Logout"
2. **Expected**:
   - ✅ Message: "👋 You have been logged out successfully."
   - ✅ Redirected to login page
   - ✅ Navbar shows "Login" and "Register"

#### Test 2.5: Protected Routes
**Test Steps:**
1. Logout completely
2. Try to access: `http://localhost:5000/admin/`
3. **Expected**:
   - ✅ Redirected to login page
   - ✅ Message: "⚠️ Please login to access this page."

---

### ✅ Phase 3: Admin Dashboard

#### Test 3.1: Dashboard Access
- **URL**: `http://localhost:5000/admin/`
- **Prerequisites**: Login as admin

**Test Steps:**
1. Login as admin
2. Click "Admin Dashboard" in navbar
3. **Expected**:
   - ✅ Page loads without errors
   - ✅ Statistics cards show:
     - Total Areas: 4
     - Total Capacity: ~450
     - Occupied: ~280
     - Available: ~170
   - ✅ All 4 parking areas listed with vehicle statuses

#### Test 3.2: Add Parking Area
**Test Steps:**
1. Click "➕ Add New Parking Area"
2. Fill form:
   - Area Name: `Central Plaza`
   - Location: `Near Main Building`
3. Click "Save"
4. **Expected**:
   - ✅ Success message: "✅ Parking area added successfully!"
   - ✅ Redirected to dashboard
   - ✅ New area appears in list
   - ✅ Statistics updated

**Edge Cases:**
- Empty fields → Validation errors
- Duplicate name → "⚠️ Parking area with this name already exists!"

#### Test 3.3: Edit Parking Area
**Test Steps:**
1. Find "North Block"
2. Click "✏️ Edit" button
3. Change:
   - Name: `North Block Updated`
   - Location: `New Location`
4. Click "Save"
5. **Expected**:
   - ✅ Success: "✏️ Parking area updated successfully!"
   - ✅ Changes reflected in dashboard
   - ✅ Last updated timestamp changed

#### Test 3.4: Delete Parking Area
**Test Steps:**
1. Find "Central Plaza" (or any area)
2. Click "🗑️ Delete"
3. **Expected**:
   - ✅ Confirmation dialog appears
   - ✅ After confirming: Success message
   - ✅ Area removed from list
   - ✅ All vehicle statuses also deleted

#### Test 3.5: Add Vehicle Status
**Test Steps:**
1. Find any parking area
2. Click "➕ Add Vehicle Status"
3. Fill form:
   - Vehicle Type: `Bus`
   - Capacity: `20`
   - Occupied: `5`
4. Click "Save"
5. **Expected**:
   - ✅ Success message
   - ✅ New status appears in table
   - ✅ Available shows: 15

**Edge Cases:**
- Occupied > Capacity → "⚠️ Occupied spots cannot exceed capacity!"
- Duplicate vehicle type → "⚠️ Bus status already exists for this area!"

#### Test 3.6: Edit Vehicle Status
**Test Steps:**
1. Find any vehicle status
2. Click "Edit" button
3. Change occupied from 35 to 45
4. Click "Save"
5. **Expected**:
   - ✅ Success message
   - ✅ Occupied updated to 45
   - ✅ Available recalculated automatically

#### Test 3.7: Delete Vehicle Status
**Test Steps:**
1. Find any vehicle status
2. Click "Delete" button
3. Confirm deletion
4. **Expected**:
   - ✅ Confirmation dialog
   - ✅ Status removed
   - ✅ Total available spots updated

---

### ✅ Phase 4: Real-time Updates

#### Test 4.1: Public Page Live Updates
**Test Steps:**
1. Open home page in browser
2. Open another tab with admin dashboard
3. In admin, change occupied spots for a vehicle
4. Switch back to public page
5. **Expected**:
   - ✅ Within 10 seconds, public page updates automatically
   - ✅ No page refresh needed

#### Test 4.2: Multiple Browsers
**Test Steps:**
1. Open home page in Chrome
2. Open home page in Firefox/Edge
3. Update data in admin
4. **Expected**:
   - ✅ Both browsers update independently
   - ✅ Data stays synchronized

---

### ✅ Phase 5: Error Handling

#### Test 5.1: Invalid URLs
**Test Cases:**
- `http://localhost:5000/invalid-page` → Redirects to home
- `http://localhost:5000/admin/edit-area/999` → 404 error handled
- `http://localhost:5000/api/status/999` → Returns error JSON

#### Test 5.2: CSRF Protection
**Test Steps:**
1. Open browser dev tools (F12)
2. Try to submit a form without CSRF token
3. **Expected**:
   - ✅ Request blocked
   - ✅ CSRF error message

#### Test 5.3: Session Timeout
**Test Steps:**
1. Login as admin
2. Close browser completely
3. Reopen and try to access admin dashboard
4. **Expected**:
   - ✅ Redirected to login (if session expired)
   - ✅ Still logged in (if "Remember Me" was checked)

---

## 🎯 Quick Test Script

Run this complete test in 5 minutes:

```bash
# 1. Setup
flask seed
python app.py

# 2. Open browser and test:
# ✅ Visit http://localhost:5000/ - See 4 areas
# ✅ Search "North" - See 1 area
# ✅ Click Login - Use admin@cu.edu / adminpass
# ✅ Click Admin Dashboard - See stats
# ✅ Click Add New Area - Add "Test Area"
# ✅ Click Add Vehicle Status - Add car with capacity 10
# ✅ Edit the status - Change occupied to 5
# ✅ Delete the status - Confirm deletion
# ✅ Delete the area - Confirm deletion
# ✅ Click Logout - Return to home
# ✅ Verify public page still shows live data

# All working? ✅ SUCCESS!
```

---

## 📊 Test Results Template

Copy and fill this out:

```
PARKING NAVIGATOR - TEST RESULTS
Date: __________
Tester: __________

PUBLIC ACCESS:
[ ] Home page loads
[ ] Search works
[ ] API endpoint works
[ ] Live updates work

AUTHENTICATION:
[ ] Registration works
[ ] User login works
[ ] Admin login works
[ ] Logout works
[ ] Protected routes work

ADMIN FEATURES:
[ ] Dashboard loads
[ ] Add parking area works
[ ] Edit parking area works
[ ] Delete parking area works
[ ] Add vehicle status works
[ ] Edit vehicle status works
[ ] Delete vehicle status works

OVERALL STATUS: [ ] PASS [ ] FAIL

ISSUES FOUND:
_________________________________
_________________________________
```

---

## 🐛 Common Issues & Solutions

### Issue 1: "No module named 'flask'"
**Solution:**
```bash
pip install -r requirements.txt
```

### Issue 2: "Table already exists"
**Solution:**
```bash
flask reset-db  # WARNING: Deletes all data
```

### Issue 3: CSRF Token errors
**Solution:**
- Clear browser cache
- Make sure app.py has csrf_token in context processor

### Issue 4: "Admin access only" error
**Solution:**
- Make sure you're logged in as admin@cu.edu
- Check if user.is_admin is True in database

### Issue 5: Live updates not working
**Solution:**
- Check browser console for JavaScript errors
- Verify API endpoints return correct JSON
- Check if main.js is loaded properly

---

## ✅ Test Completion

After completing all tests:
- [ ] All features work as expected
- [ ] No console errors
- [ ] No Python exceptions
- [ ] Data persists correctly
- [ ] Security features active

**Status: READY FOR PRODUCTION** 🚀

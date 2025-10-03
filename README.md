# 🅿️ Parking Navigator

> A real-time campus parking management system built with Flask

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0%2B-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-success.svg)]()

**Parking Navigator** is a comprehensive web application designed to help users find available parking spots across campus in real-time. Administrators can manage parking areas and update availability, while users can view live parking data through an intuitive interface.

---

## 📋 Table of Contents

- [Features](#-features)
- [Demo](#-demo)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Usage](#-usage)
- [API Documentation](#-api-documentation)
- [Screenshots](#-screenshots)
- [Testing](#-testing)
- [Deployment](#-deployment)
- [Contributing](#-contributing)
- [License](#-license)
- [Contact](#-contact)

---

## ✨ Features

### 🔐 User Authentication
- **Secure Login/Registration** - Password hashing with Werkzeug
- **Role-Based Access Control** - Admin and Regular user roles
- **Session Management** - Persistent login with "Remember Me"
- **CSRF Protection** - Built-in security with Flask-WTF

### 🚗 Parking Management
- **Real-Time Updates** - Live parking availability every 10 seconds
- **Multiple Vehicle Types** - Support for Cars, Bikes, and Buses
- **Smart Search** - Instant search by area name or location
- **Capacity Tracking** - Visual indicators for available spots

### 👨‍💼 Admin Dashboard
- **Area Management** - Add, edit, delete parking areas
- **Status Management** - Control vehicle capacity and occupancy
- **Live Statistics** - Real-time dashboard with metrics
- **Validation** - Prevents duplicate entries and invalid data

### 🎨 User Interface
- **Responsive Design** - Works on desktop, tablet, and mobile
- **Bootstrap 5** - Modern and clean UI
- **Real-Time Updates** - No page refresh needed
- **Interactive Elements** - Smooth animations and transitions

### 🔒 Security Features
- **Password Hashing** - Secure password storage
- **CSRF Tokens** - Protection against cross-site attacks
- **Session Security** - HTTP-only cookies
- **Input Validation** - Server-side and client-side validation

---

## 🎬 Demo


### Live Demo
🔗 **[Live Demo](https://parking-navigator.onrender.com/)** 

**Test Credentials:**
- Admin: `admin@cu.edu` / `adminpass`
- User: `user@cu.edu` / `userpass`

---

## 🛠 Tech Stack

### Backend
- **Flask 3.0+** - Python web framework
- **SQLAlchemy** - ORM for database operations
- **Flask-Login** - User session management
- **Flask-WTF** - Form handling and validation
- **Werkzeug** - Password hashing and security

### Frontend
- **Bootstrap 5.3** - Responsive UI framework
- **Vanilla JavaScript** - Real-time updates and interactions
- **HTML5/CSS3** - Modern web standards
- **Font Awesome** - Icons (optional)

### Database
- **SQLite** - Development database (default)
- **PostgreSQL** - Production ready (configurable)
- **MySQL** - Alternative option (configurable)

### Development Tools
- **Python Dotenv** - Environment variable management
- **Flask CLI** - Command-line tools
- **Pylance** - Type checking
- **Git** - Version control

---

## 📁 Project Structure

```
parking_navigator/
│
├── 📄 app.py                      # Application entry point
├── 📄 config.py                   # Configuration settings
├── 📄 models.py                   # Database models
├── 📄 forms.py                    # WTForms definitions
├── 📄 utils.py                    # Utility functions (seeding)
│
├── 🔐 auth.py                     # Authentication routes
├── 👨‍💼 admin_routes.py             # Admin dashboard routes
├── 🌐 public_routes.py            # Public & API routes
│
├── 📁 templates/                  # Jinja2 templates
│   ├── base.html                  # Base template
│   ├── index.html                 # Public homepage
│   ├── login.html                 # Login page
│   ├── register.html              # Registration page
│   ├── admin.html                 # Admin dashboard
│   ├── admin_area_form.html       # Add/Edit parking area
│   └── admin_status_form.html     # Add/Edit vehicle status
│
├── 📁 static/                     # Static assets
│   ├── css/
│   │   └── styles.css             # Custom styles
│   └── js/
│       └── main.js                # JavaScript logic
│
├── 📁 instance/                   # Instance folder (ignored)
│   └── parking.db                 # SQLite database
│
├── 📄 requirements.txt            # Python dependencies
├── 📄 .env                        # Environment variables
├── 📄 .gitignore                  # Git ignore rules
├── 📄 README.md                   # This file
└── 📄 LICENSE                     # MIT License
```

---

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git (optional)

### Step 1: Clone the Repository
```bash
# Using Git
git clone https://github.com/bansalayush475/parking_navigator.git
cd parking_navigator

# OR download and extract ZIP
```

### Step 2: Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Set Up Environment Variables
```bash
# Create .env file
cp .env.example .env

# Edit .env with your settings
# SECRET_KEY=your-secret-key-here
# DATABASE_URL=sqlite:///parking.db
```

### Step 5: Initialize Database
```bash
# Seed database with sample data
flask seed

# OR create a fresh database
flask reset-db
```

### Step 6: Run the Application
```bash
# Development mode
python app.py

# OR using Flask CLI
flask run

# Application runs at: http://localhost:5000
```

---

## ⚙️ Configuration

### Environment Variables (.env)
```env
# Flask Configuration
FLASK_APP=app.py
FLASK_ENV=development
SECRET_KEY=your-super-secret-key-change-this-in-production

# Database Configuration
DATABASE_URL=sqlite:///parking.db
# DATABASE_URL=postgresql://user:pass@localhost/parking_db
# DATABASE_URL=mysql://user:pass@localhost/parking_db

# Server Configuration
PORT=5000
```

### Application Settings (config.py)
```python
class Config:
    # Security
    SECRET_KEY = os.environ.get("SECRET_KEY")
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # CSRF
    WTF_CSRF_ENABLED = True
    
    # Session
    SESSION_COOKIE_SECURE = True  # HTTPS only
    SESSION_COOKIE_HTTPONLY = True
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
```

---

## 📖 Usage

### For Regular Users

#### 1. View Parking Availability
- Navigate to homepage: `http://localhost:5000`
- View all parking areas with real-time availability
- Data updates automatically every 10 seconds

#### 2. Search Parking Areas
- Use search bar to filter by name or location
- Results update instantly as you type

#### 3. Check Specific Vehicle Types
- Each area shows availability for:
  - 🚗 Cars
  - 🏍️ Bikes
  - 🚌 Buses (if available)

### For Administrators

#### 1. Login to Admin Panel
```
URL: http://localhost:5000/auth/login
Email: admin@cu.edu
Password: adminpass
```

#### 2. Manage Parking Areas
- **Add Area**: Click "Add New Parking Area"
- **Edit Area**: Click edit icon next to area name
- **Delete Area**: Click delete button (confirms before deletion)

#### 3. Manage Vehicle Statuses
- **Add Status**: Click "Add Vehicle Status" in any area
- **Edit Status**: Modify capacity and occupancy
- **Delete Status**: Remove vehicle type from area

#### 4. View Statistics
- Total parking areas
- Total capacity across all areas
- Currently occupied spots
- Available spots

### CLI Commands

```bash
# Seed database with sample data
flask seed

# Reset database (WARNING: Deletes all data)
flask reset-db

# Create a new admin user
flask create-admin

# Run application
python app.py

# Run with custom port
PORT=8080 python app.py
```

---

## 🔌 API Documentation

### Public Endpoints

#### Get All Parking Areas
```http
GET /
```
**Response:** HTML page with all parking areas

#### Get Area Status (JSON)
```http
GET /api/status/<int:area_id>
```
**Response:**
```json
{
  "areaId": 1,
  "areaName": "North Block",
  "location": "Near Main Gate",
  "statuses": [
    {
      "vehicle_type": "car",
      "capacity": 50,
      "occupied": 35,
      "available": 15
    }
  ],
  "available_spots": 15,
  "last_updated": "2025-01-15T10:30:00"
}
```

#### Search Areas (JSON)
```http
GET /api/search?q=north
```
**Response:**
```json
[
  {
    "id": 1,
    "name": "North Block",
    "location": "Near Main Gate",
    "status_count": 2,
    "available_spots": 40
  }
]
```

### Admin Endpoints (Authentication Required)

All admin endpoints require login with admin credentials.

#### Dashboard
```http
GET /admin/
```

#### Add Parking Area
```http
GET  /admin/add-area          # Show form
POST /admin/add-area          # Submit form
```

#### Edit Parking Area
```http
GET  /admin/edit-area/<int:area_id>
POST /admin/edit-area/<int:area_id>
```

#### Delete Parking Area
```http
POST /admin/delete-area/<int:area_id>
```

#### Manage Vehicle Status
```http
GET  /admin/manage-status/<int:area_id>
POST /admin/manage-status/<int:area_id>
```

#### Edit Vehicle Status
```http
GET  /admin/edit-status/<int:status_id>
POST /admin/edit-status/<int:status_id>
```

#### Delete Vehicle Status
```http
POST /admin/delete-status/<int:status_id>
```

---

## 🧪 Testing

### Manual Testing

#### Run Quick Test Script
```bash
# Linux/macOS
bash quick_test.sh

# Windows
quick_test.bat
```

#### Test Checklist
- [ ] Homepage loads with parking data
- [ ] Search functionality works
- [ ] Real-time updates every 10 seconds
- [ ] User registration works
- [ ] User login works
- [ ] Admin login redirects to dashboard
- [ ] Admin can add parking areas
- [ ] Admin can edit parking areas
- [ ] Admin can delete parking areas
- [ ] Admin can manage vehicle statuses
- [ ] Forms validate correctly
- [ ] CSRF protection active
- [ ] Mobile responsive design

### Automated Testing (Future)
```bash
# Run unit tests
pytest tests/

# Run with coverage
pytest --cov=. tests/

# Run specific test
pytest tests/test_auth.py
```

### API Testing
```bash
# Test API endpoints with curl
curl http://localhost:5000/api/status/1

# Test with authentication
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@cu.edu","password":"adminpass"}'
```

---

## 🚢 Deployment

### Heroku Deployment

#### 1. Create Procfile
```
web: gunicorn app:app
```

#### 2. Install Gunicorn
```bash
pip install gunicorn
pip freeze > requirements.txt
```

#### 3. Deploy
```bash
heroku create parking-navigator
heroku addons:create heroku-postgresql:mini
git push heroku main
heroku run flask seed
heroku open
```

### Docker Deployment

#### 1. Create Dockerfile
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

#### 2. Build and Run
```bash
docker build -t parking-navigator .
docker run -p 5000:5000 parking-navigator
```

### VPS Deployment (Ubuntu)

```bash
# Install dependencies
sudo apt update
sudo apt install python3-pip python3-venv nginx

# Clone project
git clone https://github.com/yourusername/parking_navigator.git
cd parking_navigator

# Setup virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Configure Nginx
sudo nano /etc/nginx/sites-available/parking

# Start with supervisor/systemd
sudo systemctl start parking
sudo systemctl enable parking
```

---

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

### How to Contribute

1. **Fork the repository**
2. **Create a feature branch**
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Commit your changes**
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. **Push to the branch**
   ```bash
   git push origin feature/AmazingFeature
   ```
5. **Open a Pull Request**

### Development Guidelines

- Follow PEP 8 style guide
- Add docstrings to functions
- Write meaningful commit messages
- Test before submitting PR
- Update documentation if needed

### Code Style
```python
# Good
def calculate_available_spots(capacity: int, occupied: int) -> int:
    """Calculate available parking spots.
    
    Args:
        capacity: Total parking capacity
        occupied: Currently occupied spots
        
    Returns:
        Number of available spots
    """
    return max(0, capacity - occupied)
```

### Report Bugs
Found a bug? [Open an issue](https://github.com/yourusername/parking_navigator/issues)

---

## 📝 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2025 Parking Navigator

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 👥 Authors

- **Ayush Bansal** - *Initial work* - [Github](https://github.com/bansalayush475)

See also the list of [contributors](https://github.com/bansalayush475/parking_navigator/contributors) who participated in this project.

---

## 📧 Contact

**Project Maintainer:** Ayush Bansal
- Email: bansalayush475@gmail.com
- GitHub: [@bansalayush475](https://github.com/bansalayush475)
- LinkedIn: [Ayush Bansal](https://www.linkedin.com/in/ayush-bansal-563415347)

**Project Link:** [https://github.com/bansalayush475/parking_navigator](https://github.com/bansalayush475/parking_navigator)

---

## 🙏 Acknowledgments

- Flask documentation and community
- Bootstrap for the amazing UI framework
- Stack Overflow community
- All contributors and testers

---

## 🗺️ Roadmap

### Version 2.0 (Planned)
- [ ] Mobile app (React Native)
- [ ] Email notifications
- [ ] Reservation system
- [ ] Payment integration
- [ ] Analytics dashboard
- [ ] Multi-language support

### Version 1.5 (In Progress)
- [ ] Export reports (PDF/Excel)
- [ ] Advanced search filters
- [ ] User preferences
- [ ] Dark mode

### Version 1.0 (Current) ✅
- [x] Real-time parking updates
- [x] Admin dashboard
- [x] User authentication
- [x] Responsive design
- [x] Search functionality

---

## 📊 Project Statistics

![GitHub stars](https://img.shields.io/github/stars/yourusername/parking_navigator?style=social)
![GitHub forks](https://img.shields.io/github/forks/yourusername/parking_navigator?style=social)
![GitHub issues](https://img.shields.io/github/issues/yourusername/parking_navigator)
![GitHub pull requests](https://img.shields.io/github/issues-pr/yourusername/parking_navigator)

---

## ⚡ Quick Links

- [Installation Guide](#-installation)
- [User Guide](#-usage)
- [API Docs](#-api-documentation)
- [Contributing](#-contributing)
- [Report Bug](https://github.com/yourusername/parking_navigator/issues)
- [Request Feature](https://github.com/yourusername/parking_navigator/issues)

---

## 📚 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Bootstrap 5 Docs](https://getbootstrap.com/docs/5.3/)
- [SQLAlchemy Guide](https://docs.sqlalchemy.org/)
- [Python Best Practices](https://docs.python-guide.org/)

---

<div align="center">

**Made with ❤️ by [Ayush Bansal](https://github.com/bansalayush475)**

⭐ **Star this repo if you found it helpful!** ⭐

</div>
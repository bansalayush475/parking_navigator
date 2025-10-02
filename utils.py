# utils.py
from models import db, User, ParkingArea, ParkingStatus
from datetime import datetime


def seed_data():
    """
    Seed database with sample data for testing.
    This function is idempotent - safe to run multiple times.
    """
    print("🌱 Starting database seeding...")
    
    try:
        # Create admin user
        admin_email = "admin@cu.edu"
        admin = User.query.filter_by(email=admin_email).first()
        
        if not admin:
            admin = User()
            admin.email = admin_email
            admin.is_admin = True
            admin.set_password("adminpass")
            db.session.add(admin)
            print(f"✅ Created admin user: {admin_email}")
        else:
            print(f"ℹ️  Admin user already exists: {admin_email}")

        # Create regular test user
        user_email = "user@cu.edu"
        user = User.query.filter_by(email=user_email).first()
        
        if not user:
            user = User()
            user.email = user_email
            user.is_admin = False
            user.set_password("userpass")
            db.session.add(user)
            print(f"✅ Created test user: {user_email}")
        else:
            print(f"ℹ️  Test user already exists: {user_email}")

        db.session.commit()

        # Create parking areas with statuses
        areas_data = [
            {
                "name": "North Block",
                "location": "Near Main Gate - Building A",
                "statuses": [
                    {"vehicle_type": "car", "capacity": 50, "occupied": 35},
                    {"vehicle_type": "bike", "capacity": 100, "occupied": 75},
                ]
            },
            {
                "name": "South Wing",
                "location": "Behind Library - Block C",
                "statuses": [
                    {"vehicle_type": "car", "capacity": 40, "occupied": 20},
                    {"vehicle_type": "bike", "capacity": 80, "occupied": 45},
                    {"vehicle_type": "bus", "capacity": 10, "occupied": 3},
                ]
            },
            {
                "name": "East Plaza",
                "location": "Near Cafeteria - Block E",
                "statuses": [
                    {"vehicle_type": "car", "capacity": 60, "occupied": 55},
                    {"vehicle_type": "bike", "capacity": 120, "occupied": 90},
                ]
            },
            {
                "name": "West Ground",
                "location": "Sports Complex - Block W",
                "statuses": [
                    {"vehicle_type": "car", "capacity": 30, "occupied": 10},
                    {"vehicle_type": "bike", "capacity": 60, "occupied": 25},
                    {"vehicle_type": "bus", "capacity": 5, "occupied": 0},
                ]
            }
        ]

        for area_data in areas_data:
            area = ParkingArea.query.filter_by(name=area_data["name"]).first()
            
            if not area:
                area = ParkingArea()
                area.name = area_data["name"]
                area.location = area_data["location"]
                area.last_updated = datetime.utcnow()
                db.session.add(area)
                db.session.flush()  # Get the ID without committing
                
                # Add vehicle statuses
                for status_data in area_data["statuses"]:
                    status = ParkingStatus()
                    status.vehicle_type = status_data["vehicle_type"]
                    status.capacity = status_data["capacity"]
                    status.occupied = status_data["occupied"]
                    status.area_id = area.id
                    db.session.add(status)
                
                print(f"✅ Created parking area: {area.name} with {len(area_data['statuses'])} vehicle types")
            else:
                print(f"ℹ️  Parking area already exists: {area.name}")

        db.session.commit()
        
        print("\n✅ Database seeding completed successfully!")
        print(f"\n📊 Summary:")
        print(f"   - Users: {User.query.count()}")
        print(f"   - Parking Areas: {ParkingArea.query.count()}")
        print(f"   - Vehicle Statuses: {ParkingStatus.query.count()}")
        print(f"\n🔑 Login Credentials:")
        print(f"   Admin: admin@cu.edu / adminpass")
        print(f"   User:  user@cu.edu / userpass")
        
    except Exception as e:
        db.session.rollback()
        print(f"❌ Error during seeding: {str(e)}")
        raise


def reset_database():
    """
    Drop all tables and recreate them.
    WARNING: This will delete all data!
    """
    print("⚠️  WARNING: This will delete all data!")
    confirm = input("Type 'YES' to confirm: ")
    
    if confirm == "YES":
        db.drop_all()
        db.create_all()
        print("✅ Database reset complete!")
        seed_data()
    else:
        print("❌ Database reset cancelled.")
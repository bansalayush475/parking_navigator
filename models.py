# models.py
from __future__ import annotations
from typing import TYPE_CHECKING
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

if TYPE_CHECKING:
    from sqlalchemy.orm import Mapped
    from typing import List


class User(UserMixin, db.Model):
    """User model for authentication"""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password: str):
        """Hash and set user password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Verify user password"""
        if not password:
            return False
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.email}>"


class ParkingArea(db.Model):
    """Parking area model"""
    __tablename__ = "parking_areas"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True, index=True)
    location = db.Column(db.String(150), nullable=False)
    last_updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship with cascade delete
    statuses = db.relationship(
        "ParkingStatus",
        backref="area",
        cascade="all, delete-orphan",
        lazy="joined",
        order_by="ParkingStatus.vehicle_type"
    )

    # Type hint for IDE support
    if TYPE_CHECKING:
        statuses: List[ParkingStatus]

    @property
    def available_spots(self) -> int:
        """Calculate total available spots across all vehicle types"""
        if not self.statuses:
            return 0
        return sum(s.available_spots() for s in self.statuses)

    @property
    def total_capacity(self) -> int:
        """Calculate total capacity across all vehicle types"""
        if not self.statuses:
            return 0
        return sum(s.capacity for s in self.statuses)

    @property
    def total_occupied(self) -> int:
        """Calculate total occupied spots across all vehicle types"""
        if not self.statuses:
            return 0
        return sum(s.occupied for s in self.statuses)

    @property
    def occupancy_rate(self) -> float:
        """Calculate occupancy rate as percentage"""
        if self.total_capacity == 0:
            return 0.0
        return (self.total_occupied / self.total_capacity) * 100

    def __repr__(self):
        return f"<ParkingArea {self.name}>"


class ParkingStatus(db.Model):
    """Vehicle status for parking areas"""
    __tablename__ = "parking_status"

    id = db.Column(db.Integer, primary_key=True)
    vehicle_type = db.Column(db.String(50), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    occupied = db.Column(db.Integer, default=0)
    area_id = db.Column(db.Integer, db.ForeignKey("parking_areas.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def available_spots(self) -> int:
        """Calculate available spots for this vehicle type"""
        available = self.capacity - self.occupied
        return max(0, available)

    def is_full(self) -> bool:
        """Check if parking is full"""
        return self.occupied >= self.capacity

    def occupancy_percentage(self) -> float:
        """Calculate occupancy percentage"""
        if self.capacity == 0:
            return 0.0
        return (self.occupied / self.capacity) * 100

    def __repr__(self):
        return f"<ParkingStatus {self.vehicle_type} {self.occupied}/{self.capacity}>"
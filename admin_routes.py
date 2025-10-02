# admin_routes.py - COMPLETE FIX (Type-safe version)
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from models import db, ParkingArea, ParkingStatus
from forms import ParkingAreaForm, ParkingStatusForm
from datetime import datetime
from functools import wraps

admin_bp = Blueprint("admin", __name__, template_folder="templates")


def admin_required(func):
    """Decorator to require admin access"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash("⚠️ Admin access only!", "danger")
            return redirect(url_for("public.index"))
        return func(*args, **kwargs)
    return wrapper


@admin_bp.route("/")
@login_required
@admin_required
def dashboard():
    """Admin dashboard showing all parking areas"""
    try:
        areas = ParkingArea.query.all()
        
        # Calculate statistics
        total_capacity = 0
        total_occupied = 0
        total_available = 0
        
        for area in areas:
            for status in area.statuses:
                total_capacity += status.capacity
                total_occupied += status.occupied
            total_available += area.available_spots
        
        stats = {
            'total_areas': len(areas),
            'total_capacity': total_capacity,
            'total_occupied': total_occupied,
            'total_available': total_available
        }
        
        return render_template("admin.html", areas=areas, stats=stats)
    except Exception as e:
        flash(f"❌ Error loading dashboard: {str(e)}", "danger")
        return redirect(url_for("public.index"))


@admin_bp.route("/add-area", methods=["GET", "POST"])
@login_required
@admin_required
def add_area():
    """Add a new parking area"""
    form = ParkingAreaForm()
    if form.validate_on_submit():
        try:
            # Check if area with same name exists
            existing = ParkingArea.query.filter_by(name=form.name.data).first()
            if existing:
                flash("⚠️ Parking area with this name already exists!", "warning")
                return render_template("admin_area_form.html", form=form, action="Add")
            
            new_area = ParkingArea(
                name=form.name.data,
                location=form.location.data,
                last_updated=datetime.utcnow()
            )
            db.session.add(new_area)
            db.session.commit()
            flash("✅ Parking area added successfully!", "success")
            return redirect(url_for("admin.dashboard"))
        except Exception as e:
            db.session.rollback()
            flash(f"❌ Error adding area: {str(e)}", "danger")
    
    return render_template("admin_area_form.html", form=form, action="Add")


@admin_bp.route("/edit-area/<int:area_id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_area(area_id):
    """Edit an existing parking area"""
    area = ParkingArea.query.get_or_404(area_id)
    form = ParkingAreaForm(obj=area)
    
    if form.validate_on_submit():
        try:
            # Check if another area has this name
            existing = ParkingArea.query.filter(
                ParkingArea.name == form.name.data,
                ParkingArea.id != area_id
            ).first()
            if existing:
                flash("⚠️ Another area with this name already exists!", "warning")
                return render_template("admin_area_form.html", form=form, action="Edit", area=area)
            
            area.name = form.name.data
            area.location = form.location.data
            area.last_updated = datetime.utcnow()
            db.session.commit()
            flash("✏️ Parking area updated successfully!", "info")
            return redirect(url_for("admin.dashboard"))
        except Exception as e:
            db.session.rollback()
            flash(f"❌ Error updating area: {str(e)}", "danger")
    
    return render_template("admin_area_form.html", form=form, action="Edit", area=area)


@admin_bp.route("/delete-area/<int:area_id>", methods=["POST"])
@login_required
@admin_required
def delete_area(area_id):
    """Delete a parking area"""
    try:
        area = ParkingArea.query.get_or_404(area_id)
        area_name = area.name
        db.session.delete(area)
        db.session.commit()
        flash(f"🗑️ Parking area '{area_name}' deleted successfully.", "warning")
    except Exception as e:
        db.session.rollback()
        flash(f"❌ Error deleting area: {str(e)}", "danger")
    
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/manage-status/<int:area_id>", methods=["GET", "POST"])
@login_required
@admin_required
def manage_status(area_id):
    """Add vehicle status to a parking area"""
    area = ParkingArea.query.get_or_404(area_id)
    form = ParkingStatusForm()
    
    if form.validate_on_submit():
        try:
            # Check if this vehicle type already exists for this area
            existing = ParkingStatus.query.filter_by(
                area_id=area_id,
                vehicle_type=form.vehicle_type.data
            ).first()
            
            if existing:
                flash(f"⚠️ {form.vehicle_type.data.title()} status already exists for this area!", "warning")
                return render_template("admin_status_form.html", form=form, area=area, action="Add")
            
            # Validate occupied <= capacity (with proper None checks)
            occupied = form.occupied.data or 0
            capacity = form.capacity.data or 0
            
            if occupied > capacity:
                flash("⚠️ Occupied spots cannot exceed capacity!", "warning")
                return render_template("admin_status_form.html", form=form, area=area, action="Add")
            
            new_status = ParkingStatus(
                vehicle_type=form.vehicle_type.data,
                capacity=capacity,
                occupied=occupied,
                area_id=area_id
            )
            db.session.add(new_status)
            area.last_updated = datetime.utcnow()
            db.session.commit()
            flash("✅ Vehicle status added successfully!", "success")
            return redirect(url_for("admin.dashboard"))
        except Exception as e:
            db.session.rollback()
            flash(f"❌ Error adding status: {str(e)}", "danger")
    
    return render_template("admin_status_form.html", form=form, area=area, action="Add")


@admin_bp.route("/edit-status/<int:status_id>", methods=["GET", "POST"])
@login_required
@admin_required
def edit_status(status_id):
    """Edit vehicle status"""
    status = ParkingStatus.query.get_or_404(status_id)
    form = ParkingStatusForm(obj=status)
    
    if form.validate_on_submit():
        try:
            # Validate occupied <= capacity (with proper None checks)
            occupied = form.occupied.data or 0
            capacity = form.capacity.data or 0
            
            if occupied > capacity:
                flash("⚠️ Occupied spots cannot exceed capacity!", "warning")
                return render_template("admin_status_form.html", form=form, area=status.area, action="Edit", status=status)
            
            status.vehicle_type = form.vehicle_type.data
            status.capacity = capacity
            status.occupied = occupied
            status.area.last_updated = datetime.utcnow()
            db.session.commit()
            flash("✏️ Vehicle status updated successfully!", "info")
            return redirect(url_for("admin.dashboard"))
        except Exception as e:
            db.session.rollback()
            flash(f"❌ Error updating status: {str(e)}", "danger")
    
    return render_template("admin_status_form.html", form=form, area=status.area, action="Edit", status=status)


@admin_bp.route("/delete-status/<int:status_id>", methods=["POST"])
@login_required
@admin_required
def delete_status(status_id):
    """Delete vehicle status"""
    try:
        status = ParkingStatus.query.get_or_404(status_id)
        vehicle_type = status.vehicle_type
        area = status.area
        db.session.delete(status)
        area.last_updated = datetime.utcnow()
        db.session.commit()
        flash(f"🗑️ {vehicle_type.title()} status deleted successfully.", "warning")
    except Exception as e:
        db.session.rollback()
        flash(f"❌ Error deleting status: {str(e)}", "danger")
    
    return redirect(url_for("admin.dashboard"))


@admin_bp.route("/update-status/<int:status_id>", methods=["POST"])
@login_required
@admin_required
def update_status(status_id):
    """Quick update for occupied spots (AJAX endpoint)"""
    try:
        status = ParkingStatus.query.get_or_404(status_id)
        occupied = request.form.get("occupied", type=int)
        
        if occupied is None:
            return jsonify({"success": False, "error": "Occupied value required"}), 400
        
        if occupied < 0:
            return jsonify({"success": False, "error": "Occupied cannot be negative"}), 400
        
        if occupied > status.capacity:
            return jsonify({"success": False, "error": "Occupied exceeds capacity"}), 400
        
        status.occupied = occupied
        status.area.last_updated = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            "success": True,
            "available": status.available_spots(),
            "occupied": status.occupied
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500
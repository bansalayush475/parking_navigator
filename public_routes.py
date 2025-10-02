# public_routes.py
from flask import Blueprint, render_template, request, jsonify
from models import ParkingArea

public_bp = Blueprint("public", __name__, template_folder="templates")


@public_bp.route("/")
def index():
    """Home page showing all parking areas"""
    try:
        areas = ParkingArea.query.order_by(ParkingArea.name).all()
        return render_template("index.html", areas=areas)
    except Exception as e:
        return render_template("index.html", areas=[], error=str(e))


@public_bp.route("/api/status/<int:area_id>")
def get_status(area_id):
    """API endpoint to get parking status for a specific area"""
    try:
        area = ParkingArea.query.get_or_404(area_id)
        statuses = [
            {
                "vehicle_type": s.vehicle_type,
                "capacity": s.capacity,
                "occupied": s.occupied,
                "available": s.available_spots()
            }
            for s in area.statuses
        ]
        return jsonify({
            "areaId": area.id,
            "areaName": area.name,
            "location": area.location,
            "statuses": statuses,
            "available_spots": area.available_spots,
            "last_updated": area.last_updated.isoformat() if area.last_updated else None
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@public_bp.route("/api/search")
def search_area():
    """API endpoint to search parking areas"""
    try:
        q = request.args.get("q", "").strip()
        if not q:
            areas = ParkingArea.query.order_by(ParkingArea.name).all()
        else:
            areas = ParkingArea.query.filter(
                ParkingArea.name.ilike(f"%{q}%") | ParkingArea.location.ilike(f"%{q}%")
            ).order_by(ParkingArea.name).all()

        result = [
            {
                "id": a.id,
                "name": a.name,
                "location": a.location,
                "status_count": len(a.statuses),
                "available_spots": a.available_spots,
            }
            for a in areas
        ]
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
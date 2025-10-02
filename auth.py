# auth.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User
from forms import LoginForm, RegistrationForm

auth_bp = Blueprint("auth", __name__, template_folder="templates")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """User login route"""
    # Redirect if already logged in
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for("admin.dashboard"))
        return redirect(url_for("public.index"))

    form = LoginForm()
    
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email=form.email.data.lower().strip()).first()
            
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember.data)
                flash("✅ Login successful! Welcome back.", "success")
                
                # Handle 'next' parameter for redirects
                next_page = request.args.get("next")
                if next_page and next_page.startswith('/'):
                    return redirect(next_page)
                
                # Redirect based on user role
                if user.is_admin:
                    return redirect(url_for("admin.dashboard"))
                return redirect(url_for("public.index"))
            else:
                flash("❌ Invalid email or password. Please try again.", "danger")
        except Exception as e:
            flash(f"❌ Login error: {str(e)}", "danger")
    
    return render_template("login.html", form=form)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """User registration route"""
    # Redirect if already logged in
    if current_user.is_authenticated:
        return redirect(url_for("public.index"))

    form = RegistrationForm()
    
    if form.validate_on_submit():
        try:
            email = form.email.data.lower().strip()
            
            # Check if email already exists
            existing = User.query.filter_by(email=email).first()
            if existing:
                flash("⚠️ Email already registered. Please login instead.", "warning")
                return redirect(url_for("auth.login"))

            # Create new user
            new_user = User()
            new_user.email = email
            new_user.set_password(form.password.data)
            new_user.is_admin = False  # Regular users are not admins by default
            
            db.session.add(new_user)
            db.session.commit()

            flash("🎉 Registration successful! You can now login.", "success")
            return redirect(url_for("auth.login"))
            
        except Exception as e:
            db.session.rollback()
            flash(f"❌ Registration error: {str(e)}", "danger")

    return render_template("register.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    """User logout route"""
    logout_user()
    flash("👋 You have been logged out successfully.", "info")
    return redirect(url_for("auth.login"))
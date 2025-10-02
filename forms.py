from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange


# ----------------------
# Login Form
# ----------------------
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


# ----------------------
# Registration Form
# ----------------------
class RegistrationForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password", message="Passwords must match.")]
    )
    submit = SubmitField("Register")


# ----------------------
# Add / Edit Parking Area
# ----------------------
class ParkingAreaForm(FlaskForm):
    name = StringField("Area Name", validators=[DataRequired(), Length(max=100)])
    location = StringField("Location", validators=[DataRequired(), Length(max=150)])
    submit = SubmitField("Save")


# ----------------------
# Add / Edit Parking Status
# ----------------------
class ParkingStatusForm(FlaskForm):
    vehicle_type = SelectField(
        "Vehicle Type",
        choices=[("car", "Car"), ("bike", "Bike"), ("bus", "Bus")],
        validators=[DataRequired()]
    )
    capacity = IntegerField("Capacity", validators=[DataRequired(), NumberRange(min=1)])
    occupied = IntegerField("Occupied", validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField("Save")
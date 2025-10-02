# Flask Project

This is a Flask web application project. 

## Project Structure

- **app/**: Contains the main application code.
  - **models.py**: Defines the data models for the application.
  - **forms.py**: Contains form classes for user input.
  - **auth.py**: Handles authentication-related routes and logic.
  - **routes/**: Contains route definitions.
    - **admin_routes.py**: Routes for admin functionalities.
    - **public_routes.py**: Routes accessible to all users.
  - **utils.py**: Utility functions used across the application.
  - **templates/**: Contains HTML templates for rendering.
    - **base.html**: Base template for the application.
    - **auth/**: Contains authentication-related templates.
      - **login.html**: Login page template.
      - **register.html**: Registration page template.
    - **errors/**: Contains error templates.
      - **404.html**: Template for 404 error.
      - **500.html**: Template for 500 error.
  - **static/**: Contains static files like CSS and JavaScript.
    - **css/**: Stylesheets for the application.
      - **style.css**: Main stylesheet.
    - **js/**: JavaScript files for the application.
      - **main.js**: Main JavaScript file.

- **config.py**: Configuration settings for the application.
- **requirements.txt**: List of dependencies for the project.
- **run.py**: Entry point to run the application.
- **README.md**: Project documentation.
# config.py - FINAL VERSION
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR, "instance")

# Ensure instance directory exists
os.makedirs(INSTANCE_DIR, exist_ok=True)


class Config:
    """Application configuration"""
    
    # Flask
    SECRET_KEY = os.environ.get("SECRET_KEY") or "dev-secret-key-change-in-production"
    DEBUG = os.environ.get("FLASK_ENV") == "development"
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
        "sqlite:///" + os.path.join(INSTANCE_DIR, "parking.db")
    
    # Fix for different PostgreSQL drivers (using psycopg3)
    if SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith('postgres://'):
        # Render provides postgres://, convert to postgresql+psycopg://
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace(
            'postgres://', 
            'postgresql+psycopg://', 
            1
        )
    elif SQLALCHEMY_DATABASE_URI and SQLALCHEMY_DATABASE_URI.startswith('postgresql://'):
        # Convert postgresql:// to postgresql+psycopg:// for psycopg3
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace(
            'postgresql://', 
            'postgresql+psycopg://', 
            1
        )
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = DEBUG  # Log SQL queries in debug mode
    
    # Production database settings (for PostgreSQL)
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,      # Verify connections before using
        'pool_recycle': 300,        # Recycle connections after 5 minutes
        'pool_size': 10,            # Connection pool size
        'max_overflow': 20,         # Additional connections if pool is full
        'connect_args': {
            'connect_timeout': 10,  # Connection timeout in seconds
        }
    }
    
    # WTForms
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None  # No time limit for CSRF tokens
    
    # Session
    SESSION_COOKIE_SECURE = not DEBUG  # Only send cookies over HTTPS in production
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
    
    # Security headers
    SEND_FILE_MAX_AGE_DEFAULT = 0 if DEBUG else 31536000


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False


# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
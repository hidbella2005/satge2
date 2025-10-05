from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    country = db.Column(db.String(100), default='Morocco')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    hotels = db.relationship('Hotel', backref='city', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<City {self.name}>'

class HotelCategory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    hotels = db.relationship('Hotel', backref='category', lazy=True)

    def __repr__(self):
        return f'<HotelCategory {self.name}>'

class Hotel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    address = db.Column(db.String(300))
    rating = db.Column(db.Float, default=0.0)
    price_per_night = db.Column(db.Float, nullable=False)
    amenities = db.Column(db.Text)  # JSON string of amenities
    image_url = db.Column(db.String(500))
    is_available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign Keys
    city_id = db.Column(db.Integer, db.ForeignKey('city.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('hotel_category.id'), nullable=False)

    def __repr__(self):
        return f'<Hotel {self.name}>'

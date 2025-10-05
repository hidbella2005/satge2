from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import app, db
from models import User, City, HotelCategory, Hotel
from auth import auth_bp
from forms import HotelSearchForm, AdminHotelForm, AdminCityForm, AdminCategoryForm, AdminUserForm, AdminEditUserForm
import json

# Register auth blueprint
app.register_blueprint(auth_bp, url_prefix='/auth')

def admin_required(f):
    """Decorator to require admin access"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('Access denied. Admin privileges required.', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    """Home page"""
    if current_user.is_authenticated and current_user.is_admin:
        return redirect(url_for('admin_dashboard'))
    
    # Get featured hotels for display
    featured_hotels = Hotel.query.filter_by(is_available=True).order_by(Hotel.rating.desc()).limit(6).all()
    cities = City.query.all()
    return render_template('index.html', featured_hotels=featured_hotels, cities=cities)

@app.route('/hotels')
def hotels():
    """Hotel listing page with search and filtering"""
    form = HotelSearchForm()
    
    # Get query parameters
    search = request.args.get('search', '')
    city_id = request.args.get('city_id', type=int)
    category_id = request.args.get('category_id', type=int)
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    min_rating = request.args.get('min_rating', type=float)
    
    # Build query
    query = Hotel.query.filter_by(is_available=True)
    
    if search:
        query = query.filter(Hotel.name.contains(search))
    if city_id:
        query = query.filter_by(city_id=city_id)
    if category_id:
        query = query.filter_by(category_id=category_id)
    if min_price:
        query = query.filter(Hotel.price_per_night >= min_price)
    if max_price:
        query = query.filter(Hotel.price_per_night <= max_price)
    if min_rating:
        query = query.filter(Hotel.rating >= min_rating)
    
    hotels = query.order_by(Hotel.rating.desc()).all()
    cities = City.query.all()
    categories = HotelCategory.query.all()
    
    return render_template('hotels.html', 
                         hotels=hotels, 
                         cities=cities, 
                         categories=categories,
                         form=form,
                         search=search,
                         city_id=city_id,
                         category_id=category_id,
                         min_price=min_price,
                         max_price=max_price,
                         min_rating=min_rating)

@app.route('/admin')
@login_required
@admin_required
def admin_dashboard():
    """Admin dashboard with statistics"""
    stats = {
        'total_users': User.query.count(),
        'total_hotels': Hotel.query.count(),
        'total_cities': City.query.count(),
        'total_categories': HotelCategory.query.count(),
        'available_hotels': Hotel.query.filter_by(is_available=True).count(),
    }
    
    # Get recent hotels
    recent_hotels = Hotel.query.order_by(Hotel.created_at.desc()).limit(5).all()
    
    # Get city distribution data
    city_data = db.session.query(City.name, db.func.count(Hotel.id)).join(Hotel).group_by(City.name).all()
    
    # Get category distribution data
    category_data = db.session.query(HotelCategory.name, db.func.count(Hotel.id)).join(Hotel).group_by(HotelCategory.name).all()
    
    return render_template('admin/dashboard.html', 
                         stats=stats, 
                         recent_hotels=recent_hotels,
                         city_data=city_data,
                         category_data=category_data)

@app.route('/admin/users')
@login_required
@admin_required
def admin_users():
    """Admin users management"""
    users = User.query.order_by(User.created_at.desc()).all()
    form = AdminUserForm()
    return render_template('admin/users.html', users=users, form=form)

@app.route('/admin/users/create', methods=['POST'])
@login_required
@admin_required
def admin_create_user():
    """Create new user"""
    form = AdminUserForm()
    if form.validate_on_submit():
        # Check if user already exists
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists', 'danger')
            return redirect(url_for('admin_users'))
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already exists', 'danger')
            return redirect(url_for('admin_users'))
        
        user = User(
            username=form.username.data,
            email=form.email.data,
            is_admin=form.is_admin.data
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('User created successfully', 'success')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{field}: {error}', 'danger')
    return redirect(url_for('admin_users'))

@app.route('/admin/users/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_edit_user(user_id):
    """Edit user"""
    user = User.query.get_or_404(user_id)
    form = AdminEditUserForm(obj=user)
    
    if form.validate_on_submit():
        # Check if username/email already exists for other users
        existing_username = User.query.filter(User.username == form.username.data, User.id != user_id).first()
        existing_email = User.query.filter(User.email == form.email.data, User.id != user_id).first()
        
        if existing_username:
            flash('Username already exists', 'danger')
            return render_template('admin/edit_user.html', form=form, user=user)
        if existing_email:
            flash('Email already exists', 'danger')
            return render_template('admin/edit_user.html', form=form, user=user)
        
        user.username = form.username.data
        user.email = form.email.data
        user.is_admin = form.is_admin.data
        if form.password.data:
            user.set_password(form.password.data)
        
        db.session.commit()
        flash('User updated successfully', 'success')
        return redirect(url_for('admin_users'))
    
    return render_template('admin/edit_user.html', form=form, user=user)

@app.route('/admin/users/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def admin_delete_user(user_id):
    """Delete user"""
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('Cannot delete your own account', 'danger')
        return redirect(url_for('admin_users'))
    
    db.session.delete(user)
    db.session.commit()
    flash('User deleted successfully', 'success')
    return redirect(url_for('admin_users'))

@app.route('/admin/scrape', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_scrape_hotels():
    """Scrape hotels from Booking.com"""
    if request.method == 'POST':
        cities = request.form.get('cities', '').split(',')
        cities = [city.strip() for city in cities if city.strip()]
        limit = int(request.form.get('limit', 5))
        
        if not cities:
            flash('Please enter at least one city name', 'danger')
            return render_template('admin/scrape.html')
        
        try:
            # First try the hotel generator for reliable data
            from hotel_generator import generate_hotels_for_morocco
            total_hotels = generate_hotels_for_morocco(cities, limit)
            flash(f'Successfully generated {total_hotels} realistic hotels for {len(cities)} cities', 'success')
        except Exception as e:
            flash(f'Error generating hotel data: {str(e)}', 'danger')
        
        return redirect(url_for('admin_scrape_hotels'))
    
    return render_template('admin/scrape.html')

@app.route('/admin/cities')
@login_required
@admin_required
def admin_cities():
    """Admin cities management"""
    cities = City.query.order_by(City.name).all()
    form = AdminCityForm()
    return render_template('admin/cities.html', cities=cities, form=form)

@app.route('/admin/cities/create', methods=['POST'])
@login_required
@admin_required
def admin_create_city():
    """Create new city"""
    form = AdminCityForm()
    if form.validate_on_submit():
        if City.query.filter_by(name=form.name.data).first():
            flash('City already exists', 'danger')
            return redirect(url_for('admin_cities'))
        
        city = City(name=form.name.data, country=form.country.data)
        db.session.add(city)
        db.session.commit()
        flash('City created successfully', 'success')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{field}: {error}', 'danger')
    return redirect(url_for('admin_cities'))

@app.route('/admin/cities/<int:city_id>/delete', methods=['POST'])
@login_required
@admin_required
def admin_delete_city(city_id):
    """Delete city"""
    city = City.query.get_or_404(city_id)
    if city.hotels:
        flash('Cannot delete city with associated hotels', 'danger')
        return redirect(url_for('admin_cities'))
    
    db.session.delete(city)
    db.session.commit()
    flash('City deleted successfully', 'success')
    return redirect(url_for('admin_cities'))

@app.route('/admin/categories')
@login_required
@admin_required
def admin_categories():
    """Admin categories management"""
    categories = HotelCategory.query.order_by(HotelCategory.name).all()
    form = AdminCategoryForm()
    return render_template('admin/categories.html', categories=categories, form=form)

@app.route('/admin/categories/create', methods=['POST'])
@login_required
@admin_required
def admin_create_category():
    """Create new category"""
    form = AdminCategoryForm()
    if form.validate_on_submit():
        if HotelCategory.query.filter_by(name=form.name.data).first():
            flash('Category already exists', 'danger')
            return redirect(url_for('admin_categories'))
        
        category = HotelCategory(name=form.name.data, description=form.description.data)
        db.session.add(category)
        db.session.commit()
        flash('Category created successfully', 'success')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{field}: {error}', 'danger')
    return redirect(url_for('admin_categories'))

@app.route('/admin/categories/<int:category_id>/delete', methods=['POST'])
@login_required
@admin_required
def admin_delete_category(category_id):
    """Delete category"""
    category = HotelCategory.query.get_or_404(category_id)
    if category.hotels:
        flash('Cannot delete category with associated hotels', 'danger')
        return redirect(url_for('admin_categories'))
    
    db.session.delete(category)
    db.session.commit()
    flash('Category deleted successfully', 'success')
    return redirect(url_for('admin_categories'))

@app.route('/admin/hotels')
@login_required
@admin_required
def admin_hotels():
    """Admin hotels management"""
    hotels = Hotel.query.order_by(Hotel.created_at.desc()).all()
    form = AdminHotelForm()
    form.city_id.choices = [(c.id, c.name) for c in City.query.all()]
    form.category_id.choices = [(c.id, c.name) for c in HotelCategory.query.all()]
    return render_template('admin/hotels.html', hotels=hotels, form=form)

@app.route('/admin/hotels/create', methods=['POST'])
@login_required
@admin_required
def admin_create_hotel():
    """Create new hotel"""
    form = AdminHotelForm()
    form.city_id.choices = [(c.id, c.name) for c in City.query.all()]
    form.category_id.choices = [(c.id, c.name) for c in HotelCategory.query.all()]
    
    if form.validate_on_submit():
        hotel = Hotel(
            name=form.name.data,
            description=form.description.data,
            address=form.address.data,
            rating=form.rating.data,
            price_per_night=form.price_per_night.data,
            amenities=form.amenities.data,
            image_url=form.image_url.data,
            is_available=form.is_available.data,
            city_id=form.city_id.data,
            category_id=form.category_id.data
        )
        db.session.add(hotel)
        db.session.commit()
        flash('Hotel created successfully', 'success')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{field}: {error}', 'danger')
    return redirect(url_for('admin_hotels'))

@app.route('/admin/hotels/<int:hotel_id>/delete', methods=['POST'])
@login_required
@admin_required
def admin_delete_hotel(hotel_id):
    """Delete hotel"""
    hotel = Hotel.query.get_or_404(hotel_id)
    db.session.delete(hotel)
    db.session.commit()
    flash('Hotel deleted successfully', 'success')
    return redirect(url_for('admin_hotels'))

@app.route('/admin/hotels/<int:hotel_id>/toggle', methods=['POST'])
@login_required
@admin_required
def admin_toggle_hotel_availability(hotel_id):
    """Toggle hotel availability"""
    hotel = Hotel.query.get_or_404(hotel_id)
    hotel.is_available = not hotel.is_available
    db.session.commit()
    status = 'available' if hotel.is_available else 'unavailable'
    flash(f'Hotel marked as {status}', 'success')
    return redirect(url_for('admin_hotels'))

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

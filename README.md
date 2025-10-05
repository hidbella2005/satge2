# Hotel Management System

A complete Flask web application for managing hotels in Morocco with PostgreSQL database integration.

## Features

### User Features
- User registration and authentication
- Browse hotels with search and filtering
- View hotel details, ratings, and prices
- Responsive design with dark theme

### Admin Features
- Admin dashboard with statistics and charts
- User management (create, edit, delete users)
- Hotel management (CRUD operations)
- City and category management
- Hotel data scraping functionality
- Data visualization with Chart.js

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: PostgreSQL
- **Frontend**: Bootstrap 5 with dark theme
- **Authentication**: Flask-Login
- **Forms**: Flask-WTF
- **Charts**: Chart.js
- **Scraping**: BeautifulSoup4, Requests

## Installation

1. **Install Python 3.11+**

2. **Install dependencies**:
   ```bash
   pip install flask flask-sqlalchemy flask-login flask-wtf
   pip install psycopg2-binary requests beautifulsoup4 selenium
   pip install gunicorn werkzeug wtforms email-validator
   ```

3. **Set up PostgreSQL database**:
   - Create a PostgreSQL database
   - Set the `DATABASE_URL` environment variable:
     ```bash
     export DATABASE_URL="postgresql://username:password@localhost/hotel_db"
     ```

4. **Set Flask secret key**:
   ```bash
   export SESSION_SECRET="your-secret-key-here"
   ```

5. **Initialize database with sample data**:
   ```bash
   python seed_data.py
   ```

6. **Run the application**:
   ```bash
   python main.py
   # Or with Gunicorn:
   gunicorn --bind 0.0.0.0:5000 main:app
   ```

## Default Login Credentials

After running `seed_data.py`:

- **Admin**: 
  - Username: `admin`
  - Password: `admin123`

- **Regular User**: 
  - Username: `testuser`
  - Password: `user123`

## Project Structure

```
hotel_management_system/
├── app.py                 # Flask app configuration
├── main.py               # Application entry point
├── models.py             # Database models
├── routes.py             # Application routes
├── auth.py               # Authentication blueprint
├── forms.py              # WTForms definitions
├── scraper.py            # Hotel data scraping
├── seed_data.py          # Sample data generator
├── templates/            # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── hotels.html
│   └── admin/            # Admin templates
├── static/               # CSS, JS, images
│   ├── css/style.css
│   └── js/admin.js
└── README.md
```

## Database Models

### User
- User authentication and role management
- Admin vs regular user permissions

### City
- Moroccan cities for hotel locations
- One-to-many relationship with hotels

### HotelCategory
- Hotel classification (Luxury, Budget, Riad, etc.)
- One-to-many relationship with hotels

### Hotel
- Complete hotel information
- Foreign keys to City and HotelCategory
- Includes rating, price, amenities, images

## API Endpoints

### Public Routes
- `/` - Homepage with featured hotels
- `/hotels` - Hotel listing with search/filter
- `/auth/login` - User login
- `/auth/register` - User registration
- `/auth/logout` - User logout

### Admin Routes (Login Required)
- `/admin` - Admin dashboard
- `/admin/users` - User management
- `/admin/cities` - City management
- `/admin/categories` - Category management
- `/admin/hotels` - Hotel management
- `/admin/scrape` - Hotel scraping interface

## Customization

### Adding New Cities
1. Access admin panel
2. Go to Cities section
3. Add new Moroccan cities

### Hotel Categories
1. Access admin panel
2. Go to Categories section
3. Create custom hotel types

### Scraping Configuration
1. Access admin panel
2. Go to "Scrape Hotels"
3. Enter city names and limits
4. Monitor scraping progress

## Security Features

- Password hashing with Werkzeug
- CSRF protection with Flask-WTF
- Role-based access control
- SQL injection prevention with SQLAlchemy ORM
- Session management with Flask-Login

## Development

### Adding New Features
1. Create database models in `models.py`
2. Add routes in `routes.py`
3. Create forms in `forms.py`
4. Design templates in `templates/`
5. Add styling in `static/css/style.css`

### Database Migrations
1. Modify models in `models.py`
2. Run the application to auto-create tables
3. Or manually create migration scripts

## Deployment

### Production Setup
1. Use a production WSGI server (Gunicorn recommended)
2. Set up reverse proxy (Nginx)
3. Configure PostgreSQL for production
4. Set secure environment variables
5. Enable HTTPS

### Environment Variables
```bash
DATABASE_URL=postgresql://user:pass@host:port/dbname
SESSION_SECRET=your-secure-secret-key
FLASK_ENV=production
```

## Troubleshooting

### Common Issues
1. **Database Connection**: Check DATABASE_URL format
2. **Missing Tables**: Run `seed_data.py` to create tables
3. **Permission Errors**: Ensure admin user exists
4. **Scraping Issues**: Check network connectivity and rate limits

### Logs
- Application logs show in console
- Check Flask debug mode for detailed errors
- Monitor database queries with SQLAlchemy echo

## Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## License

This project is for educational purposes. Please respect website terms of service when scraping data.

## Contact

For questions or issues, please check the documentation or create an issue in the project repository.

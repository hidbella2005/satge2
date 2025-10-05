"""
Seed data script to populate the database with sample hotels, cities, and categories.
Run this script after setting up the database to populate it with sample data.
"""

from app import app, db
from models import User, City, HotelCategory, Hotel
from werkzeug.security import generate_password_hash

def create_sample_data():
    """Create sample data for the hotel management system"""
    
    with app.app_context():
        # Clear existing data
        print("Clearing existing data...")
        db.drop_all()
        db.create_all()
        
        # Create admin user
        print("Creating admin user...")
        admin = User(
            username='admin',
            email='admin@hotel.com',
            is_admin=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        
        # Create regular user
        print("Creating test user...")
        user = User(
            username='testuser',
            email='user@hotel.com',
            is_admin=False
        )
        user.set_password('user123')
        db.session.add(user)
        
        # Create Moroccan cities
        print("Creating cities...")
        cities_data = [
            'Casablanca',
            'Marrakech',
            'Rabat',
            'Fez',
            'Tangier',
            'Agadir',
            'Meknes',
            'Oujda',
            'Essaouira',
            'Chefchaouen'
        ]
        
        cities = []
        for city_name in cities_data:
            city = City(name=city_name, country='Morocco')
            cities.append(city)
            db.session.add(city)
        
        # Create hotel categories
        print("Creating hotel categories...")
        categories_data = [
            ('Luxury Resort', 'High-end resorts with premium amenities and services'),
            ('Boutique Hotel', 'Small, stylish hotels with personalized service'),
            ('Business Hotel', 'Hotels catering to business travelers with meeting facilities'),
            ('Budget Hotel', 'Affordable accommodations with basic amenities'),
            ('Riad', 'Traditional Moroccan houses converted into hotels'),
            ('Beach Resort', 'Hotels located on or near beaches with water activities'),
            ('Spa Hotel', 'Hotels specializing in wellness and spa treatments'),
            ('Heritage Hotel', 'Historic buildings converted into unique accommodations')
        ]
        
        categories = []
        for cat_name, cat_desc in categories_data:
            category = HotelCategory(name=cat_name, description=cat_desc)
            categories.append(category)
            db.session.add(category)
        
        # Commit cities and categories first
        db.session.commit()
        
        # Create sample hotels
        print("Creating hotels...")
        hotels_data = [
            # Casablanca
            {
                'name': 'Four Seasons Hotel Casablanca',
                'description': 'Luxury oceanfront hotel in the heart of Casablanca with stunning Atlantic views.',
                'address': 'Anfa Place, Boulevard de la Corniche, Casablanca',
                'rating': 4.8,
                'price_per_night': 350.00,
                'amenities': 'WiFi, Pool, Spa, Restaurant, Bar, Fitness Center, Ocean View',
                'image_url': 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=500',
                'city': 'Casablanca',
                'category': 'Luxury Resort'
            },
            {
                'name': 'Hyatt Regency Casablanca',
                'description': 'Modern business hotel with excellent conference facilities and city views.',
                'address': 'Place des Nations Unies, Casablanca',
                'rating': 4.5,
                'price_per_night': 280.00,
                'amenities': 'WiFi, Business Center, Restaurant, Bar, Fitness Center, Meeting Rooms',
                'image_url': 'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=500',
                'city': 'Casablanca',
                'category': 'Business Hotel'
            },
            
            # Marrakech
            {
                'name': 'La Mamounia',
                'description': 'Legendary palace hotel in the heart of Marrakech with lush gardens.',
                'address': 'Avenue Bab Jdid, Marrakech',
                'rating': 4.9,
                'price_per_night': 450.00,
                'amenities': 'WiFi, Pool, Spa, Multiple Restaurants, Gardens, Concierge',
                'image_url': 'https://images.unsplash.com/photo-1564501049412-61c2a3083791?w=500',
                'city': 'Marrakech',
                'category': 'Luxury Resort'
            },
            {
                'name': 'Riad Yasmine',
                'description': 'Traditional Moroccan riad with authentic architecture and courtyard.',
                'address': 'Derb Assehbi, Medina, Marrakech',
                'rating': 4.3,
                'price_per_night': 120.00,
                'amenities': 'WiFi, Traditional Courtyard, Rooftop Terrace, Moroccan Breakfast',
                'image_url': 'https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=500',
                'city': 'Marrakech',
                'category': 'Riad'
            },
            
            # Rabat
            {
                'name': 'Sofitel Rabat Jardin des Roses',
                'description': 'Elegant hotel combining French luxury with Moroccan hospitality.',
                'address': 'BP 450 Souissi, Rabat',
                'rating': 4.6,
                'price_per_night': 320.00,
                'amenities': 'WiFi, Pool, Spa, French Restaurant, Gardens, Tennis Court',
                'image_url': 'https://images.unsplash.com/photo-1520250497591-112f2f40a3f4?w=500',
                'city': 'Rabat',
                'category': 'Luxury Resort'
            },
            
            # Fez
            {
                'name': 'Riad Fes',
                'description': 'Luxury riad in the historic medina of Fez with panoramic views.',
                'address': 'Derb Ben Slimane, Zerbtana, Fez',
                'rating': 4.4,
                'price_per_night': 180.00,
                'amenities': 'WiFi, Spa, Restaurant, Medina Views, Traditional Hammam',
                'image_url': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=500',
                'city': 'Fez',
                'category': 'Riad'
            },
            {
                'name': 'Palais Medina & Spa',
                'description': 'Palatial hotel offering traditional Moroccan architecture and modern comfort.',
                'address': 'Rue Lalla Asmaa, Fez',
                'rating': 4.2,
                'price_per_night': 200.00,
                'amenities': 'WiFi, Spa, Pool, Restaurant, Traditional Architecture, Gardens',
                'image_url': 'https://images.unsplash.com/photo-1590490360182-c33d57733427?w=500',
                'city': 'Fez',
                'category': 'Heritage Hotel'
            },
            
            # Tangier
            {
                'name': 'Hilton Garden Inn Tanger City Center',
                'description': 'Modern hotel in the business district with Mediterranean views.',
                'address': 'Place du Maghreb Arabe, Tangier',
                'rating': 4.3,
                'price_per_night': 150.00,
                'amenities': 'WiFi, Restaurant, Fitness Center, Business Center, City Views',
                'image_url': 'https://images.unsplash.com/photo-1551882547-ff40c63fe5fa?w=500',
                'city': 'Tangier',
                'category': 'Business Hotel'
            },
            
            # Agadir
            {
                'name': 'Royal Atlas Agadir',
                'description': 'Beachfront resort with direct access to Agadir beach and Atlantic Ocean.',
                'address': 'Boulevard 20 Aout, Agadir',
                'rating': 4.1,
                'price_per_night': 180.00,
                'amenities': 'WiFi, Beach Access, Pool, Restaurant, Water Sports, Kids Club',
                'image_url': 'https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=500',
                'city': 'Agadir',
                'category': 'Beach Resort'
            },
            {
                'name': 'Ibis Budget Agadir',
                'description': 'Affordable hotel near the beach with modern amenities and friendly service.',
                'address': 'Secteur Touristique, Agadir',
                'rating': 3.8,
                'price_per_night': 60.00,
                'amenities': 'WiFi, Air Conditioning, 24h Reception, Near Beach',
                'image_url': 'https://images.unsplash.com/photo-1566073771259-6a8506099945?w=500',
                'city': 'Agadir',
                'category': 'Budget Hotel'
            },
            
            # Essaouira
            {
                'name': 'Heure Bleue Palais',
                'description': 'Boutique hotel in a restored riad with rooftop terrace and ocean views.',
                'address': '2 Rue Ibn Battouta, Essaouira',
                'rating': 4.5,
                'price_per_night': 220.00,
                'amenities': 'WiFi, Spa, Restaurant, Ocean Views, Rooftop Terrace, Hammam',
                'image_url': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=500',
                'city': 'Essaouira',
                'category': 'Boutique Hotel'
            },
            
            # Chefchaouen
            {
                'name': 'Casa Hassan',
                'description': 'Charming hotel in the blue city with traditional Moroccan hospitality.',
                'address': '22 Rue Targui, Chefchaouen',
                'rating': 4.0,
                'price_per_night': 90.00,
                'amenities': 'WiFi, Restaurant, Mountain Views, Traditional Decor, Terrace',
                'image_url': 'https://images.unsplash.com/photo-1590490360182-c33d57733427?w=500',
                'city': 'Chefchaouen',
                'category': 'Boutique Hotel'
            },
            
            # Meknes
            {
                'name': 'Riad Yacout',
                'description': 'Traditional riad in the imperial city with authentic Moroccan design.',
                'address': '27 Derb Jemaa, Meknes',
                'rating': 4.2,
                'price_per_night': 110.00,
                'amenities': 'WiFi, Traditional Courtyard, Restaurant, Imperial City Views',
                'image_url': 'https://images.unsplash.com/photo-1571896349842-33c89424de2d?w=500',
                'city': 'Meknes',
                'category': 'Riad'
            }
        ]
        
        for hotel_data in hotels_data:
            # Find city and category
            city = next((c for c in cities if c.name == hotel_data['city']), None)
            category = next((c for c in categories if c.name == hotel_data['category']), None)
            
            if city and category:
                hotel = Hotel(
                    name=hotel_data['name'],
                    description=hotel_data['description'],
                    address=hotel_data['address'],
                    rating=hotel_data['rating'],
                    price_per_night=hotel_data['price_per_night'],
                    amenities=hotel_data['amenities'],
                    image_url=hotel_data['image_url'],
                    is_available=True,
                    city_id=city.id,
                    category_id=category.id
                )
                db.session.add(hotel)
        
        # Commit all data
        db.session.commit()
        
        print("\n" + "="*50)
        print("Sample data created successfully!")
        print("="*50)
        print(f"Created {len(cities_data)} cities")
        print(f"Created {len(categories_data)} hotel categories")
        print(f"Created {len(hotels_data)} hotels")
        print("\nLogin credentials:")
        print("Admin: username='admin', password='admin123'")
        print("User:  username='testuser', password='user123'")
        print("="*50)

if __name__ == '__main__':
    create_sample_data()

"""
Hotel Data Generator for Morocco
This script generates realistic hotel data for Moroccan cities using various sources.
Since direct scraping may be blocked, this creates realistic sample data.
"""

import requests
from bs4 import BeautifulSoup
import time
import random
import json
from urllib.parse import urljoin, quote
from app import app, db
from models import Hotel, City, HotelCategory
import re

class BookingScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        })
        
    def get_page(self, url, params=None, retries=3):
        """Get a page with retries and rate limiting"""
        for attempt in range(retries):
            try:
                # Random delay between requests
                time.sleep(random.uniform(2, 5))
                
                response = self.session.get(url, params=params, timeout=15)
                response.raise_for_status()
                return response
            except Exception as e:
                print(f"Attempt {attempt + 1} failed for {url}: {e}")
                if attempt == retries - 1:
                    raise
                time.sleep(random.uniform(5, 10))
    
    def search_hotels_in_city(self, city_name, checkin="2024-12-01", checkout="2024-12-02", limit=20):
        """Search for hotels in a specific Moroccan city"""
        # Booking.com search URL
        search_url = f"https://www.booking.com/searchresults.html"
        
        params = {
            'ss': f"{city_name}, Morocco",
            'checkin_year': checkin.split('-')[0],
            'checkin_month': checkin.split('-')[1],
            'checkin_monthday': checkin.split('-')[2],
            'checkout_year': checkout.split('-')[0],
            'checkout_month': checkout.split('-')[1],
            'checkout_monthday': checkout.split('-')[2],
            'group_adults': '2',
            'group_children': '0',
            'no_rooms': '1',
            'offset': '0'
        }
        
        print(f"Searching for hotels in {city_name}...")
        
        try:
            response = self.get_page(search_url, params=params)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            hotels = []
            hotel_elements = soup.find_all('div', {'data-testid': 'property-card'})
            
            if not hotel_elements:
                # Try alternative selectors
                hotel_elements = soup.find_all('div', class_=re.compile('sr_item'))
                
            print(f"Found {len(hotel_elements)} hotel elements")
            
            for i, hotel_element in enumerate(hotel_elements[:limit]):
                try:
                    hotel_data = self.extract_hotel_data(hotel_element, city_name)
                    if hotel_data:
                        hotels.append(hotel_data)
                        print(f"Extracted: {hotel_data['name']}")
                    
                    # Rate limiting
                    time.sleep(random.uniform(1, 3))
                    
                except Exception as e:
                    print(f"Error extracting hotel {i}: {e}")
                    continue
                    
            return hotels
            
        except Exception as e:
            print(f"Error searching hotels in {city_name}: {e}")
            return []
    
    def extract_hotel_data(self, hotel_element, city_name):
        """Extract hotel data from a hotel element"""
        try:
            # Hotel name
            name_element = hotel_element.find('h3') or hotel_element.find('h2') or hotel_element.find('a', {'data-testid': 'title-link'})
            name = name_element.get_text(strip=True) if name_element else "Unknown Hotel"
            
            # Address
            address_element = hotel_element.find('span', {'data-testid': 'address'}) or hotel_element.find('span', class_=re.compile('address'))
            address = address_element.get_text(strip=True) if address_element else f"{city_name}, Morocco"
            
            # Price
            price_element = hotel_element.find('span', {'data-testid': 'price-and-discounted-price'}) or hotel_element.find('div', class_=re.compile('price'))
            price_text = price_element.get_text(strip=True) if price_element else "0"
            price = self.extract_price(price_text)
            
            # Rating
            rating_element = hotel_element.find('div', {'data-testid': 'review-score'}) or hotel_element.find('div', class_=re.compile('rating'))
            rating = self.extract_rating(rating_element.get_text(strip=True) if rating_element else "0")
            
            # Review text
            review_element = hotel_element.find('div', {'data-testid': 'review-score-word'}) or hotel_element.find('span', class_=re.compile('review'))
            review_text = review_element.get_text(strip=True) if review_element else "No reviews"
            
            # Description (limited from search results)
            desc_element = hotel_element.find('div', class_=re.compile('important_facility')) or hotel_element.find('div', class_=re.compile('facility'))
            description = desc_element.get_text(strip=True) if desc_element else f"Hotel in {city_name}, Morocco"
            
            # Image URL
            img_element = hotel_element.find('img')
            image_url = img_element.get('src') or img_element.get('data-src') if img_element else None
            
            return {
                'name': name,
                'description': description,
                'address': address,
                'rating': rating,
                'price_per_night': price,
                'review_text': review_text,
                'image_url': image_url,
                'city': city_name
            }
            
        except Exception as e:
            print(f"Error extracting hotel data: {e}")
            return None
    
    def extract_price(self, price_text):
        """Extract numeric price from price text"""
        try:
            # Remove currency symbols and extract numbers
            numbers = re.findall(r'\d+', price_text.replace(',', ''))
            if numbers:
                return float(numbers[0])
            return 100.0  # Default price if extraction fails
        except:
            return 100.0
    
    def extract_rating(self, rating_text):
        """Extract numeric rating from rating text"""
        try:
            # Look for decimal numbers in rating text
            rating_match = re.search(r'(\d+\.?\d*)', rating_text)
            if rating_match:
                rating = float(rating_match.group(1))
                # Normalize to 5-star scale if needed
                if rating > 5:
                    rating = rating / 2  # Convert from 10-point to 5-point scale
                return min(rating, 5.0)
            return 4.0  # Default rating
        except:
            return 4.0
    
    def save_hotels_to_database(self, hotels_data, city_name):
        """Save scraped hotels to the database"""
        with app.app_context():
            # Find or create city
            city = City.query.filter_by(name=city_name).first()
            if not city:
                city = City(name=city_name, country="Morocco")
                db.session.add(city)
                db.session.commit()
            
            # Find or create default category
            category = HotelCategory.query.filter_by(name="Scraped Hotel").first()
            if not category:
                category = HotelCategory(
                    name="Scraped Hotel",
                    description="Hotels scraped from Booking.com"
                )
                db.session.add(category)
                db.session.commit()
            
            saved_count = 0
            for hotel_data in hotels_data:
                try:
                    # Check if hotel already exists
                    existing = Hotel.query.filter_by(name=hotel_data['name'], city_id=city.id).first()
                    if existing:
                        print(f"Hotel {hotel_data['name']} already exists, skipping...")
                        continue
                    
                    # Create new hotel
                    hotel = Hotel(
                        name=hotel_data['name'],
                        description=hotel_data['description'],
                        address=hotel_data['address'],
                        rating=hotel_data['rating'],
                        price_per_night=hotel_data['price_per_night'],
                        amenities=f"Review: {hotel_data['review_text']}",
                        image_url=hotel_data['image_url'],
                        is_available=True,
                        city_id=city.id,
                        category_id=category.id
                    )
                    
                    db.session.add(hotel)
                    saved_count += 1
                    
                except Exception as e:
                    print(f"Error saving hotel {hotel_data['name']}: {e}")
                    continue
            
            db.session.commit()
            print(f"Saved {saved_count} new hotels to database")
            return saved_count

def scrape_moroccan_cities(cities=None, limit_per_city=10):
    """Scrape hotels from multiple Moroccan cities"""
    if cities is None:
        cities = [
            "Casablanca", "Marrakech", "Rabat", "Fez", 
            "Tangier", "Agadir", "Essaouira", "Chefchaouen"
        ]
    
    scraper = BookingScraper()
    total_hotels = 0
    
    for city in cities:
        print(f"\n{'='*50}")
        print(f"Scraping hotels in {city}")
        print(f"{'='*50}")
        
        try:
            hotels = scraper.search_hotels_in_city(city, limit=limit_per_city)
            if hotels:
                saved = scraper.save_hotels_to_database(hotels, city)
                total_hotels += saved
                print(f"Successfully scraped {len(hotels)} hotels from {city}")
            else:
                print(f"No hotels found for {city}")
                
        except Exception as e:
            print(f"Error scraping {city}: {e}")
            continue
        
        # Longer delay between cities
        print("Waiting before next city...")
        time.sleep(random.uniform(10, 20))
    
    print(f"\n{'='*50}")
    print(f"Scraping completed! Total hotels saved: {total_hotels}")
    print(f"{'='*50}")
    
    return total_hotels

if __name__ == "__main__":
    # Example usage
    print("Starting Booking.com scraper for Morocco...")
    
    # Scrape hotels from major Moroccan cities
    cities_to_scrape = ["Marrakech", "Casablanca", "Fez"]
    total = scrape_moroccan_cities(cities_to_scrape, limit_per_city=5)
    
    print(f"Scraping finished. {total} hotels added to database.")
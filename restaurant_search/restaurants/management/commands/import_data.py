import os, re, csv
from tqdm import tqdm
from django.core.management.base import BaseCommand
from restaurants.models import Restaurant, Dish

CSV_PATH = __file__
for _ in range(4):
    CSV_PATH = os.path.dirname(CSV_PATH)
CSV_PATH = os.path.join(CSV_PATH, "restaurants_small.csv")

class Command(BaseCommand):
    help = 'Load data from CSV file'

    def handle(self, *args, **kwargs):
        restaurants_to_create = []
        dishes_to_create = []

        with open(CSV_PATH, newline='', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in tqdm(reader, desc = "Loading data", leave = False):
                restaurant, _ = Restaurant.objects.get_or_create(
                    id=row['id'],
                    defaults={
                        'name': row['name'],
                        'location': row['location'],
                        'lat_long': row['lat_long'],
                        'full_details': row['full_details'],
                    },
                )
                
                items = eval(row['items'])  # Convert string to dictionary
                for dish_name, price in items.items():
                    # Clean the price value
                    clean_price = re.sub(r'[^\d.]', '', price).strip()
                    try:
                        clean_price = float(clean_price)
                    except ValueError:
                        clean_price = 0.0  # Default to 0 if price is invalid

                    dishes_to_create.append(Dish(
                        restaurant=restaurant,
                        name=dish_name.strip(),
                        price=clean_price
                    ))

        # Bulk create dishes
        Dish.objects.bulk_create(dishes_to_create, batch_size=1000)
        self.stdout.write(self.style.SUCCESS('Data imported successfully'))

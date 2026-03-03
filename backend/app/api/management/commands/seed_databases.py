from django.core.management.base import BaseCommand
from datetime import datetime, timedelta
import random
from services.db_manager import DBManager


NAMES = [
    'Aarav Sharma', 'Emma Wilson', 'Liam Garcia', 'Sophia Martin', 'Noah Brown',
    'Olivia Lee', 'Mason Hall', 'Ava Allen', 'Ethan Young', 'Mia King',
    'Lucas Scott', 'Isabella Green', 'James Adams', 'Charlotte Baker', 'Benjamin Clark'
]
COUNTRIES = ['USA', 'Canada', 'India', 'Germany', 'UK', 'Australia']
PRODUCTS = ['Laptop', 'Phone', 'Keyboard', 'Headphones', 'Monitor', 'Mouse', 'Tablet']
INTERESTS = ['tech', 'gaming', 'travel', 'fitness', 'music', 'finance', 'books']


class Command(BaseCommand):
    help = 'Seed PostgreSQL and MongoDB with sample data'

    def handle(self, *args, **kwargs):
        self.seed_postgres()
        self.seed_mongo()
        self.stdout.write(self.style.SUCCESS('Database seeding completed.'))

    def seed_postgres(self):
        with DBManager.pg_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS users (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(120) NOT NULL,
                        email VARCHAR(120) UNIQUE NOT NULL,
                        age INTEGER,
                        country VARCHAR(80),
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                    """
                )
                cur.execute(
                    """
                    CREATE TABLE IF NOT EXISTS orders (
                        id SERIAL PRIMARY KEY,
                        user_id INTEGER REFERENCES users(id),
                        product_name VARCHAR(120),
                        price NUMERIC(10,2),
                        quantity INTEGER,
                        order_date TIMESTAMP
                    );
                    """
                )
                cur.execute("SELECT COUNT(*) FROM users;")
                if cur.fetchone()[0] == 0:
                    for idx, name in enumerate(NAMES, start=1):
                        cur.execute(
                            "INSERT INTO users (name, email, age, country, created_at) VALUES (%s,%s,%s,%s,%s)",
                            (
                                name,
                                f"user{idx}@example.com",
                                random.randint(20, 55),
                                random.choice(COUNTRIES),
                                datetime.utcnow() - timedelta(days=random.randint(1, 900)),
                            ),
                        )

                cur.execute("SELECT COUNT(*) FROM orders;")
                if cur.fetchone()[0] == 0:
                    for _ in range(30):
                        cur.execute(
                            "INSERT INTO orders (user_id, product_name, price, quantity, order_date) VALUES (%s,%s,%s,%s,%s)",
                            (
                                random.randint(1, 15),
                                random.choice(PRODUCTS),
                                round(random.uniform(30, 2200), 2),
                                random.randint(1, 5),
                                datetime.utcnow() - timedelta(days=random.randint(1, 365)),
                            ),
                        )
            conn.commit()

    def seed_mongo(self):
        db = DBManager.mongo_db()
        if db.customers.count_documents({}) == 0:
            customers = []
            for i, name in enumerate(NAMES, start=1):
                customers.append(
                    {
                        '_id': i,
                        'name': name,
                        'email': f'customer{i}@example.com',
                        'age': random.randint(20, 55),
                        'country': random.choice(COUNTRIES),
                        'interests': random.sample(INTERESTS, k=3),
                        'created_at': datetime.utcnow() - timedelta(days=random.randint(1, 900)),
                    }
                )
            db.customers.insert_many(customers)

        if db.purchases.count_documents({}) == 0:
            purchases = []
            for i in range(1, 31):
                items = []
                for _ in range(random.randint(1, 3)):
                    price = round(random.uniform(20, 1200), 2)
                    qty = random.randint(1, 4)
                    items.append(
                        {
                            'product_name': random.choice(PRODUCTS),
                            'price': price,
                            'quantity': qty,
                        }
                    )
                total_price = round(sum(x['price'] * x['quantity'] for x in items), 2)
                purchases.append(
                    {
                        '_id': i,
                        'customer_id': random.randint(1, 15),
                        'items': items,
                        'total_price': total_price,
                        'purchase_date': datetime.utcnow() - timedelta(days=random.randint(1, 365)),
                    }
                )
            db.purchases.insert_many(purchases)

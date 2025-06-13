import psycopg2
from faker import Faker
from datetime import datetime, timedelta
import random

fake = Faker()

# PostgreSQL connection
conn = psycopg2.connect(
    dbname='user_activity',
    user='postgres',
    password='genci1',
    host='localhost',
    port=5433
)
cur = conn.cursor()

# Create tables
cur.execute("""
    DROP TABLE IF EXISTS orders, activities, products, users CASCADE;
    
    CREATE TABLE users (
        user_id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    
    CREATE TABLE products (
        product_id SERIAL PRIMARY KEY,
        product_name VARCHAR(100) NOT NULL,
        price NUMERIC(10, 2) NOT NULL
    );
    
    CREATE TABLE activities (
        activity_id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(user_id),
        activity_type VARCHAR(50) NOT NULL,
        activity_date TIMESTAMP NOT NULL
    );
    
    CREATE TABLE orders (
        order_id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(user_id),
        product_id INTEGER REFERENCES products(product_id),
        order_date TIMESTAMP NOT NULL,
        quantity INTEGER NOT NULL
    );
""")

# Clear any existing data
cur.execute("DELETE FROM orders; DELETE FROM activities; DELETE FROM products; DELETE FROM users;")
conn.commit()

# Insert users
users = []
for _ in range(20):  # Exactly 20 users
    username = fake.user_name()
    email = fake.email()
    users.append((username, email))

cur.executemany("""
    INSERT INTO users (username, email) VALUES (%s, %s)
    ON CONFLICT (username) DO NOTHING;
""", users)
conn.commit()

# Insert products
products = []
for _ in range(15):  # Exactly 15 products
    product_name = fake.word().capitalize() + " " + fake.word().capitalize()
    price = round(random.uniform(10, 100), 2)
    products.append((product_name, price))

cur.executemany("""
    INSERT INTO products (product_name, price) VALUES (%s, %s);
""", products)
conn.commit()

# Fetch user and product IDs
cur.execute("SELECT user_id FROM users;")
user_ids = [row[0] for row in cur.fetchall()]
cur.execute("SELECT product_id FROM products;")
product_ids = [row[0] for row in cur.fetchall()]

# Insert activities
activities = []
for _ in range(20):  # Exactly 20 activities
    user_id = random.choice(user_ids)
    activity_type = random.choice(['login', 'logout', 'view_product', 'add_to_cart'])
    activity_date = fake.date_time_between(start_date='-30d', end_date='now')
    activities.append((user_id, activity_type, activity_date))

cur.executemany("""
    INSERT INTO activities (user_id, activity_type, activity_date) VALUES (%s, %s, %s);
""", activities)
conn.commit()

# Insert orders
orders = []
for _ in range(20):  # Exactly 20 orders
    user_id = random.choice(user_ids)
    product_id = random.choice(product_ids)
    order_date = fake.date_time_between(start_date='-30d', end_date='now')
    quantity = random.randint(1, 5)
    orders.append((user_id, product_id, order_date, quantity))

cur.executemany("""
    INSERT INTO orders (user_id, product_id, order_date, quantity) VALUES (%s, %s, %s, %s);
""", orders)
conn.commit()

print("Tables created and data populated successfully!")

cur.close()
conn.close()
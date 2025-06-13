import psycopg2
import redis
from datetime import datetime

# PostgreSQL connection config
pg_conn = psycopg2.connect(
    dbname='user_activity',
    user='postgres',
    password='genci1',
    host='localhost',
    port=5433
)

# Redis connection config
redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True, socket_timeout=5, socket_connect_timeout=5)

def fetch_users():
    with pg_conn.cursor() as cur:
        cur.execute("SELECT user_id, username, email FROM users;")
        return cur.fetchall()

def fetch_products():
    with pg_conn.cursor() as cur:
        cur.execute("SELECT product_id, product_name, price FROM products;")
        return cur.fetchall()

def fetch_activities():
    with pg_conn.cursor() as cur:
        cur.execute("SELECT user_id, activity_type, activity_date FROM activities;")
        return cur.fetchall()

def fetch_orders():
    with pg_conn.cursor() as cur:
        cur.execute("SELECT order_id, user_id, product_id, order_date, quantity FROM orders;")
        return cur.fetchall()

def migrate_to_redis():
    try:
        redis_client.ping()
        print("Connected to Redis successfully.")
    except redis.ConnectionError as e:
        print(f"Redis connection failed: {e}")
        exit(1)

    # Clear existing Redis data
    redis_client.flushdb()
    print("Cleared existing Redis data.")

    # Migrate users
    users = fetch_users()
    for user in users:
        user_id, username, email = user
        redis_client.hset(f"user:{user_id}", mapping={
            "username": username,
            "email": email
        })
    print(f"Migrated {len(users)} users to Redis.")

    # Migrate products
    products = fetch_products()
    for product in products:
        product_id, product_name, price = product
        redis_client.hset(f"product:{product_id}", mapping={
            "name": product_name,
            "price": str(price)
        })
    print(f"Migrated {len(products)} products to Redis.")

    # Migrate activities
    activities = fetch_activities()
    for activity in activities:
        user_id, activity_type, activity_date = activity
        redis_client.lpush(f"user:{user_id}:activities", f"{activity_type}:{activity_date}")
    print(f"Migrated {len(activities)} activities to Redis.")

    # Migrate orders
    orders = fetch_orders()
    for order in orders:
        order_id, user_id, product_id, order_date, quantity = order
        redis_client.hset(f"order:{order_id}", mapping={
            "user_id": str(user_id),
            "product_id": str(product_id),
            "order_date": str(order_date),
            "quantity": str(quantity)
        })
    print(f"Migrated {len(orders)} orders to Redis.")

if __name__ == "__main__":
    try:
        migrate_to_redis()
    except Exception as e:
        print(f"Migration failed: {e}")
    finally:
        pg_conn.close()
import os
import time
from sqlalchemy import create_engine

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./dev.db")

def wait_for_db(url, retries=20, delay=1):
    for i in range(retries):
        try:
            engine = create_engine(url)
            with engine.connect():
                print("Database available")
                return True
        except Exception as e:
            print(f"Waiting for database ({i+1}/{retries})... {e}")
            time.sleep(delay)
    return False

if __name__ == '__main__':
    ok = wait_for_db(DATABASE_URL, retries=30, delay=2)
    if not ok:
        print("Could not connect to the database; continuing anyway")
    else:
        print("DB connected")

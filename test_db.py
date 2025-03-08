import psycopg2
from django.conf import settings
import os
import sys
import django

# Set up Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crowd_pulse.settings')
django.setup()

def create_database():
    try:
        # Connect to default PostgreSQL database first
        conn = psycopg2.connect(
            dbname='postgres',
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT']
        )
        conn.autocommit = True
        cur = conn.cursor()
        
        # Check if database exists
        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (settings.DATABASES['default']['NAME'],))
        exists = cur.fetchone()
        
        if not exists:
            print(f"Creating database {settings.DATABASES['default']['NAME']}...")
            cur.execute(f"CREATE DATABASE {settings.DATABASES['default']['NAME']}")
            print("Database created successfully!")
        else:
            print("Database already exists!")
            
        cur.close()
        conn.close()
        return True
        
    except Exception as e:
        print(f"Error creating database: {e}")
        return False

def test_connection():
    try:
        # Get database settings from Django
        db_settings = settings.DATABASES['default']
        
        # Connect to PostgreSQL
        conn = psycopg2.connect(
            dbname=db_settings['NAME'],
            user=db_settings['USER'],
            password=db_settings['PASSWORD'],
            host=db_settings['HOST'],
            port=db_settings['PORT']
        )
        
        # Create a cursor
        cur = conn.cursor()
        
        # Execute a simple query
        cur.execute('SELECT version();')
        
        # Fetch the result
        version = cur.fetchone()
        print("Successfully connected to PostgreSQL!")
        print(f"PostgreSQL version: {version[0]}")
        
        # Close cursor and connection
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"Error connecting to PostgreSQL: {e}")

if __name__ == '__main__':
    if create_database():
        test_connection()
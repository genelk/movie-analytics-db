import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class DatabaseConnector:
    """Handles database connections and operations."""
    
    def __init__(self):
        """Initialize database connector using environment variables."""
        self.conn_params = {
            'dbname': os.getenv('DB_NAME', 'movie_analytics'),
            'user': os.getenv('DB_USER', 'postgres'),
            'password': os.getenv('DB_PASSWORD', ''),
            'host': os.getenv('DB_HOST', 'localhost'),
            'port': os.getenv('DB_PORT', '5432')
        }
        self.conn = None
    
    def connect(self):
        """Connect to PostgreSQL database."""
        try:
            self.conn = psycopg2.connect(**self.conn_params)
            print("Connected to database successfully.")
            return self.conn
        except psycopg2.Error as e:
            print(f"Unable to connect to database: {e}")
            raise
    
    def disconnect(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None
            print("Database connection closed.")
    
    def execute_query(self, query, params=None, fetch=True):
        """Execute a SQL query and return results if applicable."""
        if not self.conn:
            self.connect()
        
        try:
            with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(query, params)
                
                if fetch:
                    return cursor.fetchall()
                else:
                    self.conn.commit()
                    return cursor.rowcount
        except psycopg2.Error as e:
            self.conn.rollback()
            print(f"Query execution failed: {e}")
            raise
    
    def execute_script(self, script_path):
        """Execute a SQL script file."""
        try:
            with open(script_path, 'r') as f:
                script = f.read()
            
            if not self.conn:
                self.connect()
            
            with self.conn.cursor() as cursor:
                cursor.execute(script)
                self.conn.commit()
                print(f"Script {script_path} executed successfully.")
        except (psycopg2.Error, FileNotFoundError) as e:
            if self.conn:
                self.conn.rollback()
            print(f"Script execution failed: {e}")
            raise
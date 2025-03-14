from db_connector import DatabaseConnector
import pandas as pd
import sys

def run_query(query):
    """Run a SQL query and display results."""
    connector = DatabaseConnector()
    
    try:
        # Connect to database
        connector.connect()
        
        # Execute query
        results = connector.execute_query(query)
        
        # Convert to pandas DataFrame for nice display
        if results:
            df = pd.DataFrame(results)
            print(f"\nQuery results ({len(results)} rows):")
            print(df)
            return df
        else:
            print("Query returned no results.")
            return None
            
    except Exception as e:
        print(f"Query failed: {e}")
        return None
    
    finally:
        # Close connection
        connector.disconnect()

if __name__ == "__main__":
    # Get query from command line argument or use default query
    if len(sys.argv) > 1:
        query = sys.argv[1]
    else:
        query = """
        SELECT 
            title, 
            release_year, 
            vote_average, 
            popularity 
        FROM 
            movies 
        ORDER BY 
            vote_average DESC 
        LIMIT 10
        """
    
    print(f"Executing query:\n{query}")
    run_query(query)
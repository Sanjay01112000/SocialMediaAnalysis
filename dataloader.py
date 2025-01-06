rom cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import pandas as pd
from datetime import datetime
import uuid
import os

class DataLoader:
    def __init__(self, secure_bundle_path, client_id, client_secret):
        cloud_config = {
            'secure_connect_bundle': secure_bundle_path
        }
        auth_provider = PlainTextAuthProvider(client_id, client_secret)
        self.cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
        self.session = self.cluster.connect()
        
    def setup_database(self):
        self.session.execute("""
            CREATE KEYSPACE IF NOT EXISTS default_keyspace
            WITH replication = {'class': 'NetworkTopologyStrategy', 'datacenter1': 3}
        """)
        
        self.session.execute("""
            CREATE TABLE IF NOT EXISTS default_keyspace.post_analysis_data (
                post_id uuid PRIMARY KEY,
                post_type text,
                timestamp timestamp,
                likes int,
                shares int,
                comments int,
                reach int,
                engagement_rate float
            )
        """)
        print("Database setup completed")
    
    def process_and_load_data(self, excel_path, limit=200):
        # Read Excel file
        df = pd.read_excel(excel_path)
        df = df.head(limit)
        
        # Map post types to our schema
        post_type_mapping = {
            'Video': 'reel',
            'Image': 'static',
            'Carousel': 'carousel',
            'Link': 'static'
        }
        
        # Create a list to store processed data
        processed_data = []
        
        # Process data
        for _, row in df.iterrows():
            # Convert timestamp string to datetime
            try:
                timestamp = pd.to_datetime(row['Post Timestamp'])
            except:
                timestamp = datetime.now()
            
            # Map post type
            post_type = post_type_mapping.get(row['Post Type'], 'static')
            
            # Create post_id
            post_id = uuid.UUID(row['Post ID']) if isinstance(row['Post ID'], str) else uuid.uuid4()
            
            # Append processed data
            processed_data.append({
                'post_id': str(post_id),
                'post_type': post_type,
                'timestamp': timestamp,
                'likes': int(row['Likes']),
                'comments': int(row['Comments']),
                'shares': int(row['Shares']),
                'reach': int(row['Reach']),
                'engagement_rate': float(row['Engagement Rate'])
            })
        
        # Create DataFrame and save to CSV
        processed_df = pd.DataFrame(processed_data)
        csv_filename = f'processed_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        processed_df.to_csv(csv_filename, index=False)
        print(f"Processed data saved to {csv_filename}")
        
        # Prepare insert statement and load to database
        insert_query = self.session.prepare("""
            INSERT INTO default_keyspace.post_analysis_data 
            (post_id, post_type, timestamp, likes, comments, shares, reach, engagement_rate)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """)
        
        # Insert data into database
        for data in processed_data:
            self.session.execute(insert_query, [
                uuid.UUID(data['post_id']),
                data['post_type'],
                data['timestamp'],
                data['likes'],
                data['comments'],
                data['shares'],
                data['reach'],
                data['engagement_rate']
            ])
    
    def close(self):
        self.cluster.shutdown()

def main():
    SECURE_BUNDLE_PATH = os.environ.get("SECURE_BUNDLE_PATH")
    CLIENT_ID = os.environ.get("CLIENT_ID")
    CLIENT_SECRET =  os.environ.get("CLIENT_SECRET")
    EXCEL_FILE_PATH =  os.environ.get("EXCEL_FILE_PATH")
    
    try:
        loader = DataLoader(SECURE_BUNDLE_PATH, CLIENT_ID, CLIENT_SECRET)
        # loader.setup_database()
        loader.process_and_load_data(EXCEL_FILE_PATH)
        print("Data import completed successfully")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        loader.close()

if __name__ == "__main__":
    main()
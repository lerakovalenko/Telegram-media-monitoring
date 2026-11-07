import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
    )

def get_or_create_channel(channel_username, title):
    """Returns the channel ID from the database. If the channel does not exist, it creates it."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True) 
    
    select_query = "SELECT id FROM channels WHERE channel_username = %s"
    cursor.execute(select_query, (channel_username,))
    result = cursor.fetchone()
    
    if result:
        channel_id = result['id']
    else:
        insert_query = "INSERT INTO channels (channel_username, title) VALUES (%s, %s)"
        cursor.execute(insert_query, (channel_username, title))
        conn.commit()
        channel_id = cursor.lastrowid 
        
    cursor.close()
    conn.close()
    return channel_id

def save_post(channel_id, telegram_post_id, text, views, published_at):
    """Saves the post to DB. Ignores duplicates."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    insert_query = """
        INSERT IGNORE INTO posts 
        (channel_id, telegram_post_id, text, views, published_at) 
        VALUES (%s, %s, %s, %s, %s)
    """
    
    cursor.execute(insert_query, (channel_id, telegram_post_id, text, views, published_at))
    conn.commit()
    
    inserted_rows = cursor.rowcount
    
    cursor.close()
    conn.close()
    return inserted_rows > 0

def save_search_query(query_text: str) -> int:
    """Сохраняет искомый текст новости."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO search_queries (query_text) VALUES (%s)", (query_text,))
    conn.commit()
    query_id = cursor.lastrowid
    cursor.close()
    conn.close()
    return query_id

def save_matches_with_original(query_id: int, matches_data: list) -> int:
    """Saves the posts it finds and marks the earliest one as the original source."""
    if not matches_data:
        return 0
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    insert_query = """
        INSERT IGNORE INTO matches 
        (query_id, post_id, similarity_score, match_type, is_original)
        VALUES (%s, %s, %s, %s, %s)
    """
    
    records_to_insert = []
    for idx, match in enumerate(matches_data):
        score = match['similarity_score']
        
        if score >= 0.8:
            match_type = 'exact'
        elif score >= 0.3:
            match_type = 'rewrite'
        else:
            match_type = 'mention'
            
        is_original = True if idx == 0 else False
        
        records_to_insert.append((query_id, match['post_id'], score, match_type, is_original))
        
    cursor.executemany(insert_query, records_to_insert)
    conn.commit()
    saved_count = cursor.rowcount
    cursor.close()
    conn.close()
    return saved_count

if __name__ == "__main__":
    try:
        conn = get_db_connection()
        print("Succesfully connected to MySQL!")
        conn.close()
    except Exception as e:
        print(f"Connecting error: {e}")
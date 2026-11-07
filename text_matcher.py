from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from db import get_db_connection
from nlp_utils import preprocess_text

def get_all_posts_from_db():
    """Loads all posts from the MySQL database."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    
    query = """
        SELECT p.id, p.telegram_post_id, p.text, p.published_at, c.title as channel_title 
        FROM posts p
        JOIN channels c ON p.channel_id = c.id
    """
    cursor.execute(query)
    posts = cursor.fetchall()
    
    cursor.close()
    conn.close()
    return posts

def find_similar_posts(query_text: str, similarity_threshold: float = 0.2):
    """
    Searches posts similar to query_text.
    similarity_threshold — minimal similarity threshold (from 0.0 to 1.0).
    """
    posts = get_all_posts_from_db()
    if not posts:
        print("DB is empty.")
        return []

    cleaned_query = preprocess_text(query_text)
    cleaned_posts = [preprocess_text(p['text']) for p in posts]

    # Compile a single array of texts: [0] is the search query, [1..N] are posts from DB
    corpus = [cleaned_query] + cleaned_posts

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)
    cosine_similarities = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

    results = []
    for index, score in enumerate(cosine_similarities):
        if score >= similarity_threshold:
            post_data = posts[index]
            results.append({
                'post_id': post_data['id'],
                'channel_title': post_data['channel_title'],
                'text': post_data['text'],
                'published_at': post_data['published_at'],
                'similarity_score': round(float(score), 4)
            })

    results.sort(key=lambda x: x['similarity_score'], reverse=True)
    return results

if __name__ == "__main__":
    #Example
    search_phrase = "загроза БПЛА у Києві та областях, де оголошено тривогу"
    
    print(f"Search for matches for the phrase: '{search_phrase}'\n" + "="*50)
    matches = find_similar_posts(search_phrase, similarity_threshold=0.1)

    for idx, match in enumerate(matches, 1):
        print(f"{idx}. Channel: {match['channel_title']} | Similarity: {match['similarity_score'] * 100:.1f}%")
        print(f"   Data: {match['published_at']}")
        print(f"   Text: {match['text'][:150]}...")
        print("-" * 50)
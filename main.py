import sys
from text_matcher import find_similar_posts
from db import save_search_query, save_matches_with_original

def analyze_news_source(target_news_text: str, similarity_threshold: float = 0.20):
    print("=" * 70)
    print("NEWS SOURCE ANALYZER")
    print("=" * 70)
    print(f" News to search for:\n\"{target_news_text}\"\n")
    
    # Search starting
    print("🔍Searching for similar records in the MySQL-DB...")
    raw_matches = find_similar_posts(target_news_text, similarity_threshold=similarity_threshold)
    
    if not raw_matches:
        print("❌ Similar news items were not found.")
        return

    # Chronological sorting
    sorted_matches = sorted(raw_matches, key=lambda x: x['published_at'])
    
    original_post = sorted_matches[0]
    total_found = len(sorted_matches)
    
    query_id = save_search_query(target_news_text)
    save_matches_with_original(query_id, sorted_matches)

    print(f" Posts found: {total_found}")
    print("\n" + "🏆 ORIGINAL SOURCE " + "="*45)
    print(f"📌 Channel:       {original_post['channel_title']}")
    print(f"⏰ Date: {original_post['published_at']} UTC")
    print(f"📊 Similarity:    {original_post['similarity_score'] * 100:.1f}%")
    print(f"📝 Text:       {original_post['text'][:200]}...")
    print("=" * 70)
    
    # Spread Pattern
    if total_found > 1:
        print("\n Who Shared the News Next:")
        for idx, match in enumerate(sorted_matches[1:], start=2):
            
            time_delay = match['published_at'] - original_post['published_at']
            hours, remainder = divmod(int(time_delay.total_seconds()), 3600)
            minutes, _ = divmod(remainder, 60)
            
            print(f"\n{idx}. Channel: {match['channel_title']}")
            print(f"   Time: {match['published_at']} (after {hours}h {minutes}m after original source)")
            print(f"   Type:   {match['similarity_score'] * 100:.1f}% similarity")
            print(f"   Text: {match['text'][:120]}...")


if __name__ == "__main__":
    print("=" * 70)
    print(" MONITORING AND SOURCE TRACING SYSTEM")
    print("=" * 70)
    
    user_input = input("\nEnter the text of a news article, a quote, or a key point to search for: ").strip()
    
    if not user_input:
        print(" Error: You did not enter any search text. Log out.")
        sys.exit()
        
    analyze_news_source(user_input, similarity_threshold=0.20)
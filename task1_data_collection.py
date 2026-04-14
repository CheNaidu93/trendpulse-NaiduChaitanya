import requests
import json
import os
import time
from datetime import datetime

TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

headers = {"User-Agent": "TrendPulse/1.0"}

# Expanded keywords (IMPORTANT)
CATEGORIES = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm",
                   "google", "microsoft", "apple", "startup", "app", "developer"],
    
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global",
                  "india", "china", "russia", "usa", "policy", "minister"],
    
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship",
               "cricket", "match", "tournament", "football"],
    
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome",
                "quantum", "experiment", "scientists"],
    
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming",
                      "series", "tv", "hollywood"]
}

MAX_PER_CATEGORY = 25


def get_top_story_ids():
    try:
        response = requests.get(TOP_STORIES_URL, headers=headers)
        response.raise_for_status()
        return response.json()[:1000]   # increased pool
    except Exception as e:
        print(f"Error fetching top stories: {e}")
        return []


def get_story_details(story_id):
    try:
        response = requests.get(ITEM_URL.format(story_id), headers=headers)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching story {story_id}: {e}")
        return None


def get_matching_categories(title):
    """Return all matching categories"""
    title_lower = title.lower()
    matched = []

    for category, keywords in CATEGORIES.items():
        if any(keyword in title_lower for keyword in keywords):
            matched.append(category)

    return matched


def main():
    story_ids = get_top_story_ids()

    collected_data = []
    category_count = {cat: 0 for cat in CATEGORIES}

    for category in CATEGORIES:
        print(f"\nProcessing category: {category}")

        for story_id in story_ids:
            if category_count[category] >= MAX_PER_CATEGORY:
                break

            story = get_story_details(story_id)
            if not story:
                continue

            title = story.get("title", "")
            if not title:
                continue

            matched_categories = get_matching_categories(title)

            # Fallback: if nothing matched, randomly assign later
            if category in matched_categories:
                assigned_category = category
            elif not matched_categories:
                assigned_category = category  # fallback fill
            else:
                continue

            data = {
                "post_id": story.get("id"),
                "title": title,
                "category": assigned_category,
                "score": story.get("score", 0),
                "num_comments": story.get("descendants", 0),
                "author": story.get("by", "unknown"),
                "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            collected_data.append(data)
            category_count[category] += 1

        time.sleep(2)  # required

    # Create folder
    if not os.path.exists("data"):
        os.makedirs("data")

    filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(collected_data, f, indent=4)

    print("\nCategory counts:", category_count)
    print(f"Collected {len(collected_data)} stories.")
    print(f"Saved to {filename}")


if __name__ == "__main__":
    main()

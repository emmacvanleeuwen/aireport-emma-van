"""
Manages podcast feeds and episode retrieval
"""
import feedparser
from datetime import datetime, timedelta
from typing import List, Dict

class PodcastManager:
      def __init__(self):
                self.podcasts = {}

    def add_podcast(self, podcast_id: str, rss_url: str, name: str):
              """Add a new podcast to track"""
              self.podcasts[podcast_id] = {
                  "url": rss_url,
                  "name": name,
                  "episodes": []
              }

    def fetch_episodes(self, podcast_id: str, days: int = 7) -> List[Dict]:
              """
                      Fetch episodes from the last N days
                              Returns: List of episodes with title, description, date
                                      """
              if podcast_id not in self.podcasts:
                            raise ValueError(f"Podcast {podcast_id} not found")

              podcast = self.podcasts[podcast_id]
              feed = feedparser.parse(podcast["url"])

        episodes = []
        cutoff_date = datetime.now() - timedelta(days=days)

        for entry in feed.entries[:20]:
                      try:
                                        pub_date = datetime(*entry.published_parsed[:6])

                if pub_date > cutoff_date:
                                      description = entry.description if hasattr(entry, 'description') else ""
                                      if not description and hasattr(entry, 'summary'):
                                                                description = entry.summary

                                      episodes.append({
                                          "title": entry.title,
                                          "description": description[:500],
                                          "published": pub_date,
                                          "link": entry.link if hasattr(entry, 'link') else "",
                                          "podcast": podcast["name"]
                                      })
except Exception as e:
                print(f"Error parsing episode: {e}")
                continue

        return sorted(episodes, key=lambda x: x["published"], reverse=True)

    def fetch_all_episodes(self, days: int = 7) -> Dict[str, List]:
              """Fetch episodes from all podcasts"""
              all_episodes = {}
              for podcast_id in self.podcasts:
                            try:
                                              all_episodes[podcast_id] = self.fetch_episodes(podcast_id, days)
except Exception as e:
                print(f"Error fetching {podcast_id}: {e}")
                all_episodes[podcast_id] = []

        return all_episodes

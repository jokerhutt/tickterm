# ∴ Jokerhut / models/news_item.py


from dataclasses import dataclass

@dataclass
class NewsItem:
    title: str
    source: str
    published: str

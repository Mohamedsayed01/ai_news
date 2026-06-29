from flask import Flask, render_template, request, jsonify
import feedparser
from bs4 import BeautifulSoup
from email.utils import parsedate_to_datetime
from utils.summarizer import summarize_with_gemini, research_topic
from utils.fetcher import fetch_article_text

app = Flask(__name__)

CATEGORIES = {
    "World": [
        "https://feeds.bbci.co.uk/news/world/rss.xml",
        "https://www.aljazeera.com/xml/rss/all.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",
    ],
    "Business": [
        "https://feeds.bbci.co.uk/news/business/rss.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/Business.xml",
        "https://www.theguardian.com/uk/business/rss",
    ],
    "Technology": [
        "https://techcrunch.com/feed/",
        "https://www.theverge.com/rss/index.xml",
        "https://feeds.wired.com/wired/index",
    ],
    "Sports": [
        "https://www.goal.com/en/rss/news",
        "https://feeds.bbci.co.uk/sport/rss.xml",
        "https://www.espn.com/espn/rss/news",
    ],
    "Politics": [
        "https://feeds.reuters.com/reuters/politicsNews",
        "https://www.politico.com/rss/politics.xml",
        "https://rss.nytimes.com/services/xml/rss/nyt/Politics.xml",
    ],
    "Science": [
        "https://feeds.sciencedaily.com/sciencedaily/top_news",
        "https://www.science.org/rss/news_current.xml",
    ],
}

def clean_text(html, max_len=350):
    text = BeautifulSoup(html or "", "html.parser").get_text(strip=True)
    text = text.replace('"', "&quot;").replace("'", "&#39;")
    return (text[:max_len] + "…") if len(text) > max_len else text

def fmt_date(pub_str):
    try:
        dt = parsedate_to_datetime(pub_str)
        return dt.strftime("%b %d, %Y · %H:%M"), dt.isoformat()
    except Exception:
        return (pub_str[:20] if pub_str else "Recently"), (pub_str or "")

def parse_articles(feed_url, category, search_query=None):
    articles = []
    try:
        feed = feedparser.parse(feed_url)
        for entry in feed.entries[:12]:
            title = entry.get("title", "").strip()
            if not title:
                continue
            raw_desc = entry.get("description", entry.get("summary", ""))
            desc = clean_text(raw_desc, 350)
            safe_title = title.replace('"', "&quot;").replace("'", "&#39;")
            link = entry.get("link", "#")
            pub_fmt, pub_sort = fmt_date(entry.get("published", entry.get("pubDate", "")))

            if search_query:
                q = search_query.lower()
                if q not in title.lower() and q not in desc.lower():
                    continue

            articles.append({
                "title": safe_title,
                "raw_title": title,
                "link": link,
                "published": pub_fmt,
                "pub_sort": pub_sort,
                "description": desc or "Read the full article for details.",
                "category": category,
            })
    except Exception as e:
        print(f"[rss] Error fetching {feed_url}: {e}")
    return articles

def get_latest_news(category, limit=18, search_query=None):
    if category not in CATEGORIES:
        return []
    all_articles = []
    for url in CATEGORIES[category]:
        all_articles.extend(parse_articles(url, category, search_query))
    seen, unique = set(), []
    for a in all_articles:
        if a["title"] not in seen:
            seen.add(a["title"])
            unique.append(a)
    unique.sort(key=lambda x: x["pub_sort"], reverse=True)
    return unique[:limit]

def search_all_categories(query, limit=30):
    all_articles = []
    for cat, feeds in CATEGORIES.items():
        for url in feeds:
            all_articles.extend(parse_articles(url, cat, query))
    seen, unique = set(), []
    for a in all_articles:
        if a["title"] not in seen:
            seen.add(a["title"])
            unique.append(a)
    unique.sort(key=lambda x: x["pub_sort"], reverse=True)
    return unique[:limit]

# ── Routes ───────────────────────────────────────────────────────────
@app.route("/")
def home():
    return render_template("index.html", categories=CATEGORIES.keys())

@app.route("/category/<cat>")
def category(cat):
    if cat not in CATEGORIES:
        return render_template("404.html"), 404
    q = request.args.get("search", "").strip()
    articles = get_latest_news(cat, search_query=q or None)
    return render_template("category.html", category=cat, articles=articles, search_query=q)

@app.route("/search")
def search():
    q = request.args.get("q", "").strip()
    articles = search_all_categories(q) if q else []
    return render_template("search.html", articles=articles, query=q)

@app.route("/about")
def about():
    return render_template("about.html")

# ── API ──────────────────────────────────────────────────────────────
@app.route("/api/summarize", methods=["POST"])
def summarize():
    data = request.get_json(silent=True) or {}
    url  = data.get("url", "#")
    desc = data.get("description", "")

    full_text = fetch_article_text(url) if url != "#" else ""
    text = full_text if len(full_text) > 200 else desc

    if not text:
        return jsonify({"error": "No content"}), 400

    print(f"[summarize] text_len={len(text)} used_full={bool(full_text)}")
    summary = summarize_with_gemini(text)
    print(f"[summarize] summary_len={len(summary)} preview={repr(summary[:100])}")

    return jsonify({"summary": summary, "original_url": url, "used_full": bool(full_text)})

@app.route("/api/research", methods=["POST"])
def research():
    data  = request.get_json(silent=True) or {}
    topic = data.get("topic", "").strip()
    if not topic:
        return jsonify({"error": "No topic"}), 400
    return jsonify({"briefing": research_topic(topic), "topic": topic})

# ── Error handlers ───────────────────────────────────────────────────
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(500)
def server_error(e):
    return render_template("500.html"), 500

if __name__ == "__main__":
    print("🚀 SnapNews running → http://127.0.0.1:5000")
    app.run(debug=True)

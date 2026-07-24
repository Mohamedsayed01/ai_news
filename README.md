# 📰 SnapNews — AI-Powered News Aggregator

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue?logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/Flask-Web%20App-black?logo=flask">
  <img src="https://img.shields.io/badge/Gemini-AI%20Summarization-8E75B2?logo=google">
  <img src="https://img.shields.io/badge/RSS-Live%20Feeds-orange">
  <img src="https://img.shields.io/badge/License-MIT-green">
</p>

<p align="center">
  <b>All the news that matters, summarized in seconds.</b><br>
  A Flask web app that pulls live headlines from trusted RSS sources and uses AI to summarize
  and research any story on demand.
</p>

---

## 📖 About

**SnapNews** is a real-time news aggregator built with **Flask**. Instead of relying on a single
outlet, it pulls live articles from multiple trusted RSS feeds — BBC, Al Jazeera, The New York
Times, TechCrunch, The Verge, ESPN, and more — and organizes them into clean, browsable
categories.

What sets it apart is its AI layer: powered by **Google Gemini**, SnapNews can instantly
summarize any article's full text, or generate a quick research briefing on any topic you type
in — turning a page full of headlines into something you can actually act on.

---

## 🖼️ Screenshots

<p align="center">
  <img src=""Screenshots/home.png"" alt="SnapNews Home Page" width="800"/>
  <br><i>Home page</i>
</p>

<p align="center">
  <img src=""Screenshots/Summarize Page.png"" alt="SnapNews Category / Article View" width="800"/>
  <br><i>Category view</i>
</p>

---

## ✨ Features

- 📡 **Live RSS aggregation** from multiple trusted sources per category (BBC, Al Jazeera, NYT, TechCrunch, The Verge, Wired, Reuters, Politico, ESPN, Goal, Science.org, ScienceDaily, and more).
- 🗂️ **Six curated categories** — World, Business, Technology, Sports, Politics, and Science.
- 🔍 **Full-text search** across a single category or across all categories at once.
- 🤖 **AI article summarization** — fetches the full article text and summarizes it with Gemini in one click.
- 🧠 **AI topic research** — type any topic and get an instant AI-generated briefing.
- 🧹 **Clean, deduplicated feeds** — articles are deduplicated by title and sorted by publish date automatically.
- ⚠️ **Custom error pages** for 404 and 500 errors.

---

## 🛠️ Tech Stack

| Category | Technology |
|---|---|
| Backend | Python, Flask |
| News feeds | `feedparser` (RSS parsing) |
| Content extraction | `requests`, `BeautifulSoup4`, `lxml` |
| AI | Google Gemini (`google-generativeai`) |
| Config | `python-dotenv` |
| Frontend | HTML, CSS, JavaScript (Jinja2 templates) |

---

## 📂 Project Structure

```
ai_news/
├── static/                  # CSS / JS / image assets
├── templates/                # HTML pages (Jinja2)
│   ├── index.html
│   ├── category.html
│   ├── search.html
│   ├── about.html
│   ├── 404.html
│   └── 500.html
├── utils/
│   ├── summarizer.py         # Gemini-powered summarization & topic research
│   └── fetcher.py            # Full article text extraction
├── app.py                   # App entry point, RSS parsing & all routes
└── requirements.txt
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.x
- pip
- A [Google Gemini API key](https://ai.google.dev/) (for the AI summarization & research features)

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/Mohamedsayed01/ai_news.git
cd ai_news

# 2. (Optional but recommended) create a virtual environment
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up your environment variables
# Create a .env file in the project root:
echo "GEMINI_API_KEY=your_api_key_here" > .env

# 5. Run the app
python app.py
```

Then open your browser at:
```
http://127.0.0.1:5000
```

---

## 🖥️ Usage

1. Browse the home page to see all available news categories.
2. Click into a category (**World**, **Business**, **Technology**, **Sports**, **Politics**, **Science**) to see the latest headlines from multiple sources at once.
3. Use the **search bar** to look for a specific topic within a category or across all of them.
4. Click **Summarize** on any article to get an instant AI-generated summary.
5. Use the **Research** feature to type any topic and get a quick AI-written briefing.

---

## 🗺️ Roadmap

- [ ] Add more RSS sources and categories.
- [ ] Cache feed results to reduce load time and repeated requests.
- [ ] Add user accounts to save favorite articles.
- [ ] Deploy the project (Render / Railway / Heroku).

---

## 🤝 Contributing

Contributions are welcome! To contribute:

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — feel free to use and build on it, with attribution.

---

## 👤 Author

**Mohamed Sayed**
🔗 [linkedIn](https://www.linkedin.com/in/m0hamed-sayed)

---

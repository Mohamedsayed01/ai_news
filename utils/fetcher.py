import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}

# Selectors per domain for best extraction
DOMAIN_SELECTORS = {
    "bbc.co.uk":      ["article", "[data-component='text-block']"],
    "bbc.com":        ["article", "[data-component='text-block']"],
    "theguardian.com":["article", ".article-body-commercial-selector", "div[itemprop='articleBody']"],
    "nytimes.com":    ["article", "section[name='articleBody']", ".StoryBodyCompanionColumn"],
    "aljazeera.com":  ["article", ".wysiwyg", ".article-p"],
    "theverge.com":   ["article", ".duet--article--article-body-component"],
    "techcrunch.com": ["article", ".article-content", ".entry-content"],
    "wired.com":      ["article", "[class*='body__container']"],
    "reuters.com":    ["article", "[class*='article-body']"],
    "politico.com":   ["article", ".story-text", ".content-group"],
    "espn.com":       ["article", ".article-body", ".Story__Body"],
    "sciencedaily.com":["#story_text", "article"],
    "science.org":    ["article", ".article__body"],
    "goal.com":       ["article", ".article-body"],
}

NOISE_TAGS = [
    "script", "style", "nav", "header", "footer", "aside",
    "figure", "figcaption", "iframe", "form", "button",
    "[class*='ad']", "[class*='cookie']", "[class*='subscribe']",
    "[class*='newsletter']", "[class*='related']", "[class*='sidebar']",
]

def get_domain(url: str) -> str:
    from urllib.parse import urlparse
    host = urlparse(url).netloc.lower()
    return host.replace("www.", "")

def fetch_article_text(url: str, timeout: int = 8) -> str:
    """
    Fetch and extract clean article text from a URL.
    Returns empty string on failure.
    """
    try:
        resp = requests.get(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
        if resp.status_code != 200:
            return ""

        soup = BeautifulSoup(resp.text, "html.parser")

        # Remove noise elements
        for sel in NOISE_TAGS:
            for el in soup.select(sel):
                el.decompose()

        # Try domain-specific selectors first
        domain = get_domain(url)
        selectors = DOMAIN_SELECTORS.get(domain, [])

        # Generic fallbacks
        selectors += [
            "article",
            "[itemprop='articleBody']",
            "[class*='article-body']",
            "[class*='story-body']",
            "[class*='post-body']",
            "[class*='entry-content']",
            "[class*='article-content']",
            "main",
        ]

        text = ""
        for sel in selectors:
            el = soup.select_one(sel)
            if el:
                candidate = el.get_text(separator="\n", strip=True)
                if len(candidate) > 300:
                    text = candidate
                    break

        # Last resort: full body
        if not text:
            text = soup.get_text(separator="\n", strip=True)

        # Clean up excessive whitespace
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        text = "\n".join(lines)

        return text[:6000]

    except Exception as e:
        print(f"[fetcher] Failed to fetch {url}: {e}")
        return ""

import datetime
import json
import feedparser
import requests

# Optional: Paste your Google Sheet Web App URL here later
GOOGLE_SHEET_WEBHOOK_URL = ""

SOURCES = {
    "ATD_News": "https://www.td.org/rss/news",
    "ELearningIndustry": "https://elearningindustry.com/feed",
    "ChiefLearningOfficer": "https://www.chieflearningofficer.com/feed/",
    "TrainingIndustry": "https://trainingindustry.com/feed/",
}

LD_KEYWORDS = [
    "learning and development",
    "upskilling",
    "reskilling",
    "ai in learning",
    "microlearning",
    "lms",
    "lxp",
    "instructional design",
    "workforce development",
    "leadership training",
    "capability building",
]


def run_scraper():
    print("Initializing Zero-Cost Global L&D Scraper...")
    all_articles = []

    for name, url in SOURCES.items():
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries:
                title = entry.get("title", "")
                link = entry.get("link", "")
                published = entry.get(
                    "published", str(datetime.date.today())
                )
                summary = entry.get("summary", "")

                content = f"{title} {summary}".lower()
                if any(kw in content for kw in LD_KEYWORDS):
                    all_articles.append(
                        {
                            "Source": name,
                            "Title": title,
                            "URL": link,
                            "Date": published,
                        }
                    )
        except Exception as e:
            print(f"Error reading {name}: {e}")

    # Save locally in repository
    with open("ld_latest_updates.json", "w", encoding="utf-8") as f:
        json.dump(all_articles, f, ensure_ascii=False, indent=4)

    # Post to Google Sheet if configured
    if GOOGLE_SHEET_WEBHOOK_URL and "script.google.com" in GOOGLE_SHEET_WEBHOOK_URL:
        try:
            response = requests.post(
                GOOGLE_SHEET_WEBHOOK_URL,
                data=json.dumps(all_articles),
                headers={"Content-Type": "application/json"},
            )
            print(f"Sent to Google Sheets! Status: {response.status_code}")
        except Exception as e:
            print(f"Failed to post to Google Sheets: {e}")

    print(
        f"Success! Scraped {len(all_articles)} relevant L&D updates worldwide."
    )


if __name__ == "__main__":
    run_scraper()

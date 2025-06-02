# Crypto Exchange News Crawler

A Scrapy-based web crawler designed to collect announcement news from various cryptocurrency exchanges. This project currently supports Bitfinex exchange and can be easily extended to include other exchanges.

## Project Description

This project crawls announcement news from cryptocurrency exchanges to help users stay updated with the latest developments, updates, and announcements from major crypto trading platforms. The crawler extracts key information including:

- News title and description
- Publication timestamp
- News URL
- Exchange source
- Unique news ID

## Currently Supported Exchanges

- **Bitfinex** - The first implemented exchange spider

## Features

- **Scalable Architecture**: Built with Scrapy framework for easy extension to multiple exchanges
- **Rate Limiting**: Configured with appropriate delays to respect exchange servers
- **Data Export**: Supports JSON output format
- **Pagination Support**: Automatically crawls multiple pages of news
- **User Agent Rotation**: Uses multiple user agents to avoid detection
- **Configurable Settings**: Easy to adjust crawling parameters

## Project Structure

```
crytpo_exchange_news/
├── scrapy.cfg                 # Scrapy configuration
├── crytpo_exchange_news/
│   ├── __init__.py
│   ├── items.py              # Data models
│   ├── middlewares.py        # Custom middlewares
│   ├── pipelines.py          # Data processing pipelines
│   ├── settings.py           # Project settings
│   └── spiders/
│       ├── __init__.py
│       └── bitfinex.py       # Bitfinex exchange spider
└── requirements.txt          # Python dependencies
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd crytpo_exchange_news
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Running the Bitfinex Spider

To crawl news from Bitfinex:

```bash
scrapy crawl bitfinex
```

### Export to JSON

To save the crawled data to a JSON file:

```bash
scrapy crawl bitfinex -o output.json
```

### Custom Settings

You can override settings from the command line:

```bash
scrapy crawl bitfinex -s MAX_PAGE=5 -s DOWNLOAD_DELAY=2
```

## Configuration

Key settings in `settings.py`:

- `MAX_PAGE`: Maximum number of pages to crawl (default: 2)
- `DOWNLOAD_DELAY`: Delay between requests in seconds (default: 3)
- `CONCURRENT_REQUESTS`: Number of concurrent requests (default: 8)
- `USER_AGENT`: List of user agents for rotation

## Data Structure

Each news item contains the following fields:

```json
{
    "title": "News headline",
    "desc": "News description/content",
    "url": "Full URL to the news article",
    "category_str": "News category (if available)",
    "exchange": "Exchange name (e.g., 'bitfinex')",
    "news_id": "Unique identifier from the exchange",
    "announced_at_timestamp": "Original publication timestamp",
    "timestamp": "Crawl timestamp"
}
```


## Legal Notice

This crawler is designed for educational and research purposes. Please ensure you comply with:

- Each exchange's Terms of Service
- Rate limiting and robots.txt policies
- Applicable data protection laws
- Fair use guidelines

Always use the crawler responsibly and consider the impact on the target servers.


## Support

For issues, questions, or contributions, please create an issue in the repository. 
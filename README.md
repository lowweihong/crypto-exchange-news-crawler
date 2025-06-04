# Crypto Exchange News Crawler

A Scrapy-based web crawler designed to collect announcement news from various cryptocurrency exchanges. This project currently supports Bitfinex and Bitget exchanges and can be easily extended to include other exchanges.

## Project Description

This project crawls announcement news from cryptocurrency exchanges to help users stay updated with the latest developments, updates, and announcements from major crypto trading platforms. The crawler extracts key information including:

- News title and description
- Publication timestamp
- News URL
- Exchange source
- Unique news ID
- News categories (where available)

## Currently Supported Exchanges

- **Bybit**
- **Bitget**
- **XT**
- **Bitfinex** 



## Installation

1. Clone the repository:
```bash
git clone https://github.com/lowweihong/crypto-exchange-news-crawler.git
cd crypto_exchange_news
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

4. Install Playwright browsers (required for Bitget spider):
```bash
playwright install chromium
```

## Usage

### Running the Bitfinex Spider

Supported platform
1. bybit
2. bitget
3. xt
4. bitfinex


Run the below command to crawl:

```bash
scrapy crawl <platform>
```

### Export to JSON

To save the crawled data to a JSON file:

```bash
scrapy crawl bitfinex -o bitfinex_news.json
scrapy crawl bitget -o bitget_news.json
```

### Custom Settings

You can override settings from the command line:

```bash
scrapy crawl bitget -s MAX_PAGE=5 -s DOWNLOAD_DELAY=2
```

## Configuration

Key settings in `settings.py`:

- `MAX_PAGE`: Maximum number of pages to crawl (default: 2)
- `DOWNLOAD_DELAY`: Delay between requests in seconds (default: 3)
- `CONCURRENT_REQUESTS`: Number of concurrent requests (default: 8)
- `USER_AGENT`: List of user agents for rotation
- `PROXY_LIST`: Fill the list with your proxy list and remember also to open uncomment the DOWNLOADER_MIDDLEWARES part to use the proxy middleware
- `PLAYWRIGHT_LAUNCH_OPTIONS`: Browser configuration for Playwright spiders

## Example website

Example link for each crypto exchange:

1. Bitget: https://www.bitget.com/support/sections/12508313443483
2. Bitfinex: https://www.bitfinex.com/posts/
3. XT: https://xtsupport.zendesk.com/hc/en-us/categories/10304894611993-Important-Announcements
4. Bybit: https://announcements.bybit.com/en/?category=&page=1

## Data Structure

Each news item contains the following fields:

```json
{
    "news_id": "Unique identifier from the exchange",
    "title": "News headline",
    "desc": "News description/content",
    "url": "Full URL to the news article",
    "category_str": "News category (detailed for Bitget)",
    "exchange": "Exchange name ('bitfinex' or 'bitget' or 'xt' or 'bybit)",
    "announced_at_timestamp": "Original publication timestamp (Unix)",
    "timestamp": "Crawl timestamp (Unix)"
}
```

## Technical Requirements

- Python 3.7+
- Scrapy 2.11.0+
- Playwright (for Bitget spider)
- Chromium browser (automatically installed with Playwright)

## Legal Notice

This crawler is designed for educational and research purposes. Please ensure you comply with:

- Each exchange's Terms of Service
- Rate limiting and robots.txt policies
- Applicable data protection laws
- Fair use guidelines

Always use the crawler responsibly and consider the impact on the target servers.

## Support

For issues, questions, or contributions, please create an issue in the repository.
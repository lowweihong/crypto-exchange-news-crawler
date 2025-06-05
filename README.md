# Cryptocurrency Exchange News Crawler | Bybit Binance Bitget Announcement Scraper

A comprehensive **Scrapy-based web crawler** for **cryptocurrency exchange announcements**. This **crypto news scraper** automatically collects **trading announcements**, **listing news**, and **platform updates** from major **crypto exchanges** including **Bybit**, **Binance**, **Bitget**, **XT**, and **Bitfinex**.

🔍 **Keywords**: crypto exchange crawler, bybit announcement scraper, binance news crawler, cryptocurrency announcement bot, trading news scraper, crypto listing alerts

## 🚀 Features

- **Multi-Exchange Support**: Crawls announcements from major cryptocurrency exchanges
- **Real-time Data**: Extracts latest announcements with timestamps
- **Structured Output**: Clean JSON format for easy integration
- **Scalable Architecture**: Easy to extend for additional exchanges
- **Rate Limiting**: Respectful crawling with configurable delays
- **Proxy Support**: Built-in proxy rotation capabilities

## 📊 Supported Cryptocurrency Exchanges

| Exchange | Status | Announcement Types |
|----------|--------|--------------------|
| **Bybit** ✅ | Active | Trading announcements, new listings, platform updates |
| **Binance** ✅ | Active | New coin listings, trading pairs, system updates |
| **Bitget** ✅ | Active | Futures listings, spot trading, platform news |
| **XT Exchange** ✅ | Active | Token listings, trading announcements |
| **Bitfinex** ✅ | Active | Trading updates, new assets, platform changes |

## Project Description

This project crawls announcement news from cryptocurrency exchanges to help users stay updated with the latest developments, updates, and announcements from major crypto trading platforms. The crawler extracts key information including:

- News title and description
- Publication timestamp
- News URL
- Exchange source
- Unique news ID
- News categories (where available)

## Currently Supported Exchanges

- **Binance**
- **Bybit**
- **Bitget**
- **XT**
- **Bitfinex** 

## 🎯 Use Cases

- **Trading Bots**: Feed announcement data to automated trading systems
- **Market Research**: Analyze exchange listing patterns and trends  
- **News Aggregation**: Build crypto news platforms and alert systems
- **Academic Research**: Study cryptocurrency market announcements
- **Investment Tools**: Track new token listings across exchanges

## 🔧 Quick Start

### Installation

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

### Running Specific Exchange Crawlers

**Bybit Announcements:**
```bash
scrapy crawl bybit -o bybit_announcements.json
```

**Binance News:**
```bash
scrapy crawl binance -o binance_news.json  
```

**Bitget Updates:**
```bash
scrapy crawl bitget -o bitget_updates.json
```

## 📋 Data Schema

Each announcement contains structured data perfect for analysis:

```json
{
    "news_id": "Unique identifier from the exchange",
    "title": "News headline",
    "desc": "News description/content",
    "url": "Full URL to the news article",
    "category_str": "News category (detailed for Bitget)",
    "exchange": "Exchange name ('bitfinex' or 'bitget' or 'xt' or 'bybit', or 'binance')",
    "announced_at_timestamp": "Original publication timestamp (Unix)",
    "timestamp": "Crawl timestamp (Unix)"
}
```

## ⚙️ Configuration

Key settings in `settings.py`:

- `MAX_PAGE`: Maximum number of pages to crawl (default: 2)
- `DOWNLOAD_DELAY`: Delay between requests in seconds (default: 3)
- `CONCURRENT_REQUESTS`: Number of concurrent requests (default: 8)
- `USER_AGENT`: List of user agents for rotation
- `PROXY_LIST`: Fill the list with your proxy list and remember also to open uncomment the DOWNLOADER_MIDDLEWARES part to use the proxy middleware
- `PLAYWRIGHT_LAUNCH_OPTIONS`: Browser configuration for Playwright spiders

### Custom Settings

You can override settings from the command line:

```bash
scrapy crawl bitget -s MAX_PAGE=5 -s DOWNLOAD_DELAY=2
```

## 🔧 Technical Requirements

- Python 3.7+
- Scrapy 2.11.0+
- Playwright (for Bitget spider)
- Chromium browser (automatically installed with Playwright)

## 🌐 Exchange URLs

Direct links to announcement pages:

| Exchange | Announcement URL |
|----------|------------------|
| **Bybit** | https://announcements.bybit.com/en/?category=&page=1 |
| **Binance** | https://www.binance.com/en/support/announcement |
| **Bitget** | https://www.bitget.com/support/sections/12508313443483 |
| **XT** | https://xtsupport.zendesk.com/hc/en-us/categories/10304894611993-Important-Announcements |
| **Bitfinex** | https://www.bitfinex.com/posts/ |

## 🏷️ Tags

`cryptocurrency` `crypto-exchange` `web-scraping` `scrapy` `bybit` `binance` `bitget` `announcements` `trading-bot` `crypto-news` `python` `exchange-api` `market-data` `crypto-crawler` `news-scraper`

## ⚖️ Legal & Ethical Usage

This crawler is designed for educational and research purposes. Please ensure you comply with:

- Each exchange's Terms of Service
- Rate limiting and robots.txt policies
- Applicable data protection laws
- Fair use guidelines

Always use the crawler responsibly and consider the impact on the target servers.

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Add support for more exchanges (OKX, Huobi, KuCoin, etc.)
- Implement real-time WebSocket feeds
- Add telegram/discord notification integrations
- Improve data parsing and categorization

## Support

For issues, questions, or contributions, please create an issue in the repository.
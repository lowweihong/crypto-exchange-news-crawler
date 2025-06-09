# Crypto Exchange News Crawler 🚀

A powerful and easy-to-use Python package for scraping cryptocurrency exchange announcements from major exchanges.

## 🎯 Features

- **Multi-Exchange Support**: Scrape from 9 major crypto exchanges
- **Multiple Output Formats**: JSON, CSV, and XML support
- **Structured Data**: Clean, standardized output format
- **Rate Limiting**: Built-in delays to respect exchange servers
- **Extensible**: Easy to add new exchanges

## 📦 Installation Options

### Option 1: Direct Usage

```bash
git clone https://github.com/lowweihong/crypto-exchange-news-crawler.git
cd crypto-exchange-news-crawler
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
playwright install

scrapy crawl bybit -o output.json
```

### Option 2: Install from PyPI

```bash
pip install crypto-exchange-news-crawler
playwright install

## directly use proxy and uncomment DOWNLOADER_MIDDLEWARES
crypto-news crawl binance -o binance.json

crypto-news crawl bybit -s DOWNLOADER_MIDDLEWARES='{"crypto_exchange_news.middlewares.MyProxyMiddleware": 610}' -s PROXY_LIST="http://proxy1:port,http://proxy2:port"
```

### Supported Exchanges

| Exchange | Status |
|----------|--------|
| Bybit    | ✅ |
| Binance  | ✅ |
| OKX      | ✅ |
| Bitget   | ✅ |
| BingX    | ✅ |
| Kraken   | ✅ |
| Bitfinex | ✅ |
| XT       | ✅ |
|Crypto.com| ✅ |

```
Available options : ["bybit", "binance", "okx", "bitget", "bitfinex", "xt", "bingx", 'kraken', 'cryptocom']
```
#

## 📊 Output Format

Each scraped announcement includes:

```json
{
    "news_id": "unique_identifier",
    "title": "Announcement title",
    "desc": "Announcement description",
    "url": "Full URL to announcement",
    "category_str": "Category (e.g., latest_activities, new_crypto)",
    "exchange": "Exchange name",
    "announced_at_timestamp": 1749235200,
    "timestamp": 1749232733
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
| **Binance** | https://www.binance.com/en/support/announcement |
| **OKX** | https://www.okx.com/help/category/announcements |
| **Bybit** | https://announcements.bybit.com/en/?category=&page=1 |
| **Bitget** | https://www.bitget.com/support/sections/12508313443483 |
| **BingX** | https://bingx.com/en/support/notice-center/ |
| **Kraken** | https://blog.kraken.com/category/product |
| **XT** | https://xtsupport.zendesk.com/hc/en-us/categories/10304894611993-Important-Announcements |
| **Bitfinex** | https://www.bitfinex.com/posts/ |
| **Crypto.com** | https://crypto.com/exchange/announcements |



## ⚖️ Legal & Ethical Usage

This crawler is designed for educational and research purposes. Please ensure you comply with:

- Applicable data protection laws
- Fair use guidelines

Always use the crawler responsibly and consider the impact on the target servers.

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Add support for more exchanges (Huobi, KuCoin, Gateio, etc.)
- Implement real-time WebSocket feeds
- Add telegram/discord notification integrations
- Improve data parsing and categorization

## Support

For issues, questions, or contributions, please create an issue in the repository.
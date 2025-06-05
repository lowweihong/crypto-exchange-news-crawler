from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="crypto-exchange-news-crawler",
    version="0.0.1",
    author="lowweihong",
    author_email="your.email@example.com",
    description="Cryptocurrency exchange announcement news crawler for Bybit, Binance, Bitget, XT, and Bitfinex",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lowweihong/crypto-exchange-news-crawler",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Office/Business :: Financial",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    keywords=[
        "cryptocurrency", "crypto", "exchange", "news", "crawler", "scraper",
        "bybit", "binance", "bitget", "bitfinex", "xt", "announcements",
        "trading", "bot", "api", "scrapy", "web-scraping", "market-data",
        "fintech", "blockchain", "defi", "trading-bot", "crypto-news"
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "crypto-crawler=crypto_exchange_news.cli:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/lowweihong/crypto-exchange-news-crawler/issues",
        "Source": "https://github.com/lowweihong/crypto-exchange-news-crawler",
        "Documentation": "https://github.com/lowweihong/crypto-exchange-news-crawler#readme",
    },
    include_package_data=True,
    zip_safe=False,
) 
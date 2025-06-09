from setuptools import setup, find_packages
import os

# Read README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements file
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]
    

setup(
    name="crypto_exchange_news_crawler",
    version="0.1.5",
    author="lowweihong",
    author_email="lowweihong14@gmail.com",
    description="Cryptocurrency exchange announcement news crawler for major crypto exchanges",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/lowweihong/crypto_exchange_news_crawler",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        "Topic :: Office/Business :: Financial",
    ],
    keywords=[
        "cryptocurrency", "crypto", "exchange", "news", "crawler", "scraper",
        "bybit", "binance", "bitget", "bitfinex", "xt", "okx", "bingx", "kraken", 
        "crypto.com","announcement","trading", "bot", "api", "scrapy", 
        "web-scraping","fintech", "blockchain", "defi", "trading-bot", "crypto-news"
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    project_urls={
        "Bug Reports": "https://github.com/lowweihong/crypto-exchange-news-crawler/issues",
        "Source": "https://github.com/lowweihong/crypto-exchange-news-crawler",
        "Documentation": "https://github.com/lowweihong/crypto-exchange-news-crawler#readme",
    },
    include_package_data=True,
    zip_safe=False,
    package_data={
        "crypto_exchange_news": ["scrapy.cfg"],
        "": ["scrapy.cfg", "requirements.txt"],
    },
    # Entry point for the CLI command
    entry_points={
        'console_scripts': [
            'crypto-news=crypto_exchange_news.cli:main',
        ],
    },
) 
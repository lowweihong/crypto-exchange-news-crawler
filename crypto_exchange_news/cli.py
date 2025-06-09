#!/usr/bin/env python3
"""
Command Line Interface for Crypto Exchange News Crawler
"""

import sys
import os
import argparse
import subprocess
from pathlib import Path
import json

available_spiders = ["bybit", "binance", "okx", "bitget", "bitfinex", "xt", "bingx", 'kraken', 'cryptocom']


def get_spider_classes():
    """Get all available spider classes"""
    spider_classes = {}

    try:
        # Import spider modules
        from crypto_exchange_news.spiders import (
            bybit,
            binance,
            okx,
            bitget,
            bitfinex,
            xt,
            bingx,
            kraken,
            cryptocom
        )

        spider_classes["bybit"] = bybit.BybitSpider
        spider_classes["binance"] = binance.BinanceSpider
        spider_classes["okx"] = okx.OkxSpider
        spider_classes["bitget"] = bitget.BitgetSpider
        spider_classes["bitfinex"] = bitfinex.BitfinexSpider
        spider_classes["xt"] = xt.XtSpider
        spider_classes["bingx"] = bingx.BingxSpider
        spider_classes["kraken"] = kraken.KrakenSpider
        spider_classes["cryptocom"] = cryptocom.CryptocomSpider
        
    except ImportError as e:
        print(f"❌ Error importing spiders: {e}")
        # For debugging, let's also print the current working directory
        print(f"Current working directory: {os.getcwd()}")
        print(
            "Make sure the package is properly installed with: pip install crypto_exchange_news_crawler"
        )

    return spider_classes


def parse_setting_value(value):
    """Parse setting value, handling JSON strings and other types"""
    # Try to parse as JSON first (for dicts, lists, etc.)
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        pass

    # Try to parse as boolean
    if value.lower() in ("true", "false"):
        return value.lower() == "true"

    # Try to parse as number
    try:
        if "." in value:
            return float(value)
        else:
            return int(value)
    except ValueError:
        pass

    # Return as string
    return value


def find_project_root():
    """Find the Scrapy project root directory by looking for scrapy.cfg"""
    current_dir = Path.cwd()

    # First check current directory
    if (current_dir / "scrapy.cfg").exists():
        return current_dir

    # Check parent directories
    for parent in current_dir.parents:
        if (parent / "scrapy.cfg").exists():
            return parent

    # If not found, try to find it relative to this script
    script_dir = Path(__file__).parent.parent
    if (script_dir / "scrapy.cfg").exists():
        return script_dir

    # If still not found, try to find the installed package location
    try:
        import crypto_exchange_news

        package_dir = Path(crypto_exchange_news.__file__).parent.parent
        if (package_dir / "scrapy.cfg").exists():
            return package_dir
    except (ImportError, AttributeError):
        pass

    # As a last resort, create a temporary scrapy.cfg in current directory
    # This allows the command to work from any directory
    temp_scrapy_cfg = current_dir / "scrapy.cfg"
    if not temp_scrapy_cfg.exists():
        print("⚠️  No scrapy.cfg found. Creating temporary configuration...")
        with open(temp_scrapy_cfg, "w") as f:
            f.write("""[settings]
                        default = crypto_exchange_news.settings

                        [deploy]
                        project = crypto_exchange_news
            """)
        print(f"📝 Created temporary scrapy.cfg in {current_dir}")

    return current_dir


def run_spider(spider_name, output_file=None, custom_settings=None, spider_args=None):
    """Run a spider using subprocess to avoid reactor issues"""
    project_root = find_project_root()

    # Set default output file if not provided
    if not output_file:
        output_file = f"{spider_name}_announcements.json"

    # Build scrapy command
    cmd = ["scrapy", "crawl", spider_name, "-o", output_file]

    # Add custom settings
    if custom_settings:
        for key, value in custom_settings.items():
            cmd.extend(["-s", f"{key}={value}"])

    # Add spider arguments
    if spider_args:
        for key, value in spider_args.items():
            cmd.extend(["-a", f"{key}={value}"])

    print(f"🚀 Running: {spider_name} spider")
    print(f"📁 Working directory: {project_root}")
    print(f"📄 Output file: {output_file}")

    # Run the spider with explicit working directory
    result = subprocess.run(cmd, capture_output=True, text=True, cwd=project_root)

    if result.returncode == 0:
        print(f"✅ Spider '{spider_name}' completed successfully")
        print(f"📄 Output saved to: {os.path.join(project_root, output_file)}")
        return True
    else:
        print(f"❌ Error running spider '{spider_name}':")
        if result.stderr:
            print(f"Error details: {result.stderr}")
        if result.stdout:
            print(f"Output: {result.stdout}")
        return False


def list_spiders():
    """List all available spiders"""
    try:

        print("📋 Available exchanges:")
        for spider_name in sorted(available_spiders):
            print(f"  • {spider_name}")

    except Exception as e:
        print(f"❌ Error: {str(e)}")


def validate_spider_name(spider_name):
    """Validate if the spider name is supported"""
    return spider_name in available_spiders


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Crypto Exchange News Crawler",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
            Examples:
            crypto-news crawl bybit                                   # Scrape Bybit announcements
            crypto-news crawl binance -o my_file.json                 # Scrape Binance to custom file
            crypto-news crawl okx -f csv                              # Scrape OKX and save as CSV
            crypto-news crawl xt -s CONCURRENT_REQUESTS=16         # Set concurrent requests
            crypto-news crawl kraken -s DOWNLOAD_DELAY=1               # Set download delay
            crypto-news crawl bingx -s 'DOWNLOADER_MIDDLEWARES={"crypto_exchange_news.middlewares.MyProxyMiddleware": 610}'
            crypto-news list                                          # List all available exchanges
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Crawl command
    crawl_parser = subparsers.add_parser("crawl", help="Crawl a specific exchange")
    crawl_parser.add_argument(
        "exchange", help="Exchange name (e.g., bybit, binance, okx)"
    )
    crawl_parser.add_argument("-o", "--output", help="Output file name")
    crawl_parser.add_argument(
        "-f",
        "--format",
        choices=["json", "csv", "xml"],
        default="json",
        help="Output format (default: json)",
    )
    crawl_parser.add_argument(
        "-s",
        "--set",
        action="append",
        dest="settings",
        metavar="NAME=VALUE",
        help="Set/override setting (may be repeated). Example: -s CONCURRENT_REQUESTS=16",
    )
    crawl_parser.add_argument(
        "-a",
        "--arg",
        action="append",
        dest="spider_args",
        metavar="NAME=VALUE",
        help="Set spider argument (may be repeated). Example: -a category=new_crypto",
    )
    crawl_parser.add_argument(
        "--loglevel",
        "-L",
        choices=["CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG"],
        help="Log level",
    )

    # List command
    list_parser = subparsers.add_parser("list", help="List all available exchanges")

    args = parser.parse_args()

    if args.command == "crawl":
        # Validate spider name first
        if not validate_spider_name(args.exchange):
            print(f"❌ Unknown exchange: {args.exchange}")
            print("📋 Available exchanges:")
            for spider_name in sorted(available_spiders):
                print(f"  • {spider_name}")
            sys.exit(1)

        # Parse custom settings
        custom_settings = {}
        if args.settings:
            for setting in args.settings:
                if "=" not in setting:
                    print(f"❌ Invalid setting format: {setting}. Use NAME=VALUE")
                    sys.exit(1)
                name, value = setting.split("=", 1)
                custom_settings[name] = value

        # Parse spider arguments
        spider_args = {}
        if args.spider_args:
            for arg in args.spider_args:
                if "=" not in arg:
                    print(f"❌ Invalid spider argument format: {arg}. Use NAME=VALUE")
                    sys.exit(1)
                name, value = arg.split("=", 1)
                spider_args[name] = value

        # Set log level if provided
        if args.loglevel:
            custom_settings["LOG_LEVEL"] = args.loglevel

        success = run_spider(args.exchange, args.output, custom_settings, spider_args)
        sys.exit(0 if success else 1)
    elif args.command == "list":
        list_spiders()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

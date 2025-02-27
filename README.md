# Price Tracker and Alert System

## Overview
This Python script monitors product prices from a list of URLs, compares them to predefined alert prices, and notifies users via email if a price drops below the alert threshold. It also logs the updated prices to a CSV file.

## Features
- Scrapes product prices from specified URLs
- Compares current prices with alert prices
- Saves updated price data to a CSV file
- Sends email notifications for price drops

## Requirements
Ensure you have the following installed before running the script:

- Python 3.x
- Required Python packages:
  ```bash
  pip install pandas requests beautifulsoup4 price-parser python-dotenv selenium
  ```

## Setup
1. Clone the repository or download the script.
2. Create a `.env` file in the root directory and add the following:
   ```env
   SENDER=your_email@gmail.com
   RECEIVER=recipient_email@gmail.com
   PASSWORD=your_email_password
   ```
3. Prepare a CSV file (`product.csv`) with the following columns:
   ```csv
   product_title,url,alert_price
   Example Product,https://example.com/product,100
   ```

## Usage
Run the script using:
```bash
python price_tracker.py
```

## How It Works
1. Reads product data from `product.csv`
2. Scrapes the price for each product URL
3. Compares the current price with the alert price
4. Saves the updated prices to `prices.csv`
5. Sends an email if any product's price falls below the alert threshold

## Error Handling
- The script includes basic error handling for HTTP requests and email sending.
- If an error occurs, it is logged in the console.

## Future Enhancements
- Support for multiple email notifications
- Integration with a database for better data storage
- Support for additional e-commerce websites

## License
This project is open-source and free to use.


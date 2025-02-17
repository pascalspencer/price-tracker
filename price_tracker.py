import smtplib
import pandas as pd
import requests
from bs4 import BeautifulSoup
from price_parser import Price
import os
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

product_url_csv = 'product.csv'
save_to_csv = True
price_csv = 'prices.csv'
send_mail = True



# Read CSV and convert to dictionary(product, url, alert price)
def get_urls(csv_file):
    df = pd.read_csv(csv_file)
    return df

# Scraping the prices
def process_products(df):
    updated_products = []
    for product in df.to_dict("records"):
        html = get_response(product["url"])
        product["price"] = get_price(html)
        product["alert"] = product["price"] < product["alert_price"]
        updated_products.append(product)
    return pd.DataFrame(updated_products)

# Get the HTML from response for each URL
def get_response(url):
    response = requests.get(url)
    return response.text

# Locate the price element using a CSS selector
def get_price(html):
    soup = BeautifulSoup(html, "lxml")
    el = soup.select_one(".price_color")
    price = Price.fromstring(el.text)
    return price.amount_float

# Save the result/output
if save_to_csv:
    df_updated = process_products(get_urls(product_url_csv))
    df_updated.to_csv(price_csv, mode="a", index=False)

# Send email
if send_mail:
    sender = os.getenv('SENDER')
    receiver = os.getenv('RECEIVER')
    subject = "Price Drop Alert"
    password = os.getenv('PASSWORD')

    email = EmailMessage()
    email['From'] = 'Spencer LTD'
    email['To'] = receiver
    email['Subject'] = subject

    # Create the email body content
    body = "Price Drop Alert:\n\n"
    for _, product in df_updated[df_updated['alert']].iterrows():
        body += f"Product: {product['product_title']}\n"
        body += f"Current Price: {product['price']}\n"
        body += f"Alert Price: {product['alert_price']}\n\n"

    email.set_content(body)

    try:
        with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
            smtp.ehlo()
            smtp.starttls()
            smtp.login(sender, password)
            smtp.send_message(email)
            print('Email sent successfully!')
    except Exception as e:
        print(f'Error: {e}')

# Execute main file
def main():
    df = get_urls(product_url_csv)
    df_updated = process_products(df)
    save_to_csv(df_updated)
    send_mail(df_updated)

if __name__ == "__main__":
    main()
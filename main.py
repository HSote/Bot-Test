import logging
import requests
import openai
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# Replace with your actual keys
TELEGRAM_BOT_TOKEN = "7820808174:AAE-q03zAnR5r0-oLfoWdm-bmdHdVzggTq8"
OPENAI_API_KEY = "org-Z36SyFWjxZbWLKWgVc04AiKZ"

openai.api_key = OPENAI_API_KEY

# Set up logging
logging.basicConfig(level=logging.INFO)

def get_trending_products():
    """Scrapes a trending product website (e.g., AliExpress/TikTok Trends)."""
    url = "https://www.amazon.de"  # Replace with real source
    headers = {"User-Agent": "Mozilla/5.0"}
    
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    
    products = []
    for item in soup.select(".product-card"):
        title = item.select_one(".title").text
        image = item.select_one("img")["src"]
        link = item.select_one("a")["href"]
        products.append({"title": title, "image": image, "link": link})
    
    return products[:3]  # Return top 3 trending products

def generate_ad_copy(product_name):
    """Uses GPT to generate ad copy."""
    prompt = f"Write an engaging Facebook ad for {product_name}."
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt}]
    )
    
    return response["choices"][0]["message"]["content"]

def start(update: Update, context: CallbackContext) -> None:
    """Handles the /start command."""
    update.message.reply_text("Welcome! Type /trending to get trending products.")

def trending(update: Update, context: CallbackContext) -> None:
    """Handles the /trending command."""
    products = get_trending_products()
    
    for product in products:
        ad_copy = generate_ad_copy(product["title"])
        message = f"🔥 Trending Product: {product['title']}\n\n{ad_copy}\n\n🔗 Buy Now: {product['link']}"
        update.message.reply_photo(photo=product["image"], caption=message)

def main():
    """Main function to run the bot."""
    updater = Updater(TELEGRAM_BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("trending", trending))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

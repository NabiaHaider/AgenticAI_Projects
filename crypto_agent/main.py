import requests

# 🎉 Top 10 Crypto Coins
def crypto_price():
    url = "https://api.binance.com/api/v3/ticker/price"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        print("\n💰 Top 10 Crypto Coin Prices on Binance:\n")
        for coin in data[:10]:
            print(f"🔹 {coin['symbol']}: {coin['price']} USDT")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching top 10 coin prices: {e}")

# 💸 Specific Coin Price Checker
def show_specific_coin_price(symbol):
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol.upper()}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print(f"\n📈 Current Price of {symbol.upper()}: {data['price']} USDT 💸")
        else:
            print("❌ Invalid coin symbol or not available on Binance.")
    except requests.exceptions.RequestException as e:
        print(f"❌ Error fetching price for {symbol}: {e}")

# 🚀 Main Program
def main():
    print("🚀 Live Crypto Price Agent using Binance API\n")
    crypto_price()

    while True:
        user_input = input("\n🔍 Enter a coin symbol (e.g., BTCUSDT) to get its price or type 'exit' to quit: ").strip()
        if user_input.lower() == 'exit':
            print("👋 Exiting the program. Stay updated with crypto prices! 📊")
            break
        elif user_input:
            show_specific_coin_price(user_input)
        else:
            print("⚠️ Please enter a valid coin symbol.")

if __name__ == "__main__":
    main()

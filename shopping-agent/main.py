# 🔠 re aur requests modules ko import kar rahe hain
import re
import requests

# 🤖 Agent aur Runner class import kar rahe hain OpenAI agents framework se
from agents import Agent, Runner

# 🔧 Model configuration import kar rahe hain jo connection.py file me hogi
from connection import config

# 🔍 Yeh function user ke keyword ke mutabiq API se product search karta hai
def search_products(keyword: str) -> str:
    try:
        # 🛒 API ka URL jahan se product data milega
        url = "https://hackathon-apis.vercel.app/api/products"

        # 🌐 API call bhej rahe hain
        response = requests.get(url)

        # ✅ Agar API response sahi na ho to error raise karega
        response.raise_for_status()

        # 🔁 Response ko JSON me convert kar rahe hain (Python list of dicts ban jati hai)
        products = response.json()

        # 🔤 User ke keyword ko chhote words me tod rahe hain aur lowercase me kar rahe hain
        words = re.findall(r"\b\w+\b", keyword.lower())

        # ❌ Stopwords define kar rahe hain jo search me use nahi honge
        stopwords = {"the", "with", "under", "above", "for", "of", "and", "or", "are", "an", "in", "to", "below", "between", "is", "best"}

        # ✅ Stopwords ke ilawa ke words ko keywords list me le rahe hain
        keywords = [w for w in words if w not in stopwords]

        # 📦 Filtered products store karne ke liye khali list banai
        filtered = []

        # 🔁 Har product me search kar rahe hain
        for p in products:
            # 🏷️ Product ka title le rahe hain (agar na ho to khali string)
            title = p.get("title", "").lower()  # ✅ spelling "titile" se correct kar diya

            # 💰 Product ki price le rahe hain
            price = p.get("price", None)

            # ❌ Agar title ya price missing ho to is product ko skip kar do
            if not title or price is None:
                continue

            # ✅ Agar koi bhi keyword title me match kare to us product ko filtered list me daal do
            if any(kw in title for kw in keywords):
                filtered.append(f"- {p['title']} | Rs {price}")

        # 📋 Agar koi matching product mila ho to sirf pehle 5 return karo
        if filtered:
            return "\n".join(filtered[:5])
        else:
            return "No matching products found."
    
    # ⚠️ Agar koi error aaye to uska message return karo
    except Exception as e:
        return f"Error fetching products: {str(e)}"

# 🔰 Yeh main function hai — program yahan se start hota hai
def main():
    # 👋 User ko welcome message dikhate hain
    print("🛒 Welcome to the Product Shopping Agent!")

    # 🧑‍💻 User se pucha ja raha hai woh kya dhoond raha hai
    user_question = input("📃 What product are you looking for? ")

    # 🤖 GPT model define kiya gaya hai
    model = "gpt-3.5-turbo"

    # 🧠 Shopping Agent banaya gaya hai jo user ki query samjhega
    agent = Agent(
        name="Shopping Agent",  # 👩‍💼 Agent ka naam
        instructions="You are a helpful shopping assistant. Provide product recommendations based on user queries.",  # 📜 Agent ko instruction
        model=model  # 🧠 GPT model use ho raha hai
    )

    # 🔁 Agent ko run karte hain user ke question ke sath
    result = Runner.run_sync(agent, user_question, run_config=config)

    # 📤 Agent ka final response extract karte hain
    result = result.final_output

    # 🔍 Product search karte hain user ke question se
    product_results = search_products(user_question)

    # 📋 Agar products milte hain to print karo
    if product_results:
        print("\n🛍 Matching Products:\n", product_results)

    # 🤖 Agent ka jawab print karo
    print("\n🤖 Agent Response:\n", result)

# 🚀 Agar file directly run ho rahi hai to main() ko call karo
if __name__ == "__main__":
    main()

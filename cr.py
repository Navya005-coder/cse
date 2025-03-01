
import requests

def get_exchange_rate(base_currency, target_currency):
    url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
    response = requests.get(url)
    data = response.json()
    
    if target_currency in data["rates"]:
        return data["rates"][target_currency]
    else:
        return None

def convert_currency(amount, base_currency, target_currency):
    exchange_rate = get_exchange_rate(base_currency, target_currency)
    
    if exchange_rate is None:
        print("Invalid currency code.")
        return None
    
    converted_amount = amount * exchange_rate
    return converted_amount

if __name__ == "__main__":
    base_currency = input("Enter base currency (e.g., USD): ").upper()
    target_currency = input("Enter target currency (e.g., EUR): ").upper()
    amount = float(input("Enter amount to convert: "))
    
    result = convert_currency(amount, base_currency, target_currency)
    
    if result is not None:
        print(f"{amount} {base_currency} is equal to {result:.2f} {target_currency}")

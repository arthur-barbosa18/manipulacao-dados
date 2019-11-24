import requests


def create_timeline():
    data = requests.get("https://storage.googleapis.com/dito-questions/events.json").json()
    bought = [item for item in data["events"] if item["event"] == "comprou"]
    products = [item for item in data["events"] if item["event"] == "comprou-produto"]
    result = []
    for event in bought:
        transaction_id = [i["value"] for i in event["custom_data"] if i["key"] == "transaction_id"][0]
        store_name = [i["value"] for i in event["custom_data"] if i["key"] == "store_name"][0]
        data = {
            "timestamp": event["timestamp"],
            "revenue": event["revenue"],
            "transaction_id": transaction_id,
            "store_name": store_name,
            "products": [],
        }

        for product in products:
            if transaction_id in [item["value"] for item in product["custom_data"] if item["key"] == "transaction_id"]:
                name = [i["value"] for i in product["custom_data"] if i["key"] == "product_name"][0]
                price = [i["value"] for i in product["custom_data"] if i["key"] == "product_price"][0]
                data["products"].append({"name": name, "price": price})

        result.append(data)

    return {"timeline": sorted(result, key=lambda i: i["timestamp"], reverse=True)}


print(create_timeline())

import json


class Config:
    def __init__(self, webhook, save_path, invoices):
        self.webhook = webhook
        self.save_path = save_path
        self.invoices = invoices


class Invoice:
    def __init__(self, seller, buyer, items, issue_place, payment_due_days, payment_method, gtu_codes, bank_name=None,
                 bank_account=None):
        self.seller = seller
        self.buyer = buyer
        self.items = items
        self.issue_place = issue_place
        self.payment_due_days = payment_due_days
        self.payment_method = payment_method
        self.bank_name = bank_name
        self.bank_account = bank_account
        self.gtu_codes = gtu_codes


class SellerBuyer:
    def __init__(self, name, address, nip):
        self.name = name
        self.address = address
        self.nip = nip


class Item:
    def __init__(self, name, quantity, unit, net_price, vat_rate):
        self.name = name
        self.quantity = quantity
        self.unit = unit
        self.net_price = net_price
        self.vat_rate = vat_rate


def load_config(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    webhook = data.get("webhook")
    save_path = data.get("save_path", "./faktury")
    invoices_data = data.get("invoices", [])

    invoices = []
    for inv in invoices_data:
        seller_data = inv.get("seller")
        seller = SellerBuyer(seller_data["name"], seller_data["address"], seller_data["nip"])

        buyer_data = inv.get("buyer")
        buyer = SellerBuyer(buyer_data["name"], buyer_data["address"], buyer_data["nip"])

        items_data = inv.get("items", [])
        items = [Item(item["name"], item["quantity"], item["unit"], item["net_price"], item["vat_rate"]) for item in
                 items_data]

        invoice = Invoice(
            seller, buyer, items,
            inv["issue_place"], inv["payment_due_days"],
            inv["payment_method"], inv.get("gtu_codes", []), inv.get("bank_name", None), inv.get("bank_account", None),
        )

        invoices.append(invoice)

    return Config(webhook, save_path, invoices)

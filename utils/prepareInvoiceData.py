from datetime import datetime, timedelta


def prepare_invoice_data(seller, buyer, items, issue_place, payment_due_days=7,
                         payment_method="Przelew", bank_name="", bank_account="", gtu_codes=None):

    if gtu_codes is None:
        gtu_codes = []
    issue_date = datetime.now().strftime("%Y-%m-%d")
    sale_date = datetime.now().strftime("%Y-%m-%d")

    payment_due_date = (datetime.strptime(issue_date, "%Y-%m-%d") + timedelta(days=payment_due_days)).strftime(
        "%Y-%m-%d")

    invoice_data = {
        "seller": seller,
        "buyer": buyer,
        "issue_place": issue_place,
        "issue_date": issue_date,
        "sale_date": sale_date,
        "payment_due_date": payment_due_date,
        "payment_method": payment_method,
        "bank_name": bank_name,
        "bank_account": bank_account,
        "gtu_codes": gtu_codes or [],
        "items": [],
        "total_net_value": 0.0,
        "total_vat_value": 0.0,
        "total_gross_value": 0.0,
        "amount_due": 0.0
    }

    for index, item in enumerate(items, start=1):
        quantity = item.quantity
        net_price = item.net_price
        vat_rate = item.vat_rate

        net_value = quantity * net_price
        vat_value = net_value * (vat_rate / 100)
        gross_value = net_value + vat_value

        invoice_item = {
            "index": index,
            "name": item.name,
            "quantity": quantity,
            "unit": item.unit,
            "net_price": net_price,
            "net_value": net_value,
            "vat_rate": vat_rate,
            "vat_value": vat_value,
            "gross_value": gross_value
        }

        invoice_data["items"].append(invoice_item)
        invoice_data["total_net_value"] += net_value
        invoice_data["total_vat_value"] += vat_value
        invoice_data["total_gross_value"] += gross_value

    invoice_data["amount_due"] = invoice_data["total_gross_value"]

    return invoice_data

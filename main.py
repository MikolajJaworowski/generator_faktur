import argparse
import os
from datetime import datetime

from utils.loadConfig import load_config
from utils.createInvoiceDirectoryStructure import create_invoice_directory_structure
from utils.generateInvoicePdf import generate_invoice_pdf
from utils.prepareInvoiceData import prepare_invoice_data
from utils.sendWebhookNotification import send_webhook_notification


def main():
    parser = argparse.ArgumentParser(description='Skrypt do generowania faktur.')
    parser.add_argument('-c', '--config', type=str, default='config.json', help='Ścieżka do pliku konfiguracyjnego (domyślnie config.json)')
    args = parser.parse_args()

    config_path = args.config
    config = load_config(config_path)

    invoice_directory = create_invoice_directory_structure(config.save_path)

    for invoice_index, invoice in enumerate(config.invoices, start=1):
        invoice_data = prepare_invoice_data(
            seller=invoice.seller,
            buyer=invoice.buyer,
            items=invoice.items,
            issue_place=invoice.issue_place,
            payment_due_days=invoice.payment_due_days,
            payment_method=invoice.payment_method,
            bank_name=invoice.bank_name,
            bank_account=invoice.bank_account,
            gtu_codes=invoice.gtu_codes
        )

        issue_date = datetime.strptime(invoice_data["issue_date"], "%Y-%m-%d")
        buyer_name_sanitized = invoice_data['buyer'].name.lower().replace(' ', '_')
        invoice_filename = f"{issue_date.strftime('%Y-%m')}-{invoice_index:02d}-{buyer_name_sanitized}.pdf"

        invoice_filepath = os.path.join(invoice_directory, invoice_filename)

        generate_invoice_pdf(invoice_data, invoice_filepath, invoice_index)

        print(f"Faktura została zapisana: {invoice_filepath}")

    if config.webhook:
        send_webhook_notification(config.webhook, invoice_directory)


if __name__ == "__main__":
    main()
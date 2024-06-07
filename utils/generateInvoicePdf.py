from datetime import datetime

from fpdf import FPDF


def init_invoice_pdf():
    pdf = FPDF()
    pdf.add_page()

    pdf.add_font('DejaVu', '', './assets/DejaVuSansCondensed.ttf', uni=True)
    pdf.add_font('DejaVuBold', '', './assets/DejaVuSansCondensed-Bold.ttf', uni=True)

    return pdf


def set_default_font(pdf):
    pdf.set_font('DejaVu', '', 12)


def set_big_font(pdf):
    pdf.set_font('DejaVu', '', 24)


def set_small_font(pdf):
    pdf.set_font('DejaVu', '', 10)


def set_default_styles(pdf):
    set_default_font(pdf)
    pdf.set_margins(top=8, left=20, right=20)
    pdf.set_draw_color(200, 200, 200)


def add_spacer(pdf, height=10):
    pdf.cell(0, height, ln=True, align='L')


def generate_header(pdf, issue_date, invoice_index, invoice_data):
    invoice_number = f"{"{:02d}".format(invoice_index)}/{issue_date.strftime('%m/%Y')}"

    pdf.cell(0, 10, txt=f"Numer faktury", ln=True, align='R')
    set_big_font(pdf)

    pdf.cell(0, 10, txt=invoice_number, ln=True, align='R')
    set_default_font(pdf)

    add_spacer(pdf, height=6)

    pdf.cell(0, 6, txt=f"Miejsce wystawienia: {invoice_data['issue_place']}", ln=True, align='R')
    pdf.cell(0, 6, txt=f"Data wystawienia: {invoice_data['issue_date']}", ln=True, align='R')
    pdf.cell(0, 6, txt=f"Data sprzedaży: {invoice_data['sale_date']}", ln=True, align='R')


def generate_seller_buyer_box(pdf, invoice_data, box_type):
    set_default_styles(pdf)
    pdf.cell(0, 8, txt="Sprzedawca:" if box_type == 'seller' else "Nabywca:", ln=True, align='L')

    if box_type == 'seller':
        pdf.set_fill_color(220, 220, 220)

    pdf.c_margin = 6

    set_small_font(pdf)

    pdf.multi_cell(0, 6,
                   f"\n"
                   f"{invoice_data[box_type].name}\n"
                   f"{invoice_data[box_type].address}\n"
                   f"NIP: {invoice_data[box_type].nip}\n\n",
                   align='L',
                   fill=box_type == 'seller',
                   border=0 if box_type == 'seller' else 1
                   )
    pdf.c_margin = 0


def generate_products_table(pdf, invoice_data):
    set_small_font(pdf)

    pdf.set_margins(top=8, left=10, right=10)
    pdf.cell(0, 0, ln=True, align='L')

    col_widths = [6, 60, 10, 25, 25, 15, 25, 25]
    headers = ["LP", "Nazwa towaru / usługi", "Ilość", "Cena netto", "Wartość netto", "VAT %", "Wartość VAT",
               "Wartość brutto"]

    for i, header in enumerate(headers):
        pdf.set_font('DejaVuBold', '', 8)
        pdf.cell(col_widths[i], 10, txt=header, border=1, align='C')
    pdf.ln(10)

    pdf.c_margin = 1

    pdf.set_font('DejaVu', '', 8)
    for item in invoice_data['items']:
        pdf.cell(col_widths[0], 10, txt=str(item['index']), border=1, align='C')
        pdf.cell(col_widths[1], 10, txt=item['name'], border=1)
        pdf.cell(col_widths[2], 10, txt=f"{str(item['quantity'])} {item['unit']}", border=1, align='C')
        pdf.cell(col_widths[3], 10, txt=f"{item['net_price']:.2f}", border=1, align='R')
        pdf.cell(col_widths[4], 10, txt=f"{item['net_value']:.2f}", border=1, align='R')
        pdf.cell(col_widths[5], 10, txt=str(item['vat_rate']), border=1, align='C')
        pdf.cell(col_widths[6], 10, txt=f"{item['vat_value']:.2f}", border=1, align='R')
        pdf.cell(col_widths[7], 10, txt=f"{item['gross_value']:.2f}", border=1, align='R')
        pdf.ln(10)

    pdf.cell(sum(col_widths[:6]), 10, txt="Razem:", border=1)
    pdf.cell(col_widths[6], 10, txt=f"{invoice_data['total_vat_value']:.2f}", border=1, align='R')
    pdf.cell(col_widths[7], 10, txt=f"{invoice_data['total_gross_value']:.2f}", border=1, align='R')
    pdf.ln(10)

    set_default_styles(pdf)


def generate_summary(pdf, invoice_data):
    set_small_font(pdf)

    pdf.cell(200, 10, txt=f"Do zapłaty: {invoice_data['amount_due']:.2f} PLN", ln=True, align='L')

    pdf.cell(200, 10, txt=f"Termin płatności: {invoice_data['payment_due_date']}", ln=True, align='L')

    pdf.cell(200, 10, txt=f"Sposób płatności: {invoice_data['payment_method']}", ln=True, align='L')
    if invoice_data['payment_method'] == 'Przelew':
        pdf.cell(200, 10, txt=f"Bank: {invoice_data['bank_name']}", ln=True, align='L')
        pdf.cell(200, 10, txt=f"Konto: {invoice_data['bank_account']}", ln=True, align='L')

    if invoice_data['gtu_codes']:
        pdf.cell(200, 10, txt=f"Kody GTU: {', '.join(invoice_data['gtu_codes'])}", ln=True, align='L')


def generate_invoice_pdf(invoice_data, file_path, invoice_index):
    pdf = init_invoice_pdf()
    set_default_styles(pdf)

    issue_date = datetime.strptime(invoice_data['issue_date'], "%Y-%m-%d")

    generate_header(pdf, issue_date, invoice_index, invoice_data)

    generate_seller_buyer_box(pdf, invoice_data, 'seller')

    add_spacer(pdf, height=4)

    generate_seller_buyer_box(pdf, invoice_data, 'buyer')

    add_spacer(pdf)

    generate_products_table(pdf, invoice_data)

    add_spacer(pdf)

    generate_summary(pdf, invoice_data)

    pdf.output(file_path)

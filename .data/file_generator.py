from fpdf import FPDF


def generate_empty_pdf():
    with open('empty.pdf', 'w'):
        pass


def generate_pdf_files():
    pdf = FPDF()
    pdf.add_page()
    pdf.cell(txt="Hello World!")
    pdf.output("hello_world.pdf")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Hello", ln=1, align="L")
    pdf.cell(200, 10, txt="World", ln=1, align="R")
    pdf.cell(200, 10, txt="", ln=1, align="с")
    pdf.cell(200, 10, txt="!", ln=1, align="C")
    pdf.output("multi_lines.pdf")

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Привет", ln=1, align="C")
    pdf.output("russian.pdf")




generate_pdf_files()
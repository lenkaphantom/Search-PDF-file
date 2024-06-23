import os
from fpdf import FPDF

def get_filename(query):
    if '"' in query:
        return query.strip('"') + '.pdf'
    return query + '.pdf'


def save_to_pdf(results, query, text_by_page, filename='search_results.pdf'):
    if not os.path.exists('rezultati'):
        os.makedirs('rezultati')

    full_filename = os.path.join('rezultati', get_filename(query))

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()
    dejavu_font_path = os.path.join('dejavu-sans', 'DejaVuSans.ttf')
    pdf.add_font('DejaVu', '', dejavu_font_path, uni=True)
    pdf.set_font("DejaVu", size=10)

    i = 0

    for result in results:
        if i == 10:
            break
        page_number = result[1]
        page_text = text_by_page[page_number]

        pdf.set_text_color(0, 0, 0)
        pdf.cell(200, 10, txt=f"Rezultat za stranicu {page_number + 1}", ln=True)
        pdf.ln(5)

        pdf.multi_cell(0, 10, txt=page_text)
        pdf.ln(5)

        i += 1

    pdf.output(full_filename)
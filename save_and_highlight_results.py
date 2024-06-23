import os
import re
import fitz

def get_filename(query):
    if '"' in query:
        return query.strip('"') + '.pdf'
    return query + '.pdf'

def save_to_pdf(results, query, text_by_page, filename='search_results.pdf'):
    if not os.path.exists('rezultati'):
        os.makedirs('rezultati')

    full_filename = os.path.join('rezultati', get_filename(query))

    pdf = fitz.open()

    query_words = re.findall(r'\w+', query)

    for result in results:
        page_number = result[1]
        page_text = text_by_page[page_number]

        highlight_pdf_page(pdf, page_text, query_words)

    pdf.save(full_filename)
    pdf.close()

def highlight_pdf_page(pdf, page_text, query_words):
    page = pdf.new_page()

    page.insert_text((50, 100), page_text)

    for word in query_words:
        word_instances = re.finditer(rf'\b{re.escape(word)}\b', page_text, flags=re.IGNORECASE)
        for instance in word_instances:
            start, end = instance.span()
            word_text = page_text[start:end]
            word_instances = page.search_for(word_text)

            for inst in word_instances:
                highlight = page.add_highlight_annot(inst)
                highlight.update()

    return page
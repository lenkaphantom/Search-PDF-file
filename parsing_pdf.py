import PyPDF2
import json

def parse_pdf(file_path):
    reader = PyPDF2.PdfReader(file_path)
    text_by_page = [page.extract_text() for page in reader.pages]
    return text_by_page

def save_parsed_text(text_by_page, output_file):
    with open(output_file, 'w') as f:
        json.dump(text_by_page, f)

def load_parsed_text(input_file):
    with open(input_file, 'r') as f:
        text_by_page = json.load(f)
    return text_by_page

if __name__ == '__main__':
    file_path = 'Data Structures and Algorithms in Python.pdf'
    parsed_text_file = 'parsed_text.json'

    text_by_page = parse_pdf(file_path)
    save_parsed_text(text_by_page, parsed_text_file)
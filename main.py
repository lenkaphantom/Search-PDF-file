from PyPDF2 import PdfReader

if __name__ == '__main__':
    pdf_path = 'Data Structures and Algorithms in Python.pdf'
    pdf = PdfReader(pdf_path)
    print(len(pdf.pages))
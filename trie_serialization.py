from trie import Trie
from parsing_pdf import load_parsed_text
import pickle

def create_trie(text_by_page):
    trie = Trie()
    for page_number, text in enumerate(text_by_page):
        if text:
            words = text.lower().split()
            for word in words:
                trie.insert(word, page_number)
    return trie

def save_trie(trie, output_file):
    with open(output_file, 'wb') as f:
        pickle.dump(trie, f)

def load_trie(input_file):
    with open(input_file, 'rb') as f:
        trie = pickle.load(f)
    return trie

if __name__ == '__main__':
    file_path = 'Data Structures and Algorithms in Python.pdf'
    parsed_text_file = 'parsed_text.json'
    text_by_page = load_parsed_text(parsed_text_file)

    trie = create_trie(text_by_page)
    save_trie(trie, 'trie.pkl')
    trie = load_trie('trie.pkl')
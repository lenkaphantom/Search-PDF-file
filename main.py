from parsing_pdf import load_parsed_text
from trie_serialization import load_trie
from Trie import Trie

def search_and_display(query, trie, text_by_page):
    results = trie.search(query)
    if results:
        for rank, page_number in enumerate(results):
            context = text_by_page[page_number][:200]
            highlighted_context = context.replace(query, f"\033[1;31m{query}\033[0m")
            print(f"{rank + 1}. Page {page_number + 1}: {highlighted_context}")
    else:
        print("No results found")

def main():
    parsed_text_file = 'parsed_text.json'
    text_by_page = load_parsed_text(parsed_text_file)
    
    try:
        trie = load_trie('trie.pkl')
    except FileNotFoundError:
        print("Trie file not found. Please run trie_serialization.py to create the trie")
        return

    while True:
        query = input("Enter search query: ").lower()
        if query == 'exit':
            break
        search_and_display(query, trie, text_by_page)

if __name__ == "__main__":
    main()
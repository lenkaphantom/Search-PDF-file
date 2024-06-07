from parsing_pdf import load_parsed_text
from trie_serialization import load_trie

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
        print("Trie fajl nije pronadjen. Pokrenite trie_serialization.py da biste ga kreirali.")
        return

    while True:
        print("Dobro dosli u pretragu PDF-a. Za izlaz u bilo kom trenutku unesite 'X'.")
        query = input("Unesite rec za pretragu: ").lower()
        if query == 'x' or query == 'X':
            break
        search_and_display(query, trie, text_by_page)

if __name__ == "__main__":
    main()
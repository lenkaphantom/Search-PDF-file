from parsing_pdf import load_parsed_text
from trie_serialization import load_trie


def search(query, trie, text_by_page):
    results = trie.search(query)
    result_dict = {}
    if results:
        for page_number in results:
            page_text = text_by_page[page_number]
            start_index = page_text.find(query)
            if start_index != -1:
                start_context = max(0, start_index - 50)
                end_context = min(len(page_text), start_index + len(query) + 50)
                context = page_text[start_context:end_context]
                highlighted_context = context.replace(query, f"\033[1;94m{query}\033[0m")
                result_dict[page_number] = highlighted_context
    return result_dict


def search_and_display(query, trie, text_by_page):
    results = search(query, trie, text_by_page)
    i = 0
    if results:
        for key in results:
            if i == 10:
                choice = input("Prikazano je prvih 10 rezultata. Da li zelite da vidite jos? (Y/N): ")
                if choice.lower() != 'y':
                    break
                i = 0
            page_number = key + 1
            context = results[key]
            print(f"-------------Rezultat {key + 1}-------------")
            print(f"Strana: {page_number}")
            print(context)
            print("-------------------------------------\n")
            i += 1
    else:
        print("Nema rezultata za unetu rec.")


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
        if len(query) < 3:
            print("\nRec mora imati najmanje 3 karaktera.\n")
            continue
        search_and_display(query, trie, text_by_page)


if __name__ == "__main__":
    main()
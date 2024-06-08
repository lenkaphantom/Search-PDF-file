from parsing_pdf import load_parsed_text
from trie_serialization import load_trie
from graph_serialization import load_graph

import re

def search(query, trie, text_by_page):
    results = trie.search(query)
    result_dict = {}
    if results:
        for page_number in results:
            page_text = text_by_page[page_number]
            start_index = page_text.lower().find(query.lower())
            if start_index != -1:
                start_context = page_text.rfind('.', 0, start_index) + 1
                if start_context == 0:
                    start_context = page_text.rfind('!', 0, start_index) + 1
                if start_context == 0:
                    start_context = page_text.rfind('?', 0, start_index) + 1
                if start_context == 0:
                    start_context = 0

                end_context = page_text.find('.', start_index)
                if end_context == -1:
                    end_context = page_text.find('!', start_index)
                if end_context == -1:
                    end_context = page_text.find('?', start_index)
                if end_context == -1:
                    end_context = len(page_text)

                context = page_text[start_context:end_context].strip()
                highlighted_context = re.sub(re.escape(query), f"\033[1;94m{query}\033[0m", context, flags=re.IGNORECASE)
                result_dict[page_number] = highlighted_context
    return result_dict


def rank_results(query, results, graph, text_by_page):
    ranked_results = []
    for page_number in results.keys():
        page_text = text_by_page[page_number]
        word_count = page_text.lower().split().count(query)
        
        vertex = None
        for v in graph.vertices():
            if v.element() == page_number:
                vertex = v
                break
        
        citation_count = 0
        if vertex:
            citation_count = len(list(graph.incident_edges(vertex)))

        score = word_count + citation_count
        ranked_results.append((score, page_number, results[page_number]))

    ranked_results.sort(reverse=True, key=lambda x: x[0])
    return ranked_results

def search_and_display(query, trie, text_by_page, graph):
    results = search(query, trie, text_by_page)
    ranked_results = rank_results(query, results, graph, text_by_page)
    i = 0
    k = 0
    if ranked_results:
        for rank, page_number, context in ranked_results:
            if i == 10:
                choice = input("Prikazano je prvih 10 rezultata. Da li zelite da vidite jos? (Y/N): ")
                if choice.lower() != 'y':
                    break
                i = 0
            print(f"-------------Rezultat {k + 1}-------------")
            print(f"Strana: {page_number + 1}")
            print(f"Skor: {rank}")
            print(context)
            print("-------------------------------------\n")
            i += 1
            k += 1
    else:
        print("Nema rezultata za unetu rec.")

def main():
    parsed_text_file = 'parsed_text.json'
    text_by_page = load_parsed_text(parsed_text_file)

    try:
        graph = load_graph('graph.pkl')
    except FileNotFoundError:
        print("Graph fajl nije pronadjen. Pokrenite graph_serialization.py da biste ga kreirali.")
        return
    
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
        search_and_display(query, trie, text_by_page, graph)

if __name__ == "__main__":
    main()
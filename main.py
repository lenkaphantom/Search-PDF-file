from parsing_pdf import load_parsed_text
from trie_serialization import load_trie
from graph_serialization import load_graph
import re

def highlight_context(context, words):
    for word in words:
        word_pattern = re.compile(rf'(?i)\b{re.escape(word)}\b')
        context = word_pattern.sub(lambda match: f"\033[1;94m{match.group(0)}\033[0m", context)
    return context

def search(query, trie, text_by_page):
    words = query.split(", ")
    results = {}

    for word in words:
        word_results = trie.search(word)
        if word_results is None:
            continue
        for page_number in word_results:
            if page_number not in results:
                results[page_number] = set()
            page_text = text_by_page[page_number]
            start_index = page_text.lower().find(word.lower())
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
                results[page_number].add(context)
    return results


def search_phrase(query, trie, text_by_page):
    pass


def search_operators(query, trie, text_by_page):
    pass


def rank_results(query, results, graph, text_by_page):
    words = query.split(", ")
    ranked_results = []

    for page_number, contexts in results.items():
        page_text = text_by_page[page_number]
        word_count = sum(page_text.lower().split().count(word.lower()) for word in words)

        vertex = None
        for v in graph.vertices():
            if v.element() == page_number:
                vertex = v
                break
        
        citation_count = 0
        if vertex:
            citation_count = len(list(graph.incident_edges(vertex)))

        all_words_count = 0
        if len(words) > 1:
            all_words_count = sum(1 for word in words if word.lower() in page_text.lower())

        score = word_count + citation_count + all_words_count * 2
        combined_context = ' ... '.join(contexts)
        highlighted_context = highlight_context(combined_context, words)
        ranked_results.append((score, page_number, highlighted_context))

    ranked_results.sort(reverse=True, key=lambda x: x[0])
    return ranked_results


def save_results(results, file_name):
    pass


def search_and_display(query, trie, text_by_page, graph):
    results = search(query, trie, text_by_page)
    ranked_results = rank_results(query, results, graph, text_by_page)
    displayed_pages = set()
    i = 0
    k = 0
    if ranked_results:
        for rank, page_number, context in ranked_results:
            if page_number in displayed_pages:
                continue
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
            displayed_pages.add(page_number)
            i += 1
            k += 1
    else:
        print("Nema rezultata za unetu rec.")

def main():
    try:
        text_by_page = load_parsed_text('parsed_text.json')
    except FileNotFoundError:
        print("Parsed text fajl nije pronadjen. Pokrenite parsing_pdf.py da biste ga kreirali.")
        return

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
        query = input("Unesite rec za pretragu (za više reči koristite zarez, npr. 'rec, rec'): ").lower()
        if query == 'x' or query == 'X':
            break
        if len(query) < 3:
            print("\nRec mora imati najmanje 3 karaktera.\n")
            continue

        search_and_display(query, trie, text_by_page, graph)


if __name__ == "__main__":
    main()

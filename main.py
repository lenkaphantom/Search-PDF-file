import re
from parsing_pdf import load_parsed_text
from trie_serialization import load_trie
from graph_serialization import load_graph
from search import *

def levenshtein_distance(word1, word2):
    if len(word1) < len(word2):
        return levenshtein_distance(word2, word1)

    if len(word2) == 0:
        return len(word1)

    previous_row = range(len(word2) + 1)
    for i, c1 in enumerate(word1):
        current_row = [i + 1]
        for j, c2 in enumerate(word2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

def did_you_mean(word, trie):
    all_words = []
    collect_all_possible_words(trie.root, all_words)
    closest_word = None
    min_distance = float('inf')

    for candidate in all_words:
        distance = levenshtein_distance(word, candidate)
        if distance < min_distance:
            min_distance = distance
            closest_word = candidate

    return closest_word

def collect_all_possible_words(node, words):
    if node.is_end_of_word:
        words.append(node.word)
    for child in node.children.values():
        collect_all_possible_words(child, words)

def validate_query(query):
    if not query:
        print("Unesite upit za pretragu.")
        return False
    
    if len(query) < 3:
        print("Upit mora sadrzati bar 3 karaktera.")
        return False
    
    if query.startswith('"') and not query.endswith('"'):
        print("Niste zatvorili navodnike.")
        return False
    
    and_ocurrences = [i.start() for i in re.finditer("and", query)]
    or_ocurrences = [i.start() for i in re.finditer("or", query)]
    not_ocurrences = [i.start() for i in re.finditer("not", query)]

    if 0 in and_ocurrences or 0 in or_ocurrences or 0 in not_ocurrences:
        print("Operatori AND, OR i NOT ne mogu biti prvi karakteri upita.")
        return False
    
    if len(query) - 1 in and_ocurrences or len(query) - 1 in or_ocurrences or len(query) - 1 in not_ocurrences:
        print("Operatori AND, OR i NOT ne mogu biti poslednji karakteri upita.")
        return False
    
    return True

def highlight_context(context, words):
    for word in words:
        word_pattern = re.compile(rf'(?i){re.escape(word)}')
        context = word_pattern.sub(lambda match: f"\033[1;94m{match.group(0)}\033[0m", context)
    return context

def rank_results(query, results, graph, text_by_page):
    if '"' in query:
        words = query.strip('"').split()
    elif any(op in query for op in ['AND', 'OR', 'NOT']):
        words = re.split(r'\s+(AND|OR|NOT)\s+', query)[::2]
    else:
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
        if len(combined_context) > 500:
            combined_context = combined_context[:500] + '...'
        highlighted_context = highlight_context(combined_context, words)
        ranked_results.append((score, page_number, highlighted_context))

    ranked_results.sort(reverse=True, key=lambda x: x[0])
    return ranked_results

def save_results(results, file_name):
    pass

def autocomplete_search(query, trie):
    words = trie.autocomplete(query)
    final = []
    for word in words:
        if word.lower().endswith(('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                                  'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z')):
            final.append(word)
    return final

def search_and_display(query, trie, text_by_page, graph):
    if '"' in query:
        results = search_phrase(query, trie, text_by_page)
    elif any(op in query for op in ['AND', 'OR', 'NOT']):
        results = search_operators(query, trie, text_by_page)
    else:
        results = search(query, trie, text_by_page)
    
    if not results:
        suggestion = did_you_mean(query, trie)
        if suggestion:
            print(f"Da li ste mislili: {suggestion}?")
            user_input = input("Unesite Y za pretragu sa predlogom ili N za izlaz: ").strip().lower()
            if user_input == 'y':
                query = suggestion
                if '"' in query:
                    results = search_phrase(query, trie, text_by_page)
                elif any(op in query for op in ['AND', 'OR', 'NOT']):
                    results = search_operators(query, trie, text_by_page)
                else:
                    results = search(query, trie, text_by_page)
            else:
                return

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
        print("Dobro dosli u pretragu PDF-a. Za izlaz iz programa unesite 'X'.")
        print("Opcije za pretragu: ")
        print("1. Unesite rec za pretragu. Ako unosite više reči, odvojite ih zarezom.")
        print("2. Unesite frazu za pretragu. Fraza se unosi izmedju dva navodnika.")
        print("3. Unesite upit sa operatorima AND, OR, NOT za pretragu.")
        print("4. Autocomplete pretraga. Unesite deo reci za pretragu i '*' na kraju.")
        query = input("Pretraga: ").strip()
        if query == 'x' or query == 'X':
            break
        if not validate_query(query):
            continue

        if query.endswith('*'):
            words = autocomplete_search(query[:-1], trie)
            print("Reči koje počinju sa unetim prefiksom:")
            for i in range(len(words)):
                print(f"{i + 1}. {words[i]}")
            
            while True:
                choice = input("Unesite redni broj reči za pretragu: ")
                if choice == 'x' or choice == 'X':
                    break
                try:
                    choice = int(choice)
                    if choice < 1 or choice > len(words):
                        print("Unesite validan redni broj.")
                        continue
                    query = words[choice - 1]
                    break
                except ValueError:
                    print("Unesite validan redni broj.")
                    continue

        search_and_display(query, trie, text_by_page, graph)

if __name__ == "__main__":
    main()

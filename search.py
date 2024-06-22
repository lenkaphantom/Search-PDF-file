import re

def search(query, trie, text_by_page):
    words = query.split(", ")
    results = {}

    for word in words:
        word_results = trie.starts_with(word)
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
    phrase = query.strip('"')
    words = phrase.split()
    if not words:
        return {}

    initial_results = trie.search(words[0])
    if not initial_results:
        return {}

    results = {}

    for page_number in initial_results:
        page_text = text_by_page[page_number]
        start_index = 0
        while True:
            start_index = page_text.lower().find(words[0].lower(), start_index)
            if start_index == -1:
                break

            end_index = start_index + len(words[0])
            match = True
            for word in words[1:]:
                next_index = page_text.lower().find(word.lower(), end_index)
                if next_index != end_index + 1:
                    match = False
                    break
                end_index = next_index + len(word)

            if match:
                start_context = page_text.rfind('.', 0, start_index) + 1
                if start_context == 0:
                    start_context = page_text.rfind('!', 0, start_index) + 1
                if start_context == 0:
                    start_context = page_text.rfind('?', 0, start_index) + 1
                if start_context == 0:
                    start_context = 0

                end_context = page_text.find('.', end_index)
                if end_context == -1:
                    end_context = page_text.find('!', end_index)
                if end_context == -1:
                    end_context = page_text.find('?', end_index)
                if end_context == -1:
                    end_context = len(page_text)

                context = page_text[start_context:end_context].strip()
                if page_number not in results:
                    results[page_number] = set()
                results[page_number].add(context)

            start_index += 1

    return results


def search_operators(query, trie, text_by_page):
    words = re.split(r'\s+(AND|OR|NOT)\s+', query)
    results = []

    for i in range(0, len(words), 2):
        if '"' in words[i]:
            phrase_results = search_phrase(words[i], trie, text_by_page)
            results.append(phrase_results)
        else:
            word_results = search(words[i], trie, text_by_page)
            results.append(word_results)

    final_results = {}
    current_results = results[0]

    for i in range(1, len(words), 2):
        operator = words[i]
        next_results = results[(i // 2) + 1]

        if operator == 'AND':
            common_pages = set(current_results.keys()) & set(next_results.keys())
            combined_results = {}
            for page in common_pages:
                combined_results[page] = current_results[page].union(next_results[page])
            current_results = combined_results
        elif operator == 'OR':
            all_pages = set(current_results.keys()) | set(next_results.keys())
            combined_results = {}
            for page in all_pages:
                combined_results[page] = current_results.get(page, set()).union(next_results.get(page, set()))
            current_results = combined_results
        elif operator == 'NOT':
            excluded_pages = next_results.keys()
            combined_results = {}
            for page in current_results:
                if page in excluded_pages:
                    continue
                combined_results[page] = current_results[page]
            current_results = combined_results

    final_results = current_results
    return final_results
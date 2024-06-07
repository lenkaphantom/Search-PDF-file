from parsing_pdf import load_parsed_text

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.pages = []

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, page_number):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        node.pages.append(page_number)

    def search(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                return None
            node = node.children[char]
        if node.is_end_of_word:
            return node.pages
        return None

    def starts_with(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return self._collect_all_words(node)

    def _collect_all_words(self, node):
        result = []
        if node.is_end_of_word:
            result.extend(node.pages)
        for child in node.children.values():
            result.extend(self._collect_all_words(child))
        return result

def create_trie(text_by_page):
    trie = Trie()
    for page_number, text in enumerate(text_by_page):
        if text:  # Check if text is not None
            words = text.lower().split()
            for word in words:
                trie.insert(word, page_number)
    return trie

def search_and_display(query, trie, text_by_page):
    results = trie.search(query)
    if results:
        for rank, page_number in enumerate(results):
            context = text_by_page[page_number][:200]  # Prikazuje prvih 200 karaktera kao kontekst
            highlighted_context = context.replace(query, f"\033[1;31m{query}\033[0m")
            print(f"{rank + 1}. Page {page_number + 1}: {highlighted_context}")
    else:
        print("No results found")

def main():
    parsed_text_file = 'parsed_text.json'  # Zameni sa pravom putanjom
    text_by_page = load_parsed_text(parsed_text_file)
    trie = create_trie(text_by_page)

    while True:
        query = input("Enter search query: ").lower()
        if query == 'exit':
            break
        search_and_display(query, trie, text_by_page)

if __name__ == "__main__":
    main()
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.pages = []
        self.word = None

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
        node.word = word

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

    def autocomplete(self, prefix):
        node = self.root
        results = []
        prefix = prefix.lower()

        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]

        self._collect_words(node, results)
        return results

    def _collect_words(self, node, results):
        if node.is_end_of_word:
            results.append(node.word)
        for child_node in node.children.values():
            self._collect_words(child_node, results)

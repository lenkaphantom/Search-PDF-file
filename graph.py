import re
import pickle
from parsing_pdf import load_parsed_text

class Graph:
    class Vertex:
        """ Struktura koja predstavlja čvor grafa."""
        __slots__ = '_element'

        def __init__(self, x):
            self._element = x

        def element(self):
            """Vraća element vezan za čvor grafa."""
            return self._element

        def __hash__(self):
            return hash(id(self))

        def __str__(self):
            return str(self._element)

    class Edge:
        """ Struktura koja predstavlja ivicu grafa """
        __slots__ = '_origin', '_destination', '_element'

        def __init__(self, origin, destination, element=None):
            self._origin = origin
            self._destination = destination
            self._element = element

        def endpoints(self):
            """ Vraća torku (u,v) za čvorove u i v."""
            return self._origin, self._destination

        def opposite(self, v):
            """ Vraća čvor koji se nalazi sa druge strane čvora v ove ivice."""
            if not isinstance(v, Graph.Vertex):
                raise TypeError('v mora biti instanca klase Vertex')
            if self._destination == v:
                return self._origin
            elif self._origin == v:
                return self._destination
            raise ValueError('v nije čvor ivice')

        def element(self):
            """ Vraća element vezan za ivicu"""
            return self._element

        def __hash__(self):
            return hash((self._origin, self._destination))

        def __str__(self):
            return '({0},{1},{2})'.format(self._origin, self._destination, self._element)

    def __init__(self, directed=False):
        """ Kreira prazan graf (podrazumevana vrednost je da je neusmeren).

        Ukoliko se opcioni parametar directed postavi na True, kreira se usmereni graf.
        """
        self._outgoing = {}
        self._incoming = {} if directed else self._outgoing

    def _validate_vertex(self, v):
        """ Proverava da li je v čvor(Vertex) ovog grafa."""
        if not isinstance(v, self.Vertex):
            raise TypeError('Očekivan je objekat klase Vertex')
        if v not in self._outgoing:
            raise ValueError('Vertex ne pripada ovom grafu.')

    def is_directed(self):
        """ Vraća True ako je graf usmeren; False ako je neusmeren."""
        return self._incoming is not self._outgoing

    def vertex_count(self):
        """ Vraća broj čvorova u grafu."""
        return len(self._outgoing)

    def vertices(self):
        """ Vraća iterator nad svim čvorovima grafa."""
        return self._outgoing.keys()

    def edge_count(self):
        """ Vraća broj ivica u grafu."""
        total = sum(len(self._outgoing[v]) for v in self._outgoing)
        return total if self.is_directed() else total // 2

    def edges(self):
        """ Vraća set svih ivica u grafu."""
        result = set()
        for secondary_map in self._outgoing.values():
            result.update(secondary_map.values())
        return result

    def get_edge(self, u, v):
        """ Vraća ivicu između čvorova u i v ili None ako nisu susedni."""
        self._validate_vertex(u)
        self._validate_vertex(v)
        return self._outgoing[u].get(v)

    def degree(self, v, outgoing=True):
        """ Vraća stepen čvora - broj(odlaznih) ivica iz čvora v u grafu.

        Ako je graf usmeren, opcioni parametar outgoing se koristi za brojanje dolaznih ivica.
        """
        self._validate_vertex(v)
        adj = self._outgoing if outgoing else self._incoming
        return len(adj[v])

    def incident_edges(self, v, outgoing=True):
        """ Vraća sve (odlazne) ivice iz čvora v u grafu.

        Ako je graf usmeren, opcioni parametar outgoing se koristi za brojanje dolaznih ivica.
        """
        self._validate_vertex(v)
        adj = self._outgoing if outgoing else self._incoming
        for edge in adj[v].values():
            yield edge

    def insert_vertex(self, x=None):
        """ Ubacuje i vraća novi čvor (Vertex) sa elementom x"""
        v = self.Vertex(x)
        self._outgoing[v] = {}
        if self.is_directed():
            self._incoming[v] = {}
        return v

    def insert_edge(self, u, v, x=None):
        """ Ubacuje i vraća novu ivicu (Edge) od u do v sa pomoćnim elementom x.

        Baca ValueError ako u i v nisu čvorovi grafa.
        Baca ValueError ako su u i v već povezani.
        """
        if self.get_edge(u, v) is not None:
            raise ValueError('u and v are already adjacent')
        e = self.Edge(u, v, x)
        self._outgoing[u][v] = e
        self._incoming[v][u] = e

def find_page_references(text):
    """Pronadji reference ka stranicama u tekstu."""
    page_references = set()
    patterns = [
        r'See page (\d+)',
        r'see page (\d+)',
        r'on page (\d+)',
        r'pages (\d+) and (\d+)',
        r'page (\d+)'
    ]
    for pattern in patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            if isinstance(match, tuple):
                for page in match:
                    page_references.add(int(page))
            else:
                page_references.add(int(match))
    return page_references

def save_graph(graph, output_file):
    """Serijalizacija grafa u fajl."""
    with open(output_file, 'wb') as f:
        pickle.dump(graph, f)

def load_graph(input_file):
    """Deserijalizacija grafa iz fajla."""
    with open(input_file, 'rb') as f:
        graph = pickle.load(f)
    return graph

if __name__ == '__main__':
    # g = Graph(directed=True)
    # text_by_page = load_parsed_text('parsed_text.json')

    # vertices = []
    # for page_number, text in enumerate(text_by_page):
    #     v = g.insert_vertex(page_number)
    #     vertices.append(v)

    # for page_number, text in enumerate(text_by_page):
    #     v = vertices[page_number]
    #     referenced_pages = find_page_references(text)
    #     for ref_page_number in referenced_pages:
    #         if ref_page_number - 1 < len(vertices):
    #             ref_vertex = vertices[ref_page_number - 1]
    #             g.insert_edge(v, ref_vertex)

    # for v in g.vertices():
    #     print(f"Čvor: {v}, Stranica: {v.element()}")

    # for e in g.edges():
    #     print(e)

    # save_graph(g, 'graph.pkl')

    loaded_graph = load_graph('graph.pkl')
    print("\nUčitani graf:")
    for v in loaded_graph.vertices():
        print(f"Čvor: {v}, Stranica: {v.element()}")

    for e in loaded_graph.edges():
        print(e)
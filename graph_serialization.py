from Graph import Graph, find_page_references
from parsing_pdf import load_parsed_text
import pickle

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
    g = Graph(directed=True)
    text_by_page = load_parsed_text('parsed_text.json')

    # Ubacivanje čvorova sa brojevima stranica kao elementima
    vertices = []
    for page_number, text in enumerate(text_by_page):
        v = g.insert_vertex(page_number)
        vertices.append(v)

    # Dodavanje ivica na osnovu referenci u tekstu
    for page_number, text in enumerate(text_by_page):
        v = vertices[page_number]
        referenced_pages = find_page_references(text)
        for ref_page_number in referenced_pages:
            if ref_page_number - 1 < len(vertices):
                ref_vertex = vertices[ref_page_number - 1]
                g.insert_edge(v, ref_vertex)

    # Ispis čvorova i ivica za testiranje
    print("Čvorovi u grafu:")
    for v in g.vertices():
        print(f"Čvor: {v}, Stranica: {v.element()}")

    print("\nIvice u grafu:")
    for e in g.edges():
        print(e)

    # Čuvanje grafa u fajl
    save_graph(g, 'graph.pkl')

    # Učitavanje grafa iz fajla
    loaded_graph = load_graph('graph.pkl')
    print("\nUčitani graf:")
    for v in loaded_graph.vertices():
        print(f"Čvor: {v}, Stranica: {v.element()}")

    for e in loaded_graph.edges():
        print(e)
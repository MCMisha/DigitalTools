import networkx as nx
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog, Button, Label, Text, END, Toplevel
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# Funkcja do wczytania grafu z pliku
def read_graph_from_file(file_path):
    G = nx.Graph()
    with open(file_path, 'r') as file:
        for line in file:
            nodes = line.strip().split(',')
            if len(nodes) == 2:  # Sprawdzamy, czy podano dwie wierzchołki
                G.add_edge(nodes[0], nodes[1])
    return G


# Funkcja sprawdzająca teorię sześciu stopni oddalenia
def check_six_degrees_theory(G):
    result = "Sprawdzanie teorii sześciу stopni oddalenia:\n"
    all_pairs_shortest_paths = dict(nx.all_pairs_shortest_path_length(G))

    theory_holds = True
    for source, targets in all_pairs_shortest_paths.items():
        for target, distance in targets.items():
            result += f"Od {source} do {target}: {distance} stopni\n"
            if distance > 6:  # Jeśli odległość > 6, teoria jest nieprawdziwa
                theory_holds = False

    if theory_holds:
        result += "\nTeoria sześciу stopni oddalenia jest spełniona dla tego grafu!\n"
    else:
        result += "\nTeoria sześciу stopni oddalenia NIE jest spełniona dla tego grafu!\n"
    return result


# Funkcja do wyborу pliku i analizy grafu
def analyze_graph():
    file_path = filedialog.askopenfilename(title="Wybierz plik z danymi grafu", filetypes=[("Pliki tekstowe", "*.txt")])
    if not file_path:
        return

    # Wczytanie grafu
    G = read_graph_from_file(file_path)
    info_text.config(state="normal")
    theory_text.config(state="normal")
    # Wyświetlenie liczby wierzchołków i krawędzi
    info_text.delete("1.0", END)
    info_text.insert(END, f"Liczba wierzchołków: {len(G.nodes)}\n")
    info_text.insert(END, f"Liczba krawędzi: {len(G.edges)}\n")
    info_text.insert(END, f"Gęstość grafu: {nx.density(G):.2f}\n")
    info_text.insert(END, f"Wierzchołki: {list(G.nodes)}\n")
    info_text.insert(END, f"Krawędzie: {list(G.edges)}\n")

    degrees = dict(G.degree())
    max_degree_node = max(degrees, key=degrees.get)
    min_degree_node = min(degrees, key=degrees.get)
    info_text.insert(END, f"Najbardziej połączony wierzchołek: {max_degree_node} (stopień: {degrees[max_degree_node]})\n")
    info_text.insert(END, f"Najmniej połączony wierzchołek: {min_degree_node} (stopień: {degrees[min_degree_node]})\n")

    if nx.is_connected(G):
        avg_path_length = nx.average_shortest_path_length(G)
        diameter = nx.diameter(G)
        info_text.insert(END, f"Średnia długość ścieżki: {avg_path_length:.2f}\n")
        info_text.insert(END, f"Średnica grafu: {diameter}\n")
    else:
        info_text.insert(END, "Graf jest niespójny, więc nie można obliczyć średniej długości ścieżki ani średnicy.\n")

    is_connected = nx.is_connected(G)
    info_text.insert(END, f"Graf jest spójny: {'Tak' if is_connected else 'Nie'}\n")
    components = nx.connected_components(G)
    info_text.insert(END, f"Liczba składowych spójności: {nx.number_connected_components(G)}\n")
    info_text.insert(END, f"Rozmiary składowych spójności: {[len(c) for c in components]}\n")
    info_text.config(state="disabled")
# Sprawdzanie teorii sześciу stopni oddalenia
    theory_result = check_six_degrees_theory(G)
    theory_text.delete("1.0", END)
    theory_text.insert(END, theory_result)
    theory_text.config(state="disabled")
    # Wizualizacja grafu w nowym oknie
    visualize_graph(G)


# Funkcja dо wizualizacji grafu
def visualize_graph(G):
    graph_window = Toplevel(root)
    graph_window.title("Wizualizacja grafu")
    figure = plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G)

    # Rysowanie grafu
    nx.draw_networkx_nodes(G, pos, node_size=1500, node_color='lightblue')
    nx.draw_networkx_edges(G, pos, width=2, edge_color='gray')
    nx.draw_networkx_labels(G, pos, font_size=10, font_color='black')
    plt.title("Graf wczytany z pliku", fontsize=14)
    plt.axis('off')

    # Umieszczenie grafu w oknie Tkinter
    canvas = FigureCanvasTkAgg(figure, graph_window)
    canvas.get_tk_widget().pack()
    canvas.draw()


def on_closing():
    root.quit()
    root.destroy()

# Główne oknо aplikacji
root = Tk()
root.title("Analiza grafu - teoria sześciу stopni oddalenia")
root.geometry("800x500")

root.protocol("WM_DELETE_WINDOW", on_closing)

# Etykieta i przycisk do wyborу pliku
Label(root, text="Analiza grafu wczytanego z pliku", font=("Arial", 14)).pack(pady=10)
Button(root, text="Wybierz plik i analizuj graf", command=analyze_graph, font=("Arial", 12)).pack(pady=10)

# Pole tekstowe dla informacji o grafie
Label(root, text="Informacje o grafie:", font=("Arial", 12)).pack(pady=5)
info_text = Text(root, height=6, width=90, font=("Arial", 10))

info_text.pack(pady=5)

# Pole tekstowe dla informacji o sprawdzieniu teorii
Label(root, text="Wynik sprawdzania teorii sześciu stopni oddalenia:", font=("Arial", 12)).pack(pady=5)
theory_text = Text(root, height=12, width=90, font=("Arial", 10))
theory_text.pack(pady=5)

# Uruchomienie aplikacji
root.mainloop()

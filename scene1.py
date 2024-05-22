import tkinter as tk
from collections import defaultdict
import heapq

class CampusMapApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Campus Map")

        self.canvas = tk.Canvas(root, width=800, height=600, bg="white")
        self.canvas.pack()

        # Define nodes with coordinates
        self.nodes = {
            "Entrance": (425, 575),
            "Student Center 1": (200, 550),
            "Registrar's office": (480, 425),
            "Accounting Office": (100, 300),
            "Canteen": (200, 125),
            "Library": (335, 125),
            "Guidance Office": (445, 125),
            "Another Office": (600, 300),
            "Parking Lot": (350, 275)
        }

        # Define edges between nodes
        self.edges = [
            ("Entrance", "Student Center 1"),
            ("Entrance", "Registrar's office"),
            ("Student Center 1", "Accounting Office"),
            ("Registrar's office", "Parking Lot"),
            ("Registrar's office", "Another Office"),
            ("Accounting Office", "Canteen"),
            ("Canteen", "Library"),
            ("Library", "Guidance Office"),
            ("Parking Lot", "Library"),
            ("Registrar's office", "Student Center 1"),
            ("Another Office", "Parking Lot")
        ]

        self.draw_map()

        # Dropdown menu for start and end points
        self.start_var = tk.StringVar(root)
        self.end_var = tk.StringVar(root)
        self.start_var.set("Entrance")
        self.end_var.set("Canteen")
        self.start_dropdown = tk.OptionMenu(root, self.start_var, *self.nodes.keys())
        self.end_dropdown = tk.OptionMenu(root, self.end_var, *self.nodes.keys())
        self.start_dropdown.pack()
        self.end_dropdown.pack()

        # Button to find shortest path
        self.find_path_button = tk.Button(root, text="Find Shortest Path", command=self.find_shortest_path)
        self.find_path_button.pack()

    def draw_map(self):
        # Draw nodes as rectangles with text
        self.node_shapes = {}
        for node, (x, y) in self.nodes.items():
            rect = self.canvas.create_rectangle(x - 50, y - 50, x + 50, y + 50, fill="cyan", outline="cyan")
            text = self.canvas.create_text(x, y, text=node, fill="black")
            self.node_shapes[node] = (rect, text)

        # Draw edges
        self.edge_shapes = {}
        for start, end in self.edges:
            x1, y1 = self.nodes[start]
            x2, y2 = self.nodes[end]
            line = self.canvas.create_line(x1, y1, x2, y2, fill="black")
            self.edge_shapes[(start, end)] = line

    def find_shortest_path(self):
        start_node = self.start_var.get()
        end_node = self.end_var.get()
        shortest_path = self.calculate_shortest_path(start_node, end_node)

        # Change color of nodes and edges along shortest path
        for node, (rect, text) in self.node_shapes.items():
            if node in shortest_path:
                self.canvas.itemconfig(rect, fill="red", outline="red")
            else:
                self.canvas.itemconfig(rect, fill="cyan", outline="cyan")

        for i in range(len(shortest_path) - 1):
            edge = (shortest_path[i], shortest_path[i+1])
            self.canvas.itemconfig(self.edge_shapes[edge], fill="black")

    def calculate_shortest_path(self, start_node, end_node):
        # Calculate shortest path using Dijkstra's algorithm
        graph = defaultdict(dict)
        for start, end in self.edges:
            x1, y1 = self.nodes[start]
            x2, y2 = self.nodes[end]
            distance = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
            graph[start][end] = distance
            graph[end][start] = distance

        pq = [(0, start_node)]
        visited = set()
        shortest_paths = {}
        while pq:
            dist, node = heapq.heappop(pq)
            if node in visited:
                continue
            visited.add(node)
            shortest_paths[node] = dist
            for neighbor, weight in graph[node].items():
                if neighbor not in visited:
                    heapq.heappush(pq, (dist + weight, neighbor))

        # Reconstruct shortest path
        path = []
        while end_node != start_node:
            path.append(end_node)
            end_node = min((shortest_paths[node], node) for node in graph[end_node])[1]
        path.append(start_node)
        return path[::-1]

if __name__ == "__main__":
    root = tk.Tk()
    app = CampusMapApp(root)
    root.mainloop()

"""
graph.py
Modulo de Grafos - Proyecto Final Matematica Discreta
UMG Chiquimula

Implementa una estructura de grafo (dirigido o no dirigido, con pesos)

Operaciones requeridas por el enunciado:
    - Insercion de nodo
    - Eliminacion de nodo
    - Vaciado del grafo
    - Insertar arista
    - Eliminar aristas
    - Ver pesos

    Autores: * Ronny Steve Mijangos Felipe
             * Emilio José Felipe Mellado 
             * Diego Fernando Alberto Nufio Guerra
             * Franklin De Jesús Hernández López
"""

import graphviz


class Graph:
    """Representa un grafo mediante lista de adyacencia.

    self.adj es un diccionario de la forma:
        { nodo: { nodo_vecino: peso, ... }, ... }
    """

    def __init__(self, directed: bool = True):
        self.directed = directed
        self.adj = {}

    # ---------- NODOS ----------

    def add_node(self, node) -> bool:
        """Inserta un nodo. Retorna False si ya existia."""
        node = str(node)
        if node in self.adj:
            return False
        self.adj[node] = {}
        return True

    def remove_node(self, node) -> bool:
        """Elimina un nodo y todas las aristas relacionadas a el."""
        node = str(node)
        if node not in self.adj:
            return False
        del self.adj[node]
        for otro in self.adj:
            self.adj[otro].pop(node, None)
        return True

    def clear(self) -> None:
        """Vacia por completo el grafo (nodos y aristas)."""
        self.adj.clear()

    def nodes(self):
        return list(self.adj.keys())

    # ---------- ARISTAS ----------

    def add_edge(self, origen, destino, peso: float = 1) -> None:
        """Inserta una arista. Si los nodos no existen, se crean."""
        origen, destino = str(origen), str(destino)
        self.add_node(origen)
        self.add_node(destino)
        self.adj[origen][destino] = peso
        if not self.directed:
            self.adj[destino][origen] = peso

    def remove_edge(self, origen, destino) -> bool:
        """Elimina una arista entre origen y destino."""
        origen, destino = str(origen), str(destino)
        eliminado = False
        if origen in self.adj and destino in self.adj[origen]:
            del self.adj[origen][destino]
            eliminado = True
        if not self.directed and destino in self.adj and origen in self.adj[destino]:
            del self.adj[destino][origen]
            eliminado = True
        return eliminado

    def edges(self):
        """Retorna una lista de tuplas (origen, destino, peso)."""
        vistos = set()
        resultado = []
        for u in self.adj:
            for v, w in self.adj[u].items():
                if self.directed:
                    resultado.append((u, v, w))
                else:
                    clave = tuple(sorted([u, v]))
                    if clave not in vistos:
                        vistos.add(clave)
                        resultado.append((u, v, w))
        return resultado

    # ---------- VISUALIZACION (Graphviz / dot) ----------

    def to_dot(self) -> "graphviz.Graph | graphviz.Digraph":
        """Construye el objeto graphviz listo para renderizar."""
        g = graphviz.Digraph() if self.directed else graphviz.Graph()
        g.attr("graph", bgcolor="transparent", pad="0.3", nodesep="0.6", ranksep="0.7")
        g.attr("node", shape="circle", style="filled", fillcolor="#6366f1",
               fontcolor="white", fontname="Segoe UI", fontsize="14",
               color="#818cf8", penwidth="2")
        g.attr("edge", fontname="Segoe UI", fontsize="11", color="#22c55e",
               fontcolor="#e5e7eb", penwidth="2", arrowsize="0.8")

        for n in self.adj:
            g.node(n)

        for u, v, w in self.edges():
            g.edge(u, v, label=str(w))

        return g

    def render_png(self, filepath_sin_extension: str) -> str:
        """Genera un archivo PNG del grafo y retorna la ruta final."""
        dot = self.to_dot()
        ruta = dot.render(filename=filepath_sin_extension, format="png", cleanup=True)
        return ruta

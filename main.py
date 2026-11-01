"""
main.py
Proyecto Final - Matematica Discreta - UMG Chiquimula
Modulo: Grafos

Interfaz grafica en Tkinter que permite:
    - Insertar nodo
    - Eliminar nodo
    - Vaciar el grafo
    - Insertar arista (con peso)
    - Eliminar arista
    - Ver pesos (tabla de aristas)

Autores: * Ronny Steve Mijangos Felipe
         * Emilio José Felipe Mellado 
         * Diego Fernando Alberto Nufio Guerra
         * Franklin De Jesús Hernández López
"""

import os
import tempfile
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from PIL import Image, ImageTk

from graph import Graph


# ---------------------------------------------------------------------
# PALETA DE COLORES (tema oscuro moderno)
# ---------------------------------------------------------------------
COLOR_BG = "#0f172a"          # fondo general (azul muy oscuro)
COLOR_SIDEBAR = "#111827"     # barra lateral
COLOR_CARD = "#1e293b"        # tarjetas / lienzo
COLOR_ACCENT = "#6366f1"      # morado/indigo (acento principal)
COLOR_ACCENT_HOVER = "#818cf8"
COLOR_TEXT = "#e5e7eb"
COLOR_MUTED = "#94a3b8"
COLOR_SUCCESS = "#22c55e"
COLOR_DANGER = "#ef4444"
COLOR_WARNING = "#f59e0b"


class GraphApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Proyecto Final - Matematica Discreta - UMG Chiquimula")
        self.geometry("1050x680")
        self.configure(bg=COLOR_BG)
        self.minsize(900, 600)

        # Grafo dirigido con pesos (puedes cambiar directed=False si lo necesitas)
        self.graph = Graph(directed=True)
        self._tmp_dir = tempfile.mkdtemp(prefix="grafos_umg_")
        self._img_tk = None  # referencia viva para que Tkinter no la borre (GC)

        self._build_menu()
        self._build_topbar()
        self._build_body()

        self._render_graph()

    # ------------------------------------------------------------------
    # BOTONES CON EFECTO HOVER
    # ------------------------------------------------------------------
    def _make_button(self, parent, texto, icono, comando, color=COLOR_ACCENT,
                      color_hover=COLOR_ACCENT_HOVER):
        btn = tk.Button(
            parent, text=f"  {icono}   {texto}", command=comando,
            anchor="w", width=24, height=2,
            bg=color, fg="white", activebackground=color_hover,
            activeforeground="white", relief="flat", bd=0,
            font=("Segoe UI", 10, "bold"), cursor="hand2",
            padx=10
        )
        btn.bind("<Enter>", lambda e: btn.configure(bg=color_hover))
        btn.bind("<Leave>", lambda e: btn.configure(bg=color))
        return btn

    # ------------------------------------------------------------------
    # CONSTRUCCION DE INTERFAZ
    # ------------------------------------------------------------------

    def _build_menu(self):
        """Barra de menu superior (INICIO / MENUS+ / MANUAL / INFO)."""
        menubar = tk.Menu(self)

        menu_inicio = tk.Menu(menubar, tearoff=0)
        menu_inicio.add_command(label="Ir a Inicio", command=self._ir_inicio)
        menubar.add_cascade(label="Inicio", menu=menu_inicio)

        menu_modulos = tk.Menu(menubar, tearoff=0)
        menu_modulos.add_command(label="Grafos", command=self._ir_inicio)
        # Aqui se agregarian mas modulos del curso en el futuro,
        # ej: menu_modulos.add_command(label="Arboles", command=self._ir_arboles)
        menubar.add_cascade(label="Menus+", menu=menu_modulos)

        menu_manual = tk.Menu(menubar, tearoff=0)
        menu_manual.add_command(label="Ver manual de usuario", command=self._mostrar_manual)
        menubar.add_cascade(label="Manual de Usuario", menu=menu_manual)

        menu_info = tk.Menu(menubar, tearoff=0)
        menu_info.add_command(label="Acerca del software", command=self._mostrar_info)
        menubar.add_cascade(label="Informacion Software", menu=menu_info)

        self.config(menu=menubar)

    def _build_topbar(self):
        barra = tk.Frame(self, bg=COLOR_SIDEBAR, height=56)
        barra.pack(side="top", fill="x")
        barra.pack_propagate(False)

        # Franja de acento a la izquierda del titulo
        tk.Frame(barra, bg=COLOR_ACCENT, width=5).pack(side="left", fill="y")

        titulo = tk.Frame(barra, bg=COLOR_SIDEBAR)
        titulo.pack(side="left", padx=15, pady=6)
        tk.Label(
            titulo, text="🔷 MODULO: GRAFOS", bg=COLOR_SIDEBAR, fg="white",
            font=("Segoe UI", 14, "bold"), anchor="w"
        ).pack(anchor="w")
        tk.Label(
            titulo, text="Matematica Discreta · UMG Chiquimula", bg=COLOR_SIDEBAR,
            fg=COLOR_MUTED, font=("Segoe UI", 9), anchor="w"
        ).pack(anchor="w")

    def _build_body(self):
        body = tk.Frame(self, bg=COLOR_BG)
        body.pack(fill="both", expand=True, padx=15, pady=15)

        # --- Panel izquierdo: canvas donde se dibuja el grafo ---
        left = tk.Frame(body, bg=COLOR_CARD, bd=0, highlightthickness=1,
                         highlightbackground="#334155")
        left.pack(side="left", fill="both", expand=True, padx=(0, 15))

        tk.Label(
            left, text="Visualizacion del Grafo", bg=COLOR_CARD, fg=COLOR_TEXT,
            font=("Segoe UI", 11, "bold"), anchor="w"
        ).pack(fill="x", padx=15, pady=(12, 0))

        self.canvas_label = tk.Label(left, bg=COLOR_CARD)
        self.canvas_label.pack(fill="both", expand=True, padx=15, pady=15)

        # --- Panel derecho: controles ---
        right = tk.Frame(body, bg=COLOR_SIDEBAR, width=280, highlightthickness=1,
                          highlightbackground="#334155")
        right.pack(side="right", fill="y")
        right.pack_propagate(False)

        tk.Label(
            right, text="⚙  OPERACIONES", bg=COLOR_SIDEBAR, fg=COLOR_TEXT,
            font=("Segoe UI", 11, "bold")
        ).pack(pady=(20, 15), padx=20, anchor="w")

        botones = [
            ("Insertar Nodo", "➕", self.insertar_nodo, COLOR_SUCCESS, "#4ade80"),
            ("Eliminar Nodo", "➖", self.eliminar_nodo, COLOR_DANGER, "#f87171"),
            ("Vaciar Grafo", "🗑", self.vaciar_grafo, COLOR_WARNING, "#fbbf24"),
            ("Insertar Arista", "🔗", self.insertar_arista, COLOR_ACCENT, COLOR_ACCENT_HOVER),
            ("Eliminar Arista", "✂", self.eliminar_arista, "#ec4899", "#f472b6"),
            ("Ver Pesos", "📊", self.ver_pesos, "#0ea5e9", "#38bdf8"),
        ]

        for texto, icono, comando, color, hover in botones:
            self._make_button(right, texto, icono, comando, color, hover).pack(
                pady=6, padx=20, fill="x"
            )

        # Contador de nodos/aristas en vivo
        self.contador_var = tk.StringVar(value="Nodos: 0   |   Aristas: 0")
        tk.Label(
            right, textvariable=self.contador_var, bg=COLOR_SIDEBAR, fg=COLOR_MUTED,
            font=("Segoe UI", 9)
        ).pack(side="bottom", pady=20)

        self.status_var = tk.StringVar(value="Se encuentra en Opcion: Grafo")
        status = tk.Label(
            self, textvariable=self.status_var, anchor="w", bg=COLOR_SIDEBAR,
            fg=COLOR_MUTED, font=("Segoe UI", 9), padx=15, pady=6
        )
        status.pack(side="bottom", fill="x")

    # ------------------------------------------------------------------
    # ACCIONES DE MENU
    # ------------------------------------------------------------------

    def _ir_inicio(self):
        self.status_var.set("Se encuentra en Opcion: Grafo")

    def _mostrar_manual(self):
        texto = (
            "MANUAL DE USUARIO - MODULO GRAFOS\n\n"
            "1. Insertar Nodo: agrega un nuevo vertice al grafo.\n"
            "2. Eliminar Nodo: elimina un vertice y sus aristas asociadas.\n"
            "3. Vaciar Grafo: elimina todos los nodos y aristas.\n"
            "4. Insertar Arista: crea una conexion entre dos nodos con un peso.\n"
            "5. Eliminar Arista: borra la conexion entre dos nodos.\n"
            "6. Ver Pesos: muestra una tabla con todas las aristas y su peso."
        )
        messagebox.showinfo("Manual de Usuario", texto)

    def _mostrar_info(self):
        texto = (
            "Universidad Mariano Galvez de Guatemala\n"
            "Extension Chiquimula - Facultad de Ingenieria\n"
            "Curso: Matematica Discreta\n"
            "Proyecto Final - Modulo de Grafos\n"
            "Lenguaje: Python (Tkinter + Graphviz)"
        )
        messagebox.showinfo("Informacion del Software", texto)

    # ------------------------------------------------------------------
    # OPERACIONES DEL GRAFO
    # ------------------------------------------------------------------

    def insertar_nodo(self):
        valor = simpledialog.askstring("Insertar Nodo", "Nombre/valor del nodo:")
        if valor is None or valor.strip() == "":
            return
        if self.graph.add_node(valor.strip()):
            self.status_var.set(f"✅ Nodo '{valor}' insertado.")
        else:
            messagebox.showwarning("Aviso", f"El nodo '{valor}' ya existe.")
        self._render_graph()

    def eliminar_nodo(self):
        valor = simpledialog.askstring("Eliminar Nodo", "Nombre/valor del nodo a eliminar:")
        if valor is None or valor.strip() == "":
            return
        if self.graph.remove_node(valor.strip()):
            self.status_var.set(f"🗑 Nodo '{valor}' eliminado.")
        else:
            messagebox.showwarning("Aviso", f"El nodo '{valor}' no existe.")
        self._render_graph()

    def vaciar_grafo(self):
        if not self.graph.nodes():
            messagebox.showinfo("Aviso", "El grafo ya esta vacio.")
            return
        if messagebox.askyesno("Confirmar", "¿Seguro que desea vaciar todo el grafo?"):
            self.graph.clear()
            self.status_var.set("🧹 Grafo vaciado por completo.")
            self._render_graph()

    def insertar_arista(self):
        origen = simpledialog.askstring("Insertar Arista", "Nodo origen:")
        if origen is None or origen.strip() == "":
            return
        destino = simpledialog.askstring("Insertar Arista", "Nodo destino:")
        if destino is None or destino.strip() == "":
            return
        peso = simpledialog.askfloat("Insertar Arista", "Peso de la arista:", initialvalue=1)
        if peso is None:
            return
        self.graph.add_edge(origen.strip(), destino.strip(), peso)
        self.status_var.set(f"🔗 Arista {origen} → {destino} (peso {peso}) insertada.")
        self._render_graph()

    def eliminar_arista(self):
        origen = simpledialog.askstring("Eliminar Arista", "Nodo origen:")
        if origen is None or origen.strip() == "":
            return
        destino = simpledialog.askstring("Eliminar Arista", "Nodo destino:")
        if destino is None or destino.strip() == "":
            return
        if self.graph.remove_edge(origen.strip(), destino.strip()):
            self.status_var.set(f"✂ Arista {origen} → {destino} eliminada.")
        else:
            messagebox.showwarning("Aviso", "Esa arista no existe.")
        self._render_graph()

    def ver_pesos(self):
        ventana = tk.Toplevel(self)
        ventana.title("📊 Ver Pesos - Aristas del Grafo")
        ventana.geometry("420x380")
        ventana.configure(bg=COLOR_CARD)

        tk.Label(
            ventana, text="📊 Pesos de las Aristas", bg=COLOR_CARD, fg=COLOR_TEXT,
            font=("Segoe UI", 12, "bold")
        ).pack(pady=(15, 10))

        estilo = ttk.Style()
        estilo.theme_use("clam")
        estilo.configure("Custom.Treeview", background=COLOR_CARD, fieldbackground=COLOR_CARD,
                          foreground=COLOR_TEXT, rowheight=28, font=("Segoe UI", 10))
        estilo.configure("Custom.Treeview.Heading", background=COLOR_ACCENT,
                          foreground="white", font=("Segoe UI", 10, "bold"))
        estilo.map("Custom.Treeview", background=[("selected", COLOR_ACCENT_HOVER)])

        cols = ("Origen", "Destino", "Peso")
        tabla = ttk.Treeview(ventana, columns=cols, show="headings", style="Custom.Treeview")
        for c in cols:
            tabla.heading(c, text=c)
            tabla.column(c, anchor="center")
        tabla.pack(fill="both", expand=True, padx=15, pady=10)

        for origen, destino, peso in self.graph.edges():
            tabla.insert("", "end", values=(origen, destino, peso))

        if not self.graph.edges():
            tk.Label(
                ventana, text="No hay aristas registradas.", bg=COLOR_CARD,
                fg=COLOR_MUTED, font=("Segoe UI", 10)
            ).pack(pady=10)

    # ------------------------------------------------------------------
    # RENDERIZADO DEL GRAFO CON GRAPHVIZ
    # ------------------------------------------------------------------

    def _render_graph(self):
        ruta_base = os.path.join(self._tmp_dir, "grafo_actual")
        try:
            if self.graph.nodes():
                ruta_png = self.graph.render_png(ruta_base)
                imagen = Image.open(ruta_png)
                # Ajustar tamano si es muy grande
                imagen.thumbnail((650, 500))
                self._img_tk = ImageTk.PhotoImage(imagen)
                self.canvas_label.configure(image=self._img_tk, text="")
            else:
                self._img_tk = None
                self.canvas_label.configure(
                    image="", text="🌐  (Grafo vacio)\n\nUsa los botones de la derecha\npara comenzar a construirlo",
                    font=("Segoe UI", 13), fg=COLOR_MUTED, bg=COLOR_CARD, justify="center"
                )
        except Exception as e:
            messagebox.showerror("Error al graficar", str(e))

        # Actualiza el contador de nodos y aristas
        self.contador_var.set(
            f"🔵 Nodos: {len(self.graph.nodes())}   |   🔗 Aristas: {len(self.graph.edges())}"
        )


if __name__ == "__main__":
    app = GraphApp()
    app.mainloop()

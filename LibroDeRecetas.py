"""
ADA3 - Listas | Libro de Recetas (POSTRES)

Ejercicio 1: arreglo POSTRES ordenado alfabeticamente; cada elemento tiene
             una lista ligada con los ingredientes del postre.
Ejercicio 2: subprograma eliminar_repetidos() que elimina de forma automatica
             los elementos repetidos de POSTRES y reporta que paso con las listas.

Estructura de datos:
    POSTRES = [ Postre, Postre, ... ]   <- arreglo ordenado alfabeticamente
    Postre  -> nombre + cabeza          <- cabeza apunta al primer Nodo
    Nodo    -> ingrediente + siguiente  <- el ultimo apunta a None (NIL)

Requiere solo Python 3 (tkinter ya viene incluido).
"""

import tkinter as tk
from tkinter import messagebox, simpledialog


# ---------------------------------------------------------------------------
# Estructuras de datos (lista ligada de ingredientes)
# ---------------------------------------------------------------------------
class Nodo:
    def __init__(self, ingrediente):
        self.ingrediente = ingrediente
        self.siguiente = None  # None = NIL


class Postre:
    def __init__(self, nombre):
        self.nombre = nombre
        self.cabeza = None

    def esta_vacia(self):
        return self.cabeza is None

    def buscar(self, ingrediente):
        actual = self.cabeza
        while actual is not None:
            if actual.ingrediente == ingrediente:
                return actual
            actual = actual.siguiente
        return None

    def insertar(self, ingrediente):
        """Inserta al final. False si ya existia."""
        if self.buscar(ingrediente) is not None:
            return False
        nuevo = Nodo(ingrediente)
        if self.cabeza is None:
            self.cabeza = nuevo
        else:
            actual = self.cabeza
            while actual.siguiente is not None:
                actual = actual.siguiente
            actual.siguiente = nuevo
        return True

    def eliminar(self, ingrediente):
        """Elimina primero, intermedio o ultimo. False si no existe."""
        anterior, actual = None, self.cabeza
        while actual is not None and actual.ingrediente != ingrediente:
            anterior, actual = actual, actual.siguiente
        if actual is None:
            return False
        if anterior is None:
            self.cabeza = actual.siguiente
        else:
            anterior.siguiente = actual.siguiente
        return True

    def modificar(self, viejo, nuevo):
        nodo = self.buscar(viejo)
        if nodo is None:
            return "no_existe"
        if viejo != nuevo and self.buscar(nuevo) is not None:
            return "duplicado"
        nodo.ingrediente = nuevo
        return "ok"

    def ingredientes(self):
        lista, actual = [], self.cabeza
        while actual is not None:
            lista.append(actual.ingrediente)
            actual = actual.siguiente
        return lista

    def liberar(self):
        """Desliga todos los nodos de la lista (equivale a 'free' en C/Pascal)."""
        actual = self.cabeza
        while actual is not None:
            siguiente = actual.siguiente
            actual.siguiente = None
            actual = siguiente
        self.cabeza = None


POSTRES = []  # arreglo ordenado alfabeticamente


def normalizar(texto):
    return " ".join((texto or "").strip().lower().split())


def buscar_postre(nombre):
    """Busqueda binaria (primera aparicion).
    Regresa (encontrado, posicion). Si no esta, posicion = donde insertarlo."""
    bajo, alto = 0, len(POSTRES)
    while bajo < alto:
        medio = (bajo + alto) // 2
        if POSTRES[medio].nombre < nombre:
            bajo = medio + 1
        else:
            alto = medio
    encontrado = bajo < len(POSTRES) and POSTRES[bajo].nombre == nombre
    return encontrado, bajo


def separar_ingredientes(texto):
    """'harina, huevo, harina' -> ['harina', 'huevo'] (sin vacios ni repetidos)."""
    resultado = []
    for parte in (texto or "").split(","):
        ing = normalizar(parte)
        if ing and ing not in resultado:
            resultado.append(ing)
    return resultado


def recortar(texto, limite):
    return texto if len(texto) <= limite else texto[: limite - 1] + "…"


# ---------------------------------------------------------------------------
# EJERCICIO 2: subprograma que elimina automaticamente los repetidos
# ---------------------------------------------------------------------------
def eliminar_repetidos(fusionar=False):
    """Elimina de POSTRES todos los elementos repetidos (mismo nombre).

    Como POSTRES esta ordenado, los repetidos quedan juntos, asi que basta
    una sola pasada: se conserva la PRIMERA aparicion y se descartan las copias.

    fusionar=False -> la copia se elimina completa, con su lista de ingredientes.
    fusionar=True  -> antes de eliminar la copia, sus ingredientes que no
                      estaban en el original se pasan a la lista del original.

    Regresa (informe, antes, despues). 'informe' es un dict:
        nombre -> {"copias": n, "perdidos": [...], "fusionados": [...]}
    """
    antes = len(POSTRES)
    informe = {}
    unicos = []
    for postre in POSTRES:
        if unicos and unicos[-1].nombre == postre.nombre:
            base = unicos[-1]
            reg = informe.setdefault(
                postre.nombre, {"copias": 0, "perdidos": [], "fusionados": []})
            reg["copias"] += 1
            for ing in postre.ingredientes():
                if base.buscar(ing) is None:          # solo existia en la copia
                    if fusionar:
                        base.insertar(ing)
                        reg["fusionados"].append(ing)
                    elif ing not in reg["perdidos"]:
                        reg["perdidos"].append(ing)
            postre.liberar()                           # se desliga la lista de la copia
        else:
            unicos.append(postre)
    POSTRES[:] = unicos                                # el arreglo se actualiza en su lugar
    return informe, antes, len(POSTRES)


def texto_informe(informe, antes, despues, fusionar):
    lineas = [
        "INFORME: ELIMINAR REPETIDOS",
        "",
        "Modo: " + ("fusionar ingredientes de las copias con el original"
                    if fusionar else "eliminar las copias completas con sus listas"),
        f"Elementos en POSTRES  →  antes: {antes}   después: {despues}   "
        f"eliminados: {antes - despues}",
        "",
    ]
    for nombre, reg in informe.items():
        lineas.append(f"• {nombre.title()}: {reg['copias']} copia(s) eliminada(s)")
        if reg["fusionados"]:
            lineas.append("    Ingredientes de las copias pasados al original: "
                          + ", ".join(reg["fusionados"]))
        elif reg["perdidos"]:
            lineas.append("    Ingredientes que SE PERDIERON (solo estaban en la copia): "
                          + ", ".join(reg["perdidos"]))
        else:
            lineas.append("    Las copias no tenían ingredientes distintos; no se perdió nada.")
    return "\n".join(lineas)


# ---------------------------------------------------------------------------
# Interfaz: libro de recetas
# ---------------------------------------------------------------------------
CUERO = "#4a2c1a"
BORDE = "#2e1a0f"
LOMO = "#8b6b3d"
PAGINA = "#f4e8c8"
TINTA = "#3b2a1a"
ACENTO = "#8b5a2b"
ACENTO_OSC = "#6d4520"
CREMA = "#fff6e0"
LINEA = "#c9b17a"
NODO = "#fffaf0"
VINO = "#7a2e2e"
VINO_OSC = "#5c2020"

SERIF = "Georgia"


class LibroRecetas:
    def __init__(self, root):
        self.root = root
        self.pos = None  # posicion en POSTRES del postre abierto
        root.title("Libro de Recetas - POSTRES")
        root.geometry("1000x700")
        root.minsize(900, 640)
        root.configure(bg=CUERO)

        tk.Label(root, text="Libro de Recetas", font=(SERIF, 24, "bold italic"),
                 bg=CUERO, fg=CREMA).pack(pady=(12, 4))

        libro = tk.Frame(root, bg=BORDE, padx=6, pady=6)
        libro.pack(fill="both", expand=True, padx=24, pady=(0, 18))
        libro.rowconfigure(0, weight=1)
        libro.columnconfigure(2, weight=1)

        self._crear_pagina_izquierda(libro)
        tk.Frame(libro, bg=LOMO, width=8).grid(row=0, column=1, sticky="ns")
        self._crear_pagina_derecha(libro)

        self.estado = tk.Label(root, text="", font=(SERIF, 10, "italic"),
                               bg=CUERO, fg=CREMA)
        self.estado.pack(pady=(0, 8))

        self.refrescar_indice()

    # ----- construccion de widgets -----
    def boton(self, padre, texto, comando, color=ACENTO, color_osc=ACENTO_OSC):
        return tk.Button(padre, text=texto, command=comando, bg=color, fg=CREMA,
                         activebackground=color_osc, activeforeground=CREMA,
                         relief="flat", font=(SERIF, 10, "bold"), padx=10, pady=5,
                         cursor="hand2", bd=0)

    def _crear_pagina_izquierda(self, libro):
        pag = tk.Frame(libro, bg=PAGINA, padx=18, pady=16, width=310)
        pag.grid(row=0, column=0, sticky="ns")
        pag.grid_propagate(False)
        pag.pack_propagate(False)

        tk.Label(pag, text="Índice", font=(SERIF, 20, "bold"),
                 bg=PAGINA, fg=TINTA).pack(anchor="w")
        tk.Frame(pag, bg=LINEA, height=2).pack(fill="x", pady=(2, 8))

        # los botones se empacan primero (abajo) para que siempre se vean
        botones = tk.Frame(pag, bg=PAGINA)
        botones.pack(side="bottom", fill="x", pady=(10, 0))
        for texto, cmd in (("Nuevo postre", self.alta_postre),
                           ("Cambiar nombre", self.renombrar_postre),
                           ("Eliminar postre", self.baja_postre)):
            self.boton(botones, texto, cmd).pack(fill="x", pady=3)
        tk.Frame(botones, bg=LINEA, height=2).pack(fill="x", pady=6)
        tk.Label(botones, text="Ejercicio 2", font=(SERIF, 10, "italic"),
                 bg=PAGINA, fg=VINO).pack(anchor="w")
        self.boton(botones, "Duplicar postre (prueba)",
                   self.duplicar_postre_prueba, VINO, VINO_OSC).pack(fill="x", pady=3)
        self.boton(botones, "Eliminar repetidos",
                   self.eliminar_repetidos_ui, VINO, VINO_OSC).pack(fill="x", pady=3)

        marco = tk.Frame(pag, bg=PAGINA)
        marco.pack(fill="both", expand=True)
        sb = tk.Scrollbar(marco)
        sb.pack(side="right", fill="y")
        self.lista_postres = tk.Listbox(
            marco, font=(SERIF, 13), bg=PAGINA, fg=TINTA, bd=0,
            highlightthickness=0, selectbackground=ACENTO,
            selectforeground=CREMA, activestyle="none", exportselection=False,
            yscrollcommand=sb.set)
        self.lista_postres.pack(side="left", fill="both", expand=True)
        sb.config(command=self.lista_postres.yview)
        self.lista_postres.bind("<<ListboxSelect>>", self.al_elegir_postre)

    def _crear_pagina_derecha(self, libro):
        pag = tk.Frame(libro, bg=PAGINA, padx=22, pady=16)
        pag.grid(row=0, column=2, sticky="nsew")

        self.titulo = tk.Label(pag, text="", font=(SERIF, 24, "bold italic"),
                               bg=PAGINA, fg=TINTA, anchor="w")
        self.titulo.pack(fill="x")
        tk.Frame(pag, bg=LINEA, height=2).pack(fill="x", pady=(2, 6))
        self.subtitulo = tk.Label(pag, text="", font=(SERIF, 12, "italic"),
                                  bg=PAGINA, fg=ACENTO, anchor="w")
        self.subtitulo.pack(fill="x")

        marco = tk.Frame(pag, bg=PAGINA)
        marco.pack(fill="both", expand=True, pady=6)
        sb = tk.Scrollbar(marco)
        sb.pack(side="right", fill="y")
        self.lista_ing = tk.Listbox(
            marco, font=(SERIF, 14), bg=PAGINA, fg=TINTA, bd=0,
            highlightthickness=0, selectbackground=ACENTO,
            selectforeground=CREMA, activestyle="none", exportselection=False,
            yscrollcommand=sb.set)
        self.lista_ing.pack(side="left", fill="both", expand=True)
        sb.config(command=self.lista_ing.yview)
        self.lista_ing.bind("<Double-Button-1>", lambda e: self.modificar_ingrediente())

        botones = tk.Frame(pag, bg=PAGINA)
        botones.pack(fill="x", pady=4)
        for texto, cmd in (("Agregar ingrediente", self.agregar_ingredientes),
                           ("Modificar", self.modificar_ingrediente),
                           ("Eliminar", self.eliminar_ingrediente),
                           ("Reemplazar receta", self.reemplazar_receta)):
            self.boton(botones, texto, cmd).pack(side="left", padx=(0, 6))

        tk.Label(pag, text="Así se guarda en memoria (lista ligada):",
                 font=(SERIF, 11, "italic"), bg=PAGINA, fg=ACENTO,
                 anchor="w").pack(fill="x", pady=(10, 2))
        zona = tk.Frame(pag, bg=PAGINA)
        zona.pack(fill="x")
        self.canvas = tk.Canvas(zona, height=125, bg=PAGINA, highlightthickness=1,
                                highlightbackground=LINEA)
        self.canvas.pack(fill="x")
        sbx = tk.Scrollbar(zona, orient="horizontal", command=self.canvas.xview)
        sbx.pack(fill="x")
        self.canvas.config(xscrollcommand=sbx.set)

    # ----- utilidades de interfaz -----
    def aviso(self, texto):
        self.estado.config(text=texto)

    def error(self, texto):
        self.aviso("")
        messagebox.showwarning("Ojo", texto, parent=self.root)

    def preguntar(self, titulo, mensaje, inicial=""):
        return simpledialog.askstring(titulo, mensaje, initialvalue=inicial,
                                      parent=self.root)

    def postre_abierto(self):
        """Regresa el postre seleccionado o None (avisando el motivo)."""
        if not POSTRES:
            self.error("El libro está vacío. Primero da de alta un postre.")
            return None
        if self.pos is None or not (0 <= self.pos < len(POSTRES)):
            self.error("Elige un postre del índice.")
            return None
        return POSTRES[self.pos]

    def refrescar_indice(self, pos=None):
        self.lista_postres.delete(0, "end")
        for p in POSTRES:
            n = len(p.ingredientes())
            self.lista_postres.insert("end", f" {p.nombre.title()}   ({n})")
        if POSTRES:
            if pos is None:
                pos = self.pos if self.pos is not None else 0
            pos = max(0, min(pos, len(POSTRES) - 1))
            self.lista_postres.selection_set(pos)
            self.lista_postres.see(pos)
            self.pos = pos
        else:
            self.pos = None
        self.mostrar_receta()

    def al_elegir_postre(self, _evento=None):
        sel = self.lista_postres.curselection()
        if sel:
            self.pos = sel[0]
            self.mostrar_receta()

    def mostrar_receta(self):
        self.lista_ing.delete(0, "end")
        self.canvas.delete("all")
        if self.pos is None:
            self.titulo.config(text="Libro vacío")
            self.subtitulo.config(text="Da de alta tu primer postre con «Nuevo postre».")
            return
        postre = POSTRES[self.pos]
        self.titulo.config(text=postre.nombre.title())
        ings = postre.ingredientes()
        if ings:
            self.subtitulo.config(text=f"Ingredientes ({len(ings)}):")
            for ing in ings:
                self.lista_ing.insert("end", "  •  " + ing)
        else:
            self.subtitulo.config(text="Este postre no tiene ingredientes (lista NIL).")
        self.dibujar_lista(postre)

    def dibujar_lista(self, postre):
        """Dibuja la lista ligada como en el diagrama de la actividad."""
        c = self.canvas
        c.delete("all")
        x, y, h = 12, 18, 44
        ancho, ptr, sep = 110, 24, 42
        fuente = (SERIF, 10, "bold")

        c.create_rectangle(x, y, x + 120, y + h, fill=ACENTO, outline=TINTA, width=2)
        c.create_text(x + 60, y + h / 2, text=recortar(postre.nombre.title(), 14),
                      font=fuente, fill=CREMA)
        origen = x + 120
        medio_y = y + h / 2
        ings = postre.ingredientes()

        if not ings:
            c.create_line(origen, medio_y, origen + sep, medio_y, arrow="last",
                          width=2, fill=TINTA)
            c.create_text(origen + sep + 18, medio_y, text="NIL", font=fuente, fill=TINTA)
        else:
            for ing in ings:
                nx = origen + sep
                c.create_line(origen, medio_y, nx, medio_y, arrow="last",
                              width=2, fill=TINTA)
                c.create_rectangle(nx, y, nx + ancho, y + h, fill=NODO,
                                   outline=TINTA, width=2)
                c.create_line(nx + ancho - ptr, y, nx + ancho - ptr, y + h,
                              width=2, fill=TINTA)
                c.create_text(nx + (ancho - ptr) / 2, medio_y,
                              text=recortar(ing, 10), font=(SERIF, 10), fill=TINTA)
                origen = nx + ancho - ptr / 2
                c.create_oval(origen - 3, medio_y - 3, origen + 3, medio_y + 3,
                              fill=TINTA, outline=TINTA)
            c.create_line(origen, y + h, origen, y + h + 24, arrow="last",
                          width=2, fill=TINTA)
            c.create_text(origen, y + h + 38, text="NIL", font=fuente, fill=TINTA)

        caja = c.bbox("all")
        c.config(scrollregion=(0, 0, caja[2] + 20, caja[3] + 10))

    # ----- operaciones sobre postres (d, e + extras) -----
    def alta_postre(self):
        respuesta = self.preguntar("Nuevo postre", "Nombre del postre:")
        if respuesta is None:
            return  # cancelo
        nombre = normalizar(respuesta)
        if nombre == "":
            self.error("El nombre del postre no puede estar vacío.")
            return
        encontrado, pos = buscar_postre(nombre)
        if encontrado:
            self.error(f"El postre «{nombre.title()}» ya existe.")
            self.refrescar_indice(pos)
            return
        texto = self.preguntar("Ingredientes",
                               "Ingredientes separados por coma:\n(ej. harina, huevo, azúcar)")
        ings = separar_ingredientes(texto)
        if not ings:
            self.error("Un postre debe tener al menos un ingrediente. No se dio de alta.")
            return
        nuevo = Postre(nombre)
        for ing in ings:
            nuevo.insertar(ing)
        POSTRES.insert(pos, nuevo)
        self.refrescar_indice(pos)
        self.aviso(f"Se agregó «{nombre.title()}» con {len(ings)} ingrediente(s).")

    def baja_postre(self):
        postre = self.postre_abierto()
        if postre is None:
            return
        if messagebox.askyesno("Eliminar postre",
                               f"¿Borrar «{postre.nombre.title()}» con todos sus ingredientes?",
                               parent=self.root):
            POSTRES.pop(self.pos)
            postre.liberar()
            self.refrescar_indice(self.pos)
            self.aviso(f"Se eliminó «{postre.nombre.title()}».")

    def renombrar_postre(self):
        postre = self.postre_abierto()
        if postre is None:
            return
        nuevo = normalizar(self.preguntar("Cambiar nombre", "Nuevo nombre:",
                                          postre.nombre.title()))
        if nuevo == "" or nuevo == postre.nombre:
            return
        if buscar_postre(nuevo)[0]:
            self.error(f"Ya existe un postre llamado «{nuevo.title()}».")
            return
        POSTRES.pop(self.pos)
        viejo = postre.nombre
        postre.nombre = nuevo
        _, pos = buscar_postre(nuevo)
        POSTRES.insert(pos, postre)  # conserva el orden
        self.refrescar_indice(pos)
        self.aviso(f"«{viejo.title()}» ahora se llama «{nuevo.title()}».")

    # ----- operaciones sobre ingredientes (a, b, c + modificar) -----
    def agregar_ingredientes(self):
        postre = self.postre_abierto()
        if postre is None:
            return
        texto = self.preguntar("Agregar ingredientes",
                               "Ingredientes separados por coma:")
        nuevos = separar_ingredientes(texto)
        if not nuevos:
            if texto is not None:
                self.error("No escribiste ningún ingrediente válido.")
            return
        repetidos = [i for i in nuevos if not postre.insertar(i)]
        self.refrescar_indice(self.pos)
        if repetidos:
            self.error("Ya estaban en la receta y no se repitieron:\n• " +
                       "\n• ".join(repetidos))
        else:
            self.aviso(f"Se agregaron {len(nuevos)} ingrediente(s).")

    def ingrediente_elegido(self, postre):
        if postre.esta_vacia():
            self.error(f"«{postre.nombre.title()}» no tiene ingredientes.")
            return None
        sel = self.lista_ing.curselection()
        if not sel:
            self.error("Elige un ingrediente de la lista.")
            return None
        return postre.ingredientes()[sel[0]]

    def eliminar_ingrediente(self):
        postre = self.postre_abierto()
        if postre is None:
            return
        ing = self.ingrediente_elegido(postre)
        if ing is None:
            return
        postre.eliminar(ing)
        self.refrescar_indice(self.pos)
        if postre.esta_vacia():
            self.aviso(f"Se quitó «{ing}». La lista quedó vacía (NIL).")
        else:
            self.aviso(f"Se quitó «{ing}».")

    def modificar_ingrediente(self):
        postre = self.postre_abierto()
        if postre is None:
            return
        viejo = self.ingrediente_elegido(postre)
        if viejo is None:
            return
        nuevo = normalizar(self.preguntar("Modificar ingrediente",
                                          f"Cambiar «{viejo}» por:", viejo))
        if nuevo == "" or nuevo == viejo:
            return
        estado = postre.modificar(viejo, nuevo)
        if estado == "duplicado":
            self.error(f"«{nuevo}» ya está en la receta.")
        elif estado == "no_existe":
            self.error(f"«{viejo}» ya no existe.")
        else:
            self.refrescar_indice(self.pos)
            self.aviso(f"«{viejo}» ahora es «{nuevo}».")

    def reemplazar_receta(self):
        postre = self.postre_abierto()
        if postre is None:
            return
        texto = self.preguntar("Reemplazar receta",
                               "Nueva lista de ingredientes separados por coma:",
                               ", ".join(postre.ingredientes()))
        if texto is None:
            return
        nuevos = separar_ingredientes(texto)
        if not nuevos:
            self.error("La receta no puede quedar vacía. No se modificó nada.")
            return
        postre.liberar()
        for ing in nuevos:
            postre.insertar(ing)
        self.refrescar_indice(self.pos)
        self.aviso("Receta reemplazada.")

    # ----- ejercicio 2 -----
    def duplicar_postre_prueba(self):
        """Mete una copia del postre abierto para poder probar eliminar_repetidos."""
        postre = self.postre_abierto()
        if postre is None:
            return
        texto = self.preguntar(
            "Duplicar postre (prueba)",
            "Ingredientes de la copia, separados por coma.\n"
            "Puedes cambiarlos para ver qué pasa con ellos al eliminar repetidos:",
            ", ".join(postre.ingredientes()))
        if texto is None:
            return
        ings = separar_ingredientes(texto)
        if not ings:
            self.error("La copia debe tener al menos un ingrediente.")
            return
        copia = Postre(postre.nombre)
        for ing in ings:
            copia.insertar(ing)
        POSTRES.insert(self.pos + 1, copia)  # junto al original: el arreglo sigue ordenado
        self.refrescar_indice(self.pos + 1)
        self.aviso(f"Se agregó una copia de «{postre.nombre.title()}» (repetido de prueba).")

    def eliminar_repetidos_ui(self):
        if not POSTRES:
            self.error("El libro está vacío, no hay nada que revisar.")
            return
        nombres = [p.nombre for p in POSTRES]
        if len(set(nombres)) == len(nombres):
            messagebox.showinfo(
                "Sin repetidos",
                "No hay postres repetidos en el arreglo, así que no se eliminó nada.\n"
                "Usa «Duplicar postre (prueba)» para crear repetidos.",
                parent=self.root)
            return
        fusionar = messagebox.askyesnocancel(
            "Eliminar repetidos",
            "Se encontraron postres repetidos.\n\n"
            "SÍ  = conservar también los ingredientes de las copias (fusionar)\n"
            "NO  = eliminar las copias completas, con sus listas\n"
            "Cancelar = no hacer nada",
            parent=self.root)
        if fusionar is None:
            return
        try:
            informe, antes, despues = eliminar_repetidos(fusionar)
        except Exception as e:  # por si algo fallara, se reporta el error
            messagebox.showerror("Error", f"Ocurrió un error: {e}", parent=self.root)
            return
        self.refrescar_indice(self.pos)
        self.aviso(f"Repetidos eliminados: {antes - despues}.")
        self.mostrar_informe(texto_informe(informe, antes, despues, fusionar))

    def mostrar_informe(self, texto):
        ventana = tk.Toplevel(self.root)
        ventana.title("Informe - Eliminar repetidos")
        ventana.geometry("700x520")
        ventana.configure(bg=PAGINA)
        caja = tk.Text(ventana, wrap="word", font=(SERIF, 12), bg=PAGINA, fg=TINTA,
                       bd=0, padx=18, pady=14, highlightthickness=0)
        caja.pack(fill="both", expand=True)
        caja.insert("1.0", texto)
        caja.config(state="disabled")
        self.boton(ventana, "Cerrar", ventana.destroy).pack(pady=8)


def cargar_datos_iniciales():
    datos = {
        "pastel de chocolate": ["harina", "cacao", "huevo", "azúcar", "mantequilla"],
        "flan": ["leche", "huevo", "azúcar", "vainilla"],
        "gelatina": ["grenetina", "agua", "azúcar"],
    }
    for nombre, ings in datos.items():
        p = Postre(nombre)
        for ing in ings:
            p.insertar(ing)
        POSTRES.insert(buscar_postre(nombre)[1], p)


def main():
    cargar_datos_iniciales()
    root = tk.Tk()
    LibroRecetas(root)
    root.mainloop()


if __name__ == "__main__":
    main()
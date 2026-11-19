"""Interfaz gráfica del Generador de Sílabas (CustomTkinter, POO)."""

import tkinter as tk
from tkinter import messagebox
from types import SimpleNamespace

import customtkinter as ctk

from silabas import __copyright__, __date__, __license__, __version__, config, logic, recursos


class SilabasApp(ctk.CTk):
    """Ventana principal. Todo el estado vive en atributos de instancia."""

    def __init__(self):
        super().__init__()

        self.familia_fuente = recursos.cargar_fuente(self)

        # --- Estado de la aplicación (antes variables globales) ---
        self.ultima_palabra = None
        self.font_size = config.FONT_SIZE_INICIAL

        # --- Ventana ---
        self.title(f"Generador de Sílabas v{__version__}")
        self.geometry(f"{self.winfo_screenwidth()}x{config.VENTANA_ALTO}")

        # Grid principal: fila 0 = controles (auto), fila 1 = canvas (expandible)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        # --- Variables de control ---
        self.modo_coloreado = ctk.BooleanVar(master=self, value=True)
        self.modo_balanceado = ctk.BooleanVar(master=self, value=True)
        self.vocal_sola_var = ctk.BooleanVar(master=self, value=False)
        self.consonantes_vars = {
            cons: ctk.BooleanVar(master=self, value=False) for cons in config.CONSONANTES
        }

        # --- Frame superior (inputs) ---
        self.frame_inputs = ctk.CTkFrame(self, corner_radius=10)
        self.frame_inputs.grid(row=0, column=0, sticky="ew", padx=15, pady=(15, 5))
        self.frame_inputs.grid_columnconfigure(0, weight=1)  # Izquierda
        self.frame_inputs.grid_columnconfigure(1, weight=1)  # Centro
        self.frame_inputs.grid_columnconfigure(2, weight=2)  # Derecha (consonantes)
        self.frame_inputs.grid_rowconfigure(0, weight=0)
        self.frame_inputs.grid_rowconfigure(1, weight=0)

        # Bloque izquierda: cantidad de sílabas
        self.frame_izquierda = ctk.CTkFrame(self.frame_inputs, fg_color="transparent")
        self.frame_izquierda.grid(row=0, column=0, padx=20, pady=15, sticky="n")

        self.label_silabas = ctk.CTkLabel(
            self.frame_izquierda, text="Cantidad de sílabas:", font=ctk.CTkFont("Arial", 12)
        )
        self.label_silabas.pack(pady=(5, 2))

        self.entry = ctk.CTkEntry(
            self.frame_izquierda, width=80, justify="center", font=ctk.CTkFont("Arial", 14)
        )
        self.entry.pack(pady=(0, 5))
        self.entry.insert(0, str(config.SILABAS_INICIAL))

        # Bloque central: opciones adicionales
        self.frame_opciones = ctk.CTkFrame(self.frame_inputs, fg_color="transparent")
        self.frame_opciones.grid(row=0, column=1, padx=10, pady=15, sticky="n")

        self.checkbox_coloreado = ctk.CTkCheckBox(
            self.frame_opciones, text="Modo coloreado", variable=self.modo_coloreado,
            font=ctk.CTkFont("Arial", 11),
        )
        self.checkbox_coloreado.pack(anchor="w", pady=4)

        self.checkbox_balanceado = ctk.CTkCheckBox(
            self.frame_opciones, text="Modo balanceado", variable=self.modo_balanceado,
            font=ctk.CTkFont("Arial", 11),
        )
        self.checkbox_balanceado.pack(anchor="w", pady=4)

        # Bloque derecha: vocal sola + consonantes
        self.frame_consonantes = ctk.CTkFrame(self.frame_inputs, fg_color="transparent")
        self.frame_consonantes.grid(row=0, column=2, padx=20, pady=15, sticky="nsew")

        self.checkbox_vocal = ctk.CTkCheckBox(
            self.frame_consonantes, text="a", variable=self.vocal_sola_var,
            font=ctk.CTkFont("Arial", 11), width=30,
        )
        self.checkbox_vocal.grid(row=0, column=0, padx=4, pady=3, sticky="w")

        self.checkboxes_consonantes = {}
        for i, cons in enumerate(config.CONSONANTES):
            idx = i + 1  # La posición 0 la ocupa la vocal sola
            fila = idx // config.MAX_POR_FILA
            col = idx % config.MAX_POR_FILA
            checkbox = ctk.CTkCheckBox(
                self.frame_consonantes, text=cons, variable=self.consonantes_vars[cons],
                font=ctk.CTkFont("Arial", 11), width=30,
            )
            checkbox.grid(row=fila, column=col, padx=4, pady=3, sticky="w")
            self.checkboxes_consonantes[cons] = checkbox

        # Botón Generar
        self.btn_generar = ctk.CTkButton(
            self.frame_inputs, text="Generar", command=self.generar_palabra,
            font=ctk.CTkFont("Arial", 13, "bold"), height=40, corner_radius=8,
        )
        self.btn_generar.grid(row=1, column=0, columnspan=3, pady=(0, 15), sticky="ew", padx=20)

        # --- Canvas de resultado (tk.Canvas nativo: CustomTkinter no tiene equivalente) ---
        self.canvas = tk.Canvas(self, bg=config.CANVAS_BG_OSCURO, bd=0, highlightthickness=0)
        self.canvas.grid(row=1, column=0, sticky="nsew", padx=15, pady=(5, 10))

        # --- Pie de ventana ---
        self.footer = ctk.CTkLabel(
            self, text=f"{__copyright__} — v{__version__}",
            font=ctk.CTkFont("Arial", 9), text_color="gray",
        )
        self.footer.grid(row=2, column=0, pady=(0, 5))

        self.boton_info = ctk.CTkButton(
            self, text="Acerca de", command=self.mostrar_acerca_de,
            font=ctk.CTkFont("Arial", 10), height=30, corner_radius=6,
            fg_color="transparent", border_width=1, text_color=("gray10", "gray90"),
        )
        self.boton_info.grid(row=3, column=0, pady=(0, 15))

        # --- Eventos ---
        self.entry.focus()
        self.bind("<Return>", lambda event: self.generar_palabra())
        self.bind("<MouseWheel>", self.zoom_text)
        # Linux (X11): la rueda llega como Button-4 / Button-5
        self.bind("<Button-4>", lambda event: self.zoom_text(SimpleNamespace(delta=120)))
        self.bind("<Button-5>", lambda event: self.zoom_text(SimpleNamespace(delta=-120)))
        self.bind("<Configure>", self.ajustar_canvas)

        recursos.aplicar_icono(self)

        # Ajuste inicial
        self.update_idletasks()
        self.ajustar_canvas()

    # ------------------------------------------------------------------
    # Generación
    # ------------------------------------------------------------------
    def generar_palabra(self):
        """Recoge los valores de la UI, pide la palabra a logic y la dibuja."""
        # Validar cantidad de sílabas; si es inválida, restaurar el valor por defecto
        try:
            n = int(self.entry.get().strip())
            if n <= 0:
                raise ValueError
        except ValueError:
            n = config.SILABAS_INICIAL
            self.entry.delete(0, tk.END)
            self.entry.insert(0, str(n))

        seleccionadas = [c for c, var in self.consonantes_vars.items() if var.get()]

        # Si no hay consonantes ni vocal sola, activar la consonante por defecto
        if not seleccionadas and not self.vocal_sola_var.get():
            self.consonantes_vars[config.CONSONANTE_POR_DEFECTO].set(True)
            seleccionadas = [config.CONSONANTE_POR_DEFECTO]

        opciones = list(seleccionadas)
        if self.vocal_sola_var.get():
            opciones.extend(logic.VOCALES)

        palabra = logic.generar_palabra(
            n, opciones, self.modo_balanceado.get(), self.ultima_palabra
        )
        self.ultima_palabra = palabra
        self.mostrar_palabra(palabra)

    # ------------------------------------------------------------------
    # Dibujo en el Canvas
    # ------------------------------------------------------------------
    def _color_para(self, vocal):
        """Color de una letra según su vocal. Si el modo coloreado está apagado, siempre es blanco."""
        if vocal and self.modo_coloreado.get():
            return config.colores_vocales.get(vocal.lower(), config.COLOR_TEXTO_NEUTRO)
        return "white"

    def mostrar_palabra(self, texto):
        """Dibuja la palabra centrada en el Canvas, coloreada según la vocal."""
        self.canvas.delete("all")

        # Fondo del canvas adaptado al tema
        canvas_bg = (
            config.CANVAS_BG_OSCURO if ctk.get_appearance_mode() == "Dark"
            else config.CANVAS_BG_CLARO
        )
        self.canvas.create_rectangle(
            -10, -10, self.canvas.winfo_width() + 10, self.canvas.winfo_height() + 10,
            fill=canvas_bg, outline="",
        )

        if not texto:
            return

        x = self.canvas.winfo_width() // 2
        y = self.canvas.winfo_height() // 2
        fuente = (self.familia_fuente, self.font_size, "bold")

        # Medir el ancho de cada letra con su bbox
        medidas = []
        total_width = 0
        for letra, vocal in logic.segmentar(texto):
            color = self._color_para(vocal)
            item = self.canvas.create_text(0, 0, text=letra, font=fuente)
            bbox = self.canvas.bbox(item)
            w = bbox[2] - bbox[0] if bbox else 0
            medidas.append((letra, w, color))
            self.canvas.delete(item)
            total_width += w

        # Dibujar centrado
        pos_x = x - total_width // 2
        for letra, w, color in medidas:
            self.canvas.create_text(pos_x + w / 2, y, text=letra, fill=color, font=fuente)
            pos_x += w

    # ------------------------------------------------------------------
    # Zoom y redimensionado
    # ------------------------------------------------------------------
    def zoom_text(self, event):
        """Aumenta o reduce el tamaño del texto con la rueda del ratón."""
        delta = getattr(event, "delta", 0)
        paso = config.FONT_SIZE_PASO if delta > 0 else -config.FONT_SIZE_PASO
        self.font_size = max(config.FONT_SIZE_MIN, min(config.FONT_SIZE_MAX, self.font_size + paso))
        self.mostrar_palabra(self.ultima_palabra)

    def ajustar_canvas(self, event=None):
        """Redibuja la palabra al cambiar el tamaño de la ventana."""
        self.mostrar_palabra(self.ultima_palabra)

    # ------------------------------------------------------------------
    # Auxiliares
    # ------------------------------------------------------------------
    def mostrar_acerca_de(self):
        about_text = (
            f"{__copyright__}\n\n"
            f"Versión: {__version__}\n"
            f"Fecha: {__date__}\n\n"
            "Descripción:\n"
            "Generador de sílabas aleatorias (CV o CCV).\n"
            "Permite ajustar el tamaño de fuente con la rueda del ratón.\n"
            "Evita repetir la última palabra generada y cuenta con modo coloreado opcional.\n\n"
            f"Software libre, publicado bajo licencia {__license__}."
        )
        messagebox.showinfo("Acerca de", about_text)

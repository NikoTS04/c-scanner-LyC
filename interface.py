import tkinter as tk
from tkinter import filedialog, scrolledtext, ttk
from scanner import quitar_comentarios, analizar

class ScannerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("C Lexical Scanner")
        self.root.geometry("1000x700")
        self.root.configure(bg='#2b2b2b')
        
        # Variables
        self.archivo_actual = None
        self.tokens = []
        
        # Configurar estilo
        self.configurar_estilos()
        
        # Crear interfaz
        self.crear_widgets()
        
    def configurar_estilos(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Estilo para botones
        style.configure('Modern.TButton',
                       background='#4a9eff',
                       foreground='white',
                       borderwidth=0,
                       focuscolor='none',
                       font=('Arial', 10, 'bold'))
        
        style.map('Modern.TButton',
                 background=[('active', '#3a8eef')])
        
    def crear_widgets(self):
        # Frame superior - Controles
        frame_superior = tk.Frame(self.root, bg='#2b2b2b', pady=15)
        frame_superior.pack(fill='x', padx=20)
        
        # Título
        titulo = tk.Label(frame_superior, 
                         text="C Lexical Scanner",
                         font=('Arial', 20, 'bold'),
                         fg='#4a9eff',
                         bg='#2b2b2b')
        titulo.pack(side='left')
        
        # Botones
        frame_botones = tk.Frame(frame_superior, bg='#2b2b2b')
        frame_botones.pack(side='right')
        
        self.btn_cargar = ttk.Button(frame_botones,
                                     text="📁 Cargar Archivo",
                                     command=self.cargar_archivo,
                                     style='Modern.TButton',
                                     width=15)
        self.btn_cargar.pack(side='left', padx=5)
        
        self.btn_analizar = ttk.Button(frame_botones,
                                       text="🔍 Analizar",
                                       command=self.analizar_codigo,
                                       style='Modern.TButton',
                                       width=15,
                                       state='disabled')
        self.btn_analizar.pack(side='left', padx=5)
        
        self.btn_limpiar = ttk.Button(frame_botones,
                                      text="🗑️ Limpiar",
                                      command=self.limpiar_resultados,
                                      style='Modern.TButton',
                                      width=15)
        self.btn_limpiar.pack(side='left', padx=5)
        
        # Label de archivo actual
        self.label_archivo = tk.Label(self.root,
                                      text="Ningún archivo cargado",
                                      font=('Arial', 9),
                                      fg='#888888',
                                      bg='#2b2b2b')
        self.label_archivo.pack(pady=(0, 10))
        
        # Separador
        separator = tk.Frame(self.root, height=2, bg='#4a9eff')
        separator.pack(fill='x', padx=20)
        
        # Frame principal con dos columnas
        frame_principal = tk.Frame(self.root, bg='#2b2b2b')
        frame_principal.pack(fill='both', expand=True, padx=20, pady=15)
        
        # Columna izquierda - Estadísticas
        frame_izquierda = tk.Frame(frame_principal, bg='#1e1e1e', relief='flat')
        frame_izquierda.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        label_stats = tk.Label(frame_izquierda,
                              text="Estadísticas",
                              font=('Arial', 12, 'bold'),
                              fg='#4a9eff',
                              bg='#1e1e1e',
                              pady=10)
        label_stats.pack()
        
        self.text_estadisticas = scrolledtext.ScrolledText(
            frame_izquierda,
            wrap=tk.WORD,
            width=40,
            height=30,
            font=('Courier New', 10),
            bg='#1e1e1e',
            fg='#e0e0e0',
            insertbackground='white',
            selectbackground='#4a9eff',
            relief='flat'
        )
        self.text_estadisticas.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # Columna derecha - Tokens
        frame_derecha = tk.Frame(frame_principal, bg='#1e1e1e', relief='flat')
        frame_derecha.pack(side='right', fill='both', expand=True)
        
        label_tokens = tk.Label(frame_derecha,
                               text="Tokens Encontrados",
                               font=('Arial', 12, 'bold'),
                               fg='#4a9eff',
                               bg='#1e1e1e',
                               pady=10)
        label_tokens.pack()
        
        self.text_tokens = scrolledtext.ScrolledText(
            frame_derecha,
            wrap=tk.WORD,
            width=50,
            height=30,
            font=('Courier New', 10),
            bg='#1e1e1e',
            fg='#e0e0e0',
            insertbackground='white',
            selectbackground='#4a9eff',
            relief='flat'
        )
        self.text_tokens.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
    def cargar_archivo(self):
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo C",
            filetypes=[("Archivos C", "*.c"), ("Todos los archivos", "*.*")]
        )
        
        if archivo:
            self.archivo_actual = archivo
            nombre_corto = archivo.split('/')[-1]
            self.label_archivo.config(
                text=f"📄 Archivo: {nombre_corto}",
                fg='#4a9eff'
            )
            self.btn_analizar.config(state='normal')
            
    def analizar_codigo(self):
        if not self.archivo_actual:
            return
            
        try:
            with open(self.archivo_actual, 'r', encoding='utf-8') as archivo:
                contenido = archivo.read()
            
            # Limpiar resultados anteriores
            self.text_estadisticas.delete(1.0, tk.END)
            self.text_tokens.delete(1.0, tk.END)
            
            # Procesar código
            codigo_limpio = quitar_comentarios(contenido)
            self.tokens = analizar(codigo_limpio)
            
            # Mostrar estadísticas
            self.mostrar_estadisticas()
            
            # Mostrar tokens
            self.mostrar_tokens()
            
        except FileNotFoundError:
            self.mostrar_error("Archivo no encontrado")
        except Exception as e:
            self.mostrar_error(f"Error al procesar: {str(e)}")
            
    def mostrar_estadisticas(self):
        contadores = {
            'VARIABLE': 0,
            'PALABRA_RESERVADA': 0,
            'NUMERO_ENTERO': 0,
            'NUMERO_REAL': 0,
            'OPERADOR': 0
        }
        
        por_tipo = {
            'VARIABLE': [],
            'PALABRA_RESERVADA': [],
            'NUMERO_ENTERO': [],
            'NUMERO_REAL': [],
            'OPERADOR': []
        }
        
        for token in self.tokens:
            tipo = token['tipo']
            contadores[tipo] += 1
            por_tipo[tipo].append(token)
        
        # Escribir resumen
        self.text_estadisticas.insert(tk.END, "═" * 50 + "\n")
        self.text_estadisticas.insert(tk.END, "  RESUMEN GENERAL\n")
        self.text_estadisticas.insert(tk.END, "═" * 50 + "\n\n")
        
        self.text_estadisticas.insert(tk.END, f"Total de tokens: {len(self.tokens)}\n\n")
        self.text_estadisticas.insert(tk.END, f"  • Palabras reservadas: {contadores['PALABRA_RESERVADA']}\n")
        self.text_estadisticas.insert(tk.END, f"  • Variables:           {contadores['VARIABLE']}\n")
        self.text_estadisticas.insert(tk.END, f"  • Números enteros:     {contadores['NUMERO_ENTERO']}\n")
        self.text_estadisticas.insert(tk.END, f"  • Números reales:      {contadores['NUMERO_REAL']}\n")
        self.text_estadisticas.insert(tk.END, f"  • Operadores:          {contadores['OPERADOR']}\n\n")
        
        # Detalle por tipo
        self.text_estadisticas.insert(tk.END, "─" * 50 + "\n")
        self.text_estadisticas.insert(tk.END, "  DETALLE POR TIPO\n")
        self.text_estadisticas.insert(tk.END, "─" * 50 + "\n\n")
        
        nombres = {
            'PALABRA_RESERVADA': '🔵 PALABRAS RESERVADAS',
            'VARIABLE': '🟢 VARIABLES',
            'NUMERO_ENTERO': '🟡 NÚMEROS ENTEROS',
            'NUMERO_REAL': '🟠 NÚMEROS REALES',
            'OPERADOR': '🔴 OPERADORES'
        }
        
        for tipo in ['PALABRA_RESERVADA', 'VARIABLE', 'NUMERO_ENTERO', 'NUMERO_REAL', 'OPERADOR']:
            self.text_estadisticas.insert(tk.END, f"{nombres[tipo]}\n")
            if por_tipo[tipo]:
                for t in por_tipo[tipo]:
                    self.text_estadisticas.insert(tk.END, f"  [{t['orden']:3d}] {t['valor']}\n")
            else:
                self.text_estadisticas.insert(tk.END, "  (ninguno)\n")
            self.text_estadisticas.insert(tk.END, "\n")
            
    def mostrar_tokens(self):
        self.text_tokens.insert(tk.END, "═" * 60 + "\n")
        self.text_tokens.insert(tk.END, "  TOKENS EN ORDEN DE APARICIÓN\n")
        self.text_tokens.insert(tk.END, "═" * 60 + "\n\n")
        
        for token in self.tokens:
            tipo_formateado = f"[{token['tipo']}]".ljust(22)
            self.text_tokens.insert(tk.END, f"  {token['orden']:3d}. {tipo_formateado} → {token['valor']}\n")
            
    def mostrar_error(self, mensaje):
        self.text_estadisticas.delete(1.0, tk.END)
        self.text_tokens.delete(1.0, tk.END)
        self.text_estadisticas.insert(tk.END, f"❌ ERROR: {mensaje}\n")
        
    def limpiar_resultados(self):
        self.text_estadisticas.delete(1.0, tk.END)
        self.text_tokens.delete(1.0, tk.END)
        self.archivo_actual = None
        self.tokens = []
        self.label_archivo.config(
            text="Ningún archivo cargado",
            fg='#888888'
        )
        self.btn_analizar.config(state='disabled')


def main():
    root = tk.Tk()
    app = ScannerGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
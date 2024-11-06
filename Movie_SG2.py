import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from ttkbootstrap import Style
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class RecomendadorPeliculas:
    def __init__(self, root):
        self.root = root
        self.root.title("Recomendador de Películas")
        self.root.geometry("1100x700")
        
        # Aplicar estilo ttkbootstrap
        self.style = Style(theme="darkly")
        
        # Configurar estilos personalizados
        self.style.configure('Sidebar.TButton', font=('Helvetica', 14, 'bold'), padding=10)
        self.style.configure('TLabel', font=('Helvetica', 14))
        self.style.configure('TCombobox', font=('Helvetica', 14))
        self.style.configure('Treeview', font=('Helvetica', 13))
        self.style.configure('Treeview.Heading', font=('Helvetica', 14, 'bold'))
        
        # Configurar color de fondo más claro para la columna de calificación del usuario
        self.style.configure('Treeview', background="#2a3038", fieldbackground="#2a3038", foreground="white")
        self.style.map('Treeview', background=[('selected', '#3a4048')])
        
        # Cargar el dataset
        self.df = pd.read_csv('C:/Users/artu_/Documents/tarea/ESCOM/4S/Analisis de datos/Proyecto/tabla_generos.csv')
        self.df['genero'] = self.df['genero'].fillna('')
        self.df['cast'] = self.df['cast'].fillna('')
        self.df['director'] = self.df['director'].fillna('')
        self.df['combined_features'] = self.df['genero'] + ' ' + self.df['cast'] + ' ' + self.df['director']
        self.df = self.df[self.df['combined_features'].str.strip() != '']
        
        # Crear la matriz TF-IDF
        self.tfidf = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = self.tfidf.fit_transform(self.df['combined_features'])
        
        # Estructura para almacenar calificaciones del usuario
        self.user_ratings = {}
        
        # Frame principal
        main_frame = ttk.Frame(root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Barra lateral
        sidebar = ttk.Frame(main_frame, style='secondary.TFrame', width=250)
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))

        # Contenido principal
        self.content = ttk.Frame(main_frame)
        self.content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Botones en la barra lateral
        ttk.Button(sidebar, text="Recomendación Básica", command=lambda: self.show_frame("basic"), style='primary.TButton').pack(pady=10, padx=5, fill=tk.X)
        ttk.Button(sidebar, text="Recomendación Avanzada", command=lambda: self.show_frame("advanced"), style='primary.TButton').pack(pady=10, padx=5, fill=tk.X)

        # Frames para cada tipo de recomendación
        self.basic_frame = ttk.Frame(self.content)
        self.advanced_frame = ttk.Frame(self.content)

        # Configurar frame de recomendación básica
        self.setup_basic_frame()

        # Configurar frame de recomendación avanzada
        self.setup_advanced_frame()

        # Frame para resultados
        self.results_frame = ttk.Frame(self.content)

        # Tabla para mostrar recomendaciones
        self.results_tree = ttk.Treeview(self.results_frame, columns=('Title', 'Rating'), show='headings', style='Treeview')
        self.results_tree.heading('Title', text='Título', anchor="center")
        self.results_tree.heading('Rating', text='Calificación', anchor="center")
        self.results_tree.column('Title', anchor="center", width=400)
        self.results_tree.column('Rating', anchor="center", width=100)
        self.results_tree.pack(fill=tk.BOTH, expand=True)

        # Ajustar la tabla (centrado, negritas y tamaño de fuente)
        style = ttk.Style()
        style.configure("primary.Treeview.Heading", font=('Helvetica', 12, 'bold'), anchor="center")  # Negrita y centrado para cabeceras
        style.configure("primary.Treeview", rowheight=25, font=('Helvetica', 11), anchor="center")  # Centrado en filas

        # Mostrar frame básico por defecto
        self.show_frame("basic")

    def setup_basic_frame(self):
        ttk.Label(self.basic_frame, text="Género:", style='TLabel').pack(pady=5)
        self.genero_combobox_basic = ttk.Combobox(self.basic_frame, values=sorted(list(self.df['genero'].unique())), style='TCombobox', state="readonly")
        self.genero_combobox_basic.pack(pady=5)
        ttk.Button(self.basic_frame, text="Obtener Recomendaciones", command=self.obtener_recomendaciones_basicas, style='Sidebar.TButton').pack(pady=10)
        
    def limpiar_calificaciones(self):
        self.user_ratings.clear()
        self.actualizar_peliculas(None)  # Pasar None porque el evento no es relevante aquí

    def setup_advanced_frame(self):
        ttk.Label(self.advanced_frame, text="Género:", style='TLabel').pack(pady=5)
        self.genero_combobox_advanced = ttk.Combobox(self.advanced_frame, values=sorted(list(self.df['genero'].unique())), style='TCombobox', state="readonly")
        self.genero_combobox_advanced.pack(pady=5)
        self.genero_combobox_advanced.bind("<<ComboboxSelected>>", self.actualizar_peliculas)
        ttk.Button(self.advanced_frame, text="Obtener Recomendaciones Avanzadas", command=self.obtener_recomendaciones_avanzadas, style='Sidebar.TButton').pack(pady=10)
        ttk.Button(self.advanced_frame, text="Limpiar Calificaciones", command=self.limpiar_calificaciones, style='Sidebar.TButton').pack(pady=10)

        # Tabla de películas
        self.tree = ttk.Treeview(self.advanced_frame, columns=('Title', 'Rating', 'User Rating'), show='headings', style='Treeview')
        self.tree.heading('Title', text='Título', anchor="center")
        self.tree.heading('Rating', text='Calificación', anchor="center")
        self.tree.heading('User Rating', text='Tu Calificación', anchor="center")
        self.tree.column('Title', anchor="center", width=300)
        self.tree.column('Rating', anchor="center", width=100)
        self.tree.column('User Rating', anchor="center", width=100)
        self.tree.pack(fill=tk.BOTH, expand=True, pady=10)

        # Scrollbar para la tabla
        scrollbar = ttk.Scrollbar(self.advanced_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Vincular el evento de clic para permitir edición de calificaciones
        self.tree.bind("<ButtonRelease-1>", self.on_tree_click)

        # Crear entry para edición
        self.rating_entry = ttk.Entry(self.advanced_frame, font=('Helvetica', 11), width=5)
        self.rating_entry.place(x=0, y=0, width=0, height=0)  # Inicialmente oculto
        self.rating_entry.bind("<Return>", self.on_rating_change)
        self.rating_entry.bind("<FocusOut>", self.on_rating_change)

        # Detectar cuando el mouse pasa sobre la columna "Tu Calificación"
        self.tree.bind("<Motion>", self.on_mouse_motion)
    
    def on_mouse_motion(self, event):
        region = self.tree.identify("region", event.x, event.y)
        column = self.tree.identify_column(event.x)
    
        # Si estamos en la columna "Tu Calificación", cambiar el cursor
        if region == "cell" and column == "#3":  # Columna "Tu Calificación"
            self.tree.config(cursor="hand2")
        else:
            self.tree.config(cursor="")
            
    def show_frame(self, frame_name):
        self.update_results_table([])  # Pasar una lista vacía para limpiar la tabla
        if frame_name == "basic":
            self.basic_frame.pack(fill=tk.BOTH, expand=True)
            self.advanced_frame.pack_forget()
        elif frame_name == "advanced":
            self.advanced_frame.pack(fill=tk.BOTH, expand=True)
            self.basic_frame.pack_forget()
        self.results_frame.pack(fill=tk.BOTH, expand=True, pady=10)

    def on_rating_change(self, event):
        try:
            new_rating = float(self.rating_entry.get())
            if 1 <= new_rating <= 10:
                item = self.tree.item(self.current_item)
                values = item['values']
                values[2] = round(new_rating, 1)
                self.tree.item(self.current_item, values=values)
                self.user_ratings[values[0]] = new_rating
            else:
                raise ValueError
        except ValueError:
            messagebox.showwarning("Calificación Inválida", "Por favor, ingrese un número entre 1 y 10.")
        finally:
            self.rating_entry.place_forget()
            
    def actualizar_peliculas(self, event):
        genero = self.genero_combobox_advanced.get()
        peliculas_genero = self.df[self.df['genero'] == genero]
        
        # Limpiar tabla actual
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        # Llenar tabla con nuevas películas
        for _, pelicula in peliculas_genero.iterrows():
            user_rating = self.user_ratings.get(pelicula['title'], '')
            self.tree.insert('', 'end', values=(pelicula['title'], pelicula['vote_average'], user_rating))
            
        # Aplicar color de fondo más claro a la columna de calificación del usuario
        for item in self.tree.get_children():
            self.tree.tag_configure(item, background='#3a4048')
            self.tree.item(item, tags=(item,))

    def on_tree_click(self, event):
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell":
            column = self.tree.identify_column(event.x)
            if column == "#3":  # La columna "Tu Calificación"
                row_id = self.tree.identify_row(event.y)
                movie_title = self.tree.item(row_id)['values'][0]
                user_rating = simpledialog.askfloat("Calificar Película", f"Ingrese una calificación para {movie_title} (1-10):", minvalue=1, maxvalue=10)
                if user_rating is not None:
                    self.tree.set(row_id, column="#3", value=round(user_rating, 1))
                    self.user_ratings[movie_title] = user_rating
                    
    def obtener_recomendaciones_basicas(self):
        genero = self.genero_combobox_basic.get()
        if not genero:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un género.")
            return
        peliculas_genero = self.df[self.df['genero'] == genero].sort_values('vote_average', ascending=False)
        top = peliculas_genero.head(50)
        recomendaciones = [(pelicula['title'], pelicula['vote_average']) for _, pelicula in top.iterrows()]
        self.update_results_table(recomendaciones)

    def obtener_recomendaciones_avanzadas(self):
        if len(self.user_ratings) < 3:
            messagebox.showwarning("Advertencia", "Por favor, califica al menos 3 películas antes de obtener recomendaciones.")
            return

        # Crear un vector de características del usuario basado en sus calificaciones
        user_profile = np.zeros(self.tfidf_matrix.shape[1])
        for movie, rating in self.user_ratings.items():
            movie_index = self.df[self.df['title'] == movie].index[0]
            user_profile += self.tfidf_matrix[movie_index].toarray()[0] * float(rating)

        # Calcular similitud coseno entre el perfil del usuario y todas las películas
        cosine_similarities = cosine_similarity(user_profile.reshape(1, -1), self.tfidf_matrix)[0]

         # Crear un diccionario para almacenar la mejor similitud para cada película
        best_similarities = {}

       # Iterar sobre todas las películas y sus similitudes
        for idx, similarity in enumerate(cosine_similarities):
            title = self.df.iloc[idx]['title']
            if title not in self.user_ratings:  # Excluir películas ya calificadas
                if title not in best_similarities or similarity > best_similarities[title][1]:
                    best_similarities[title] = (self.df.iloc[idx]['vote_average'], similarity)
        
        # Convertir el diccionario a una lista de tuplas y ordenar por similitud
        recommendations = [(title, rating, similarity) for title, (rating, similarity) in best_similarities.items()]
        recommendations.sort(key=lambda x: x[2], reverse=True)
        # Tomar las top 50 recomendaciones
        top_recommendations = recommendations[:50]
        self.update_results_table(recommendations)

    def update_results_table(self, recommendations):
        # Limpiar tabla actual
        for i in self.results_tree.get_children():
            self.results_tree.delete(i)

        # Insertar nuevas recomendaciones en la tabla
        for recommendation in recommendations:
            self.results_tree.insert('', 'end', values=(recommendation[0], round(recommendation[1], 1)))

# Inicializar la ventana principal
root = tk.Tk()
app = RecomendadorPeliculas(root)
root.mainloop()

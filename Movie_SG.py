import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class RecomendadorPeliculas:
    def __init__(self, root):
        self.root = root
        self.root.title("Recomendador de Películas")
        self.root.geometry("1000x700")
        
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
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Pestañas
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Pestaña de recomendación básica
        self.basic_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.basic_tab, text="Recomendación Básica")

        # Selección de género para recomendación básica
        ttk.Label(self.basic_tab, text="Género:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.genero_combobox_basic = ttk.Combobox(self.basic_tab, values=sorted(list(self.df['genero'].unique())))
        self.genero_combobox_basic.grid(row=0, column=1, sticky=tk.W, pady=5)

        # Botón para obtener recomendaciones básicas
        ttk.Button(self.basic_tab, text="Obtener Recomendaciones Básicas", command=self.obtener_recomendaciones_basicas).grid(row=1, column=0, columnspan=2, pady=10)

        # Pestaña de recomendación avanzada
        self.advanced_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.advanced_tab, text="Recomendación Avanzada")

        # Selección de género para recomendación avanzada
        ttk.Label(self.advanced_tab, text="Género:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.genero_combobox_advanced = ttk.Combobox(self.advanced_tab, values=sorted(list(self.df['genero'].unique())))
        self.genero_combobox_advanced.grid(row=0, column=1, sticky=tk.W, pady=5)
        self.genero_combobox_advanced.bind("<<ComboboxSelected>>", self.actualizar_peliculas)

        # Tabla de películas
        self.tree = ttk.Treeview(self.advanced_tab, columns=('Title', 'Rating', 'User Rating'), show='headings')
        self.tree.heading('Title', text='Título')
        self.tree.heading('Rating', text='Calificación')
        self.tree.heading('User Rating', text='Tu Calificación')
        self.tree.grid(row=1, column=0, columnspan=2, pady=10)

        # Frame para calificación
        rating_frame = ttk.Frame(self.advanced_tab)
        rating_frame.grid(row=2, column=0, columnspan=2, pady=10)

        ttk.Label(rating_frame, text="Calificar película:").grid(row=0, column=0, sticky=tk.W)
        self.rating_spinbox = ttk.Spinbox(rating_frame, from_=1, to=10, width=5)
        self.rating_spinbox.grid(row=0, column=1, padx=5)
        ttk.Button(rating_frame, text="Calificar", command=self.calificar_pelicula).grid(row=0, column=2)

        # Etiqueta para mostrar el número de películas calificadas
        self.rated_movies_label = ttk.Label(self.advanced_tab, text="Películas calificadas: 0/3")
        self.rated_movies_label.grid(row=3, column=0, columnspan=2, pady=5)

        # Botón para obtener recomendaciones avanzadas
        self.recommend_button = ttk.Button(self.advanced_tab, text="Obtener Recomendaciones Avanzadas", command=self.obtener_recomendaciones_avanzadas, state=tk.DISABLED)
        self.recommend_button.grid(row=4, column=0, columnspan=2, pady=10)

        # Lista para mostrar las recomendaciones
        self.recomendaciones_listbox = tk.Listbox(main_frame, width=70, height=10)
        self.recomendaciones_listbox.grid(row=1, column=0, pady=5)

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

    def calificar_pelicula(self):
        selected_items = self.tree.selection()
        if not selected_items:
            messagebox.showwarning("Advertencia", "Por favor, selecciona una película para calificar.")
            return
        
        selected_item = selected_items[0]
        movie_title = self.tree.item(selected_item)['values'][0]
        user_rating = self.rating_spinbox.get()
        
        # Actualizar calificación del usuario
        self.user_ratings[movie_title] = user_rating
        
        # Actualizar tabla
        self.tree.item(selected_item, values=(movie_title, self.tree.item(selected_item)['values'][1], user_rating))

        # Actualizar etiqueta de películas calificadas
        num_rated = len(self.user_ratings)
        self.rated_movies_label.config(text=f"Películas calificadas: {num_rated}/3")

        # Habilitar el botón de recomendaciones si se han calificado al menos 3 películas
        if num_rated >= 3:
            self.recommend_button.config(state=tk.NORMAL)

    def obtener_recomendaciones_basicas(self):
        genero = self.genero_combobox_basic.get()
        peliculas_genero = self.df[self.df['genero'] == genero].sort_values('vote_average', ascending=False)
        top_10 = peliculas_genero.head(10)
        self.recomendaciones_listbox.delete(0, tk.END)
        for _, pelicula in top_10.iterrows():
            self.recomendaciones_listbox.insert(tk.END, f"{pelicula['title']} - Rating: {pelicula['vote_average']}")

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

        # Obtener índices de las películas más similares
        similar_indices = cosine_similarities.argsort()[::-1]

        # Filtrar películas ya calificadas
        recommendations = []
        for idx in similar_indices:
            if self.df.iloc[idx]['title'] not in self.user_ratings:
                recommendations.append((self.df.iloc[idx]['title'], self.df.iloc[idx]['vote_average'], cosine_similarities[idx]))
            if len(recommendations) == 10:
                break

        # Mostrar recomendaciones
        self.recomendaciones_listbox.delete(0, tk.END)
        for title, rating, similarity in recommendations:
            self.recomendaciones_listbox.insert(tk.END, f"{title} - Rating: {rating:.2f} - Similitud: {similarity:.2f}")

if __name__ == "__main__":
    root = tk.Tk()
    app = RecomendadorPeliculas(root)
    root.mainloop()
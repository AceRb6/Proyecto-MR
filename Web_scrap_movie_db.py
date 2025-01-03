from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup
import json
import psycopg2
import time

# Configura la ruta al EdgeDriver
edge_driver_path = "C:/Users/artu_/Documents/tarea/ESCOM/4S/Analisis de datos/Proyecto-MR/edgedriver/msedgedriver.exe"
options = webdriver.EdgeOptions()
service = Service(executable_path=edge_driver_path)
driver = webdriver.Edge(service=service, options=options)
wait = WebDriverWait(driver, 10)

# Conexión a la base de datos PostgreSQL
conn = psycopg2.connect(
    dbname="Movies", 
    user="postgres", 
    password="as52", 
    host="localhost", 
    port="5433"
)

cur = conn.cursor()

# Recorrer el abecedario
for letter in "a":
    print(f"Procesando la letra '{letter}'...")
    driver.get("https://www.imdb.com/")
    
    # Buscar la letra en IMDb
    search_bar = driver.find_element(By.ID, "suggestion-search")
    search_bar.clear()
    search_bar.send_keys(letter)
    search_bar.send_keys(Keys.RETURN)
    time.sleep(2)

    try:
        peliculas_chip = driver.find_element(By.XPATH, "//a[contains(@href, '/find/') and contains(., 'Películas')]")
        peliculas_chip.click()
        time.sleep(2)
    except Exception as e:
        print(f"No se encontró la opción 'Películas' para la letra '{letter}': {e}")
        continue

    # Expande "Coincidencias más populares" haciendo clic en el botón tres veces
    for _ in range(1):
        try:
            # Buscar y hacer clic en el botón "Coincidencias más populares"
            load_more_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'ipc-see-more__button') and .//span[text()='Coincidencias más populares']]")))
            ActionChains(driver).move_to_element(load_more_button).click().perform()
            time.sleep(2)  # Esperar a que se carguen más películas
            print("Se ha cargado un nuevo conjunto de películas.")
        except:
            print("No se encontró el botón o no hay más resultados para cargar.")
            break  # Rompe el bucle si no se encuentra el botón o no hay más resultados

    # Extrae los enlaces de todas las películas ahora desplegadas
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    movie_links = []
    results = soup.find_all('a', href=True)
    for result in results:
        if '/title/' in result['href'] and '/find/' not in result['href']:
            link = f"https://www.imdb.com{result['href']}"
            movie_links.append(link)

    # Extraer y guardar la información de cada película
    for url in movie_links:
        driver.get(url)
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        json_ld_tag = soup.find('script', type='application/ld+json')
        if json_ld_tag:
            try:
                json_data = json.loads(json_ld_tag.string)
                title = json_data.get("name", "Título no encontrado")
                vote_average = json_data.get("aggregateRating", {}).get("ratingValue")
                keywords = json_data.get("keywords", "Keywords no encontrados")
                genres = json_data.get("genre", [])
                director = json_data.get("director", [{}])[0].get("name", "Director no encontrado")
                actors = ", ".join([actor.get("name", "Actor no encontrado") for actor in json_data.get("actor", [])])

                cur.execute("SELECT id FROM movies WHERE title = %s", (title,))
                if cur.fetchone():
                    print(f"La película '{title}' ya existe en la base de datos, omitiendo inserción.")
                    continue

                cur.execute("INSERT INTO directors (director_name) VALUES (%s) ON CONFLICT (director_name) DO NOTHING", (director,))
                cur.execute("SELECT id FROM directors WHERE director_name = %s", (director,))
                director_id = cur.fetchone()[0]

                cur.execute("""
                    INSERT INTO movies (title, vote_average, keywords, cast_, director_id)
                    VALUES (%s, %s, %s, %s, %s) RETURNING id
                """, (title, vote_average, keywords, actors, director_id))
                movie_id = cur.fetchone()[0]

                for genre in genres:
                    cur.execute("INSERT INTO genres (genre_name) VALUES (%s) ON CONFLICT (genre_name) DO NOTHING", (genre,))
                    cur.execute("SELECT id FROM genres WHERE genre_name = %s", (genre,))
                    genre_id = cur.fetchone()[0]
                    cur.execute("INSERT INTO movie_genres (movie_id, genre_id) VALUES (%s, %s) ON CONFLICT DO NOTHING", (movie_id, genre_id))

                conn.commit()
                print(f"Datos de '{title}' insertados en la base de datos correctamente.")

            except json.JSONDecodeError:
                print(f"Error al decodificar JSON para la película {url}.")
        else:
            print(f"No se encontró el contenido JSON-LD en la página de {url}.")

# Cerrar la conexión y el navegador
cur.close()
conn.close()
driver.quit()

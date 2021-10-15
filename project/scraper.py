""" Importa bibliotecas """
import os
import requests
import pandas as pd 
from bs4 import BeautifulSoup

def get_rating(movie_container):
    """ Função para buscar verificar se nota está presente no container do filme """
    if movie_container.strong is not None:
        return float(movie_container.strong.text)
    else:
        return None

def generate_file(genre, movies):
    """ Função para gerar arquivos JSONL de cada genero """
    data_frame = pd.DataFrame(movies)
    print(f'Gerando arquivo...')
    output_path = 'outputs'
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    file_name = f'{genre}.jsonl'

    with open(os.path.join(output_path, file_name), 'w', encoding='utf-8') as file:
        data_frame.to_json(file, orient='records', lines=True)
       
    print(f'GÊNERO {genre.upper()} FINALIZADO\n')


def scrap_movie_info(genre):
    """ Função para buscar filmes por gênero """
    names = []
    ratings = []
    start = 1
    page = 1
    print(f'BUSCANDO DADOS DO GÊNERO: {genre.upper()}')
    # acessa 10 paginas com 50 registros
    while len(names) < 500:
        try:
            url=f"""https://www.imdb.com/search/title/?genres={genre}&sort=user_rating,desc&
            start={start}&explore=title_type,genres&title_type=movie"""
            print(f'Buscando dados da pagina {page}.')
            response = requests.get(url)
            # verifica status da requisição
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")
                # busca containers principais que possuem todos dados dos filmes
                movie_containers = soup.find_all('div', class_ = 'lister-item mode-advanced')
                # busca nomes dos filmes
                names = names + [movie_container.h3.a.text for movie_container in movie_containers]
                # busca avaliações dos filmes
                ratings = ratings + [get_rating(movie_container)
                    for movie_container in movie_containers]

            else:
                print(f'Erro na requisição para a url: {url}. Status code: {response.status_code}')
        except AttributeError:
            print(f'Erro na busca dos dados para a url: {url}.')

        # incrementa contador de acordo com o número de itens por página
        start += 50
        page += 1

    data_movies = {
        'movie': names[:500],
        'rating': ratings[:500],
    }

    generate_file(genre, data_movies)
 
 
if __name__ == '__main__':
    genres = [
        'action', 'adventure', 'animation', 'biography', 'comedy', 
        'crime', 'documentary', 'drama', 'family', 'fantasy', 
        'film-noir', 'history', 'horror', 'music', 'musical', 
        'mystery', 'romance', 'sci-fi', 'sport', 'war', 'western',
    ]
    for genre in genres:
        scrap_movie_info(genre)

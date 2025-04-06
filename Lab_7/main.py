import numpy as np
import pickle

import psycopg2 as pg
import pandas.io.sql as psql
import pandas as pd

from typing import Union, List, Tuple

connection = pg.connect(host='pgsql-196447.vipserv.org', port=5432, dbname='wbauer_adb_2023', user='wbauer_adb', password='adb2020')

def film_in_category(category:Union[int,str])->pd.DataFrame:
    if isinstance(category,int):
        df = pd.read_sql('SELECT film.title, language.name AS languge, category.name AS category\
                        FROM category JOIN film_category ON film_category.category_id = category.category_id\
                        JOIN film ON film.film_id = film_category.film_id\
                        JOIN language ON language.language_id = film.language_id\
                        WHERE category.category_id = %s \
                        ORDER BY film.title, language.name', con=connection, params = (category,))
        
        if df.empty:
            df.index = pd.Index([], dtype='object')
            return df
        return df
    if isinstance(category,str):      
        df = pd.read_sql('SELECT film.title, language.name AS languge, category.name AS category\
                        FROM category JOIN film_category ON film_category.category_id = category.category_id\
                        JOIN film ON film.film_id = film_category.film_id\
                        JOIN language ON language.language_id = film.language_id\
                        WHERE category.name = %s \
                        ORDER BY film.title, language.name', con=connection, params = (category,))
        
        if df.empty:
            df.index = pd.Index([], dtype='object')
            return df
        return df

    return None
    ''' Funkcja zwracająca wynik zapytania do bazy o tytuł filmu, język, oraz kategorię dla zadanego:
        - id: jeżeli categry jest int
        - name: jeżeli category jest str, dokładnie taki jak podana wartość
    Przykład wynikowej tabeli:
    |   |title          |languge    |category|
    |0	|Amadeus Holy	|English	|Action|
    
    Tabela wynikowa ma być posortowana po tylule filmu i języku.
    
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
    
    Parameters:
    category (int,str): wartość kategorii po id (jeżeli typ int) lub nazwie (jeżeli typ str)  dla którego wykonujemy zapytanie
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''
    
def film_in_category_case_insensitive(category:Union[int,str])->pd.DataFrame:
    if isinstance(category,int):
        df = pd.read_sql('SELECT film.title, language.name AS languge, category.name AS category\
                    FROM category JOIN film_category ON film_category.category_id = category.category_id\
                    JOIN film ON film.film_id = film_category.film_id\
                    JOIN language ON language.language_id = film.language_id\
                    WHERE category.category_id = %s \
                    ORDER BY film.title, language.name', con=connection, params = (category,))
        if (df.empty == True):
            df.index = pd.Index([], dtype='object')
        return df
    if isinstance(category,str):      
        df = pd.read_sql('SELECT film.title, language.name AS languge, category.name AS category\
                        FROM category JOIN film_category ON film_category.category_id = category.category_id\
                        JOIN film ON film.film_id = film_category.film_id\
                        JOIN language ON language.language_id = film.language_id\
                        WHERE LOWER(category.name) = LOWER(%s) \
                        ORDER BY film.title, language.name', con=connection, params = (category,))
        if (df.empty == True):
            df.index = pd.Index([], dtype='object')
        return df
    return None  
    ''' Funkcja zwracająca wynik zapytania do bazy o tytuł filmu, język, oraz kategorię dla zadanego:
        - id: jeżeli categry jest int
        - name: jeżeli category jest str
    Przykład wynikowej tabeli:
    |   |title          |languge    |category|
    |0	|Amadeus Holy	|English	|Action|
    
    Tabela wynikowa ma być posortowana po tylule filmu i języku.
    
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
    
    Parameters:
    category (int,str): wartość kategorii po id (jeżeli typ int) lub nazwie (jeżeli typ str)  dla którego wykonujemy zapytanie
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''
    return None
    
def film_cast(title:str)->pd.DataFrame:

    if isinstance(title,str):      
        df = pd.read_sql('SELECT actor.first_name, actor.last_name \
                        FROM actor JOIN film_actor ON film_actor.actor_id = actor.actor_id\
                        JOIN film ON film.film_id = film_actor.film_id\
                        WHERE film.title = %s \
                        ORDER BY actor.last_name, actor.first_name ', con=connection, params = (title,))
        return df
    return None  
    ''' Funkcja zwracająca wynik zapytania do bazy o obsadę filmu o dokładnie zadanym tytule.
    Przykład wynikowej tabeli:
    |   |first_name |last_name  |
    |0	|Greg       |Chaplin    | 
    
    Tabela wynikowa ma być posortowana po nazwisku i imieniu klienta.
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
        
    Parameters:
    title (int): wartość id kategorii dla którego wykonujemy zapytanie
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''


def film_title_case_insensitive(words:list) :

    if isinstance(words, list) and all(isinstance(word, str) for word in words):
        
        query = "SELECT title FROM film WHERE film.title ~* %s"
        pattern = '|'.join([rf'\y{word}\y' for word in words])

        df = pd.read_sql(query, con=connection, params = (pattern,))
        return df

    return None 
    ''' Funkcja zwracająca wynik zapytania do bazy o tytuły filmów zawierających conajmniej jedno z podanych słów z listy words.
    Przykład wynikowej tabeli:
    |   |title              |
    |0	|Crystal Breaking 	| 
    
    Tabela wynikowa ma być posortowana po nazwisku i imieniu klienta.

    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
        
    Parameters:
    words(list): wartość minimalnej długości filmu
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''

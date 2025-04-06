import numpy as np
import pickle

import psycopg2 as pg
import pandas.io.sql as psql
import pandas as pd

from typing import Union, List, Tuple

connection = pg.connect(host='pgsql-196447.vipserv.org', port=5432, dbname='wbauer_adb_2023', user='wbauer_adb', password='adb2020')

def film_in_category(category_id:int)->pd.DataFrame:
    if not isinstance(category_id, int):
        return None

    df = pd.read_sql('SELECT film.title AS title,\
            language.name AS language,\
            category.name AS category\
            FROM category\
            JOIN film_category ON category.category_id = film_category.category_id\
            JOIN film ON film_category.film_id = film.film_id\
            JOIN language ON film.language_id = language.language_id\
            WHERE category.category_id = %s\
            ORDER BY film.title, language.name',con=connection,params=(category_id,))
    return df
    ''' Funkcja zwracająca wynik zapytania do bazy o tytuł filmu, język, oraz kategorię dla zadanego id kategorii.
    Przykład wynikowej tabeli:
    |   |title          |language    |category|
    |0	|Amadeus Holy	|English	|Action|
    
    Tabela wynikowa ma być posortowana po tytule filmu i języku.
    
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
    
    Parameters:
    category_id (int): wartość id kategorii dla którego wykonujemy zapytanie
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''
    return None
    
def number_films_in_category(category_id:int)->pd.DataFrame:
    if not isinstance(category_id, int):
        return None
    
    df = pd.read_sql('SELECT category.name AS category, COUNT(film.film_id) FROM category\
            JOIN  film_category ON category.category_id = film_category.category_id\
            JOIN film ON film.film_id = film_category.film_id\
            WHERE category.category_id = %s\
            GROUP BY category.name',con=connection, params=(category_id,))
    return df
    ''' Funkcja zwracająca wynik zapytania do bazy o ilość filmów w zadanej kategori przez id kategorii.
    Przykład wynikowej tabeli:
    |   |category   |count|
    |0	|Action 	|64	  | 
    
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
        
    Parameters:
    category_id (int): wartość id kategorii dla którego wykonujemy zapytanie
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''
    return None

def number_film_by_length(min_length: Union[int,float] = 0, max_length: Union[int,float] = 1e6 ) :
    if not isinstance(min_length, (int, float)) or not isinstance(max_length, (int, float)) or min_length < 0 or max_length < min_length:
        return None  

    df = pd.read_sql('SELECT film.length, COUNT(film.film_id) from film WHERE film.length >= %s AND film.length <= %s\
                    GROUP BY film.length\
                    ORDER BY film.length',con=connection,params=(min_length,max_length))
    return df
    ''' Funkcja zwracająca wynik zapytania do bazy o ilość filmów o dla poszczegulnych długości pomiędzy wartościami min_length a max_length.
    Przykład wynikowej tabeli:
    |   |length     |count|
    |0	|46 	    |64	  | 
    
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
        
    Parameters:
    min_length (int,float): wartość minimalnej długości filmu
    max_length (int,float): wartość maksymalnej długości filmu
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''
    return None

def client_from_city(city:str)->pd.DataFrame:
    if not isinstance(city, str):
        return None

    df = pd.read_sql('SELECT city.city, customer.first_name, customer.last_name\
                    FROM customer\
                    JOIN address ON address.address_id = customer.address_id\
                    JOIN city ON city.city_id = address.city_id\
                    WHERE city.city = %s\
                    ORDER BY customer.last_name, customer.first_name',con=connection,params = (city,))
    return df
    ''' Funkcja zwracająca wynik zapytania do bazy o listę klientów z zadanego miasta przez wartość city.
    Przykład wynikowej tabeli:
    |   |city	    |first_name	|last_name
    |0	|Athenai	|Linda	    |Williams
    
    Tabela wynikowa ma być posortowana po nazwisku i imieniu klienta.
    
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
        
    Parameters:
    city (str): nazwa miaste dla którego mamy sporządzić listę klientów
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''
    return None

def avg_amount_by_length(length:Union[int,float])->pd.DataFrame:
    if not isinstance(length, (int,float)):
        return None

    df = pd.read_sql('SELECT film.length, AVG(payment.amount) FROM payment\
                    JOIN rental ON rental.rental_id = payment.rental_id\
                    JOIN inventory ON inventory.inventory_id = rental.inventory_id\
                    JOIN film ON film.film_id = inventory.film_id\
                    WHERE film.length = %s\
                    GROUP BY film.length',con=connection,params=(length,))
    return df
    ''' Funkcja zwracająca wynik zapytania do bazy o średnią wartość wypożyczenia filmów dla zadanej długości length.
    Przykład wynikowej tabeli:
    |   |length |avg
    |0	|48	    |4.295389
    
    
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
        
    Parameters:
    length (int,float): długość filmu dla którego mamy pożyczyć średnią wartość wypożyczonych filmów
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''
    return None

def client_by_sum_length(sum_min:Union[int,float])->pd.DataFrame:
    if not isinstance(sum_min, (int,float)):
        return None    
    

    df = pd.read_sql('SELECT customer.first_name, customer.last_name, SUM(film.length) AS sum\
                    FROM customer\
                    JOIN rental ON rental.customer_id = customer.customer_id\
                    JOIN inventory ON inventory.inventory_id = rental.inventory_id\
                    JOIN film ON film.film_id = inventory.film_id\
                    GROUP BY customer.customer_id\
                    HAVING SUM(film.length) >= %s \
                    ORDER BY sum, customer.last_name, customer.first_name',con=connection,params=(sum_min,))
    return df
    ''' Funkcja zwracająca wynik zapytania do bazy o sumaryczny czas wypożyczonych filmów przez klientów powyżej zadanej wartości .
    Przykład wynikowej tabeli:
    |   |first_name |last_name  |sum
    |0  |Brian	    |Wyman  	|1265
    
    Tabela wynikowa powinna być posortowane według sumy, imienia i nazwiska klienta.
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
        
    Parameters:
    sum_min (int,float): minimalna wartość sumy długości wypożyczonych filmów którą musi spełniać klient
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''
    return None  

def category_statistic_length(name:str)->pd.DataFrame:

    if not isinstance(name, str):
        return None    
    

    df = pd.read_sql('SELECT category.name AS category, AVG(film.length) AS avg, SUM(film.length) AS sum, MIN(film.length) AS min, MAX(film.length) AS max\
                    FROM category\
                    JOIN film_category  ON film_category.category_id = category.category_id\
                    JOIN film ON film.film_id = film_category.film_id\
                    WHERE category.name = %s\
                    GROUP BY category.name',con=connection,params=(name,))
    return df
    ''' Funkcja zwracająca wynik zapytania do bazy o statystykę długości filmów w kategorii o zadanej nazwie.
    Przykład wynikowej tabeli:
    |   |category   |avg    |sum    |min    |max
    |0	|Action 	|111.60 |7143   |47 	|185
    
    Jeżeli warunki wejściowe nie są spełnione to funkcja powinna zwracać wartość None.
        
    Parameters:
    name (str): Nazwa kategorii dla której ma zostać wypisana statystyka
    
    Returns:
    pd.DataFrame: DataFrame zawierający wyniki zapytania
    '''
    return None
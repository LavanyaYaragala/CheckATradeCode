import requests
import psycopg2
import json
from datetime import datetime

dt = datetime.now()

def db_load(response):
    try:
        conn = psycopg2.connect(database="postgres", user='postgres', password='Saibabadaddy@7$', host='127.0.0.1', port= '5432')
        cursor = conn.cursor()
        conn.commit()
        rec_nbr = len(response.json()['results'])
        print(rec_nbr)
        sql_master = f'''INSERT INTO public.run(run_time,records) values ('{dt}' , {rec_nbr})'''
        cursor.execute(sql_master)
        conn.commit()
        for i in response.json()['results']:
            species = json.dumps(i['species'])
            vehicles = json.dumps(i['vehicles'])
            starships = json.dumps(i['starships'])
            for j in i['films']:
                film_respone = requests.get(j)
                sql_statement = f'''INSERT INTO public.records(
	name, height, mass, hair_color, skin_color, eye_color, birth_year, gender, homeworld, films, species, vehicles, starships, created, edited, url)
	VALUES ('{i['name']}', {i['height']}, {i['mass']}, '{i['hair_color']}', '{i['skin_color']}', '{i['eye_color']}',
            '{i['birth_year']}', '{i['gender']}', '{i['homeworld']}', '{film_respone.json()['title']}', '{species}', 
            '{vehicles}', '{starships}', '{i['created']}', '{i['edited']}', '{i['url']}')'''
                cursor.execute(sql_statement)
        conn.commit()
        return True

    except Exception as db_error:
        print(db_error)
        return False

def aggr_sql():
    try:
        conn = psycopg2.connect(database="postgres", user='postgres', password='Saibabadaddy@7$', host='127.0.0.1', port= '5432')
        cursor = conn.cursor()
        cursor.execute('''with a as (select (regexp_matches(birth_year, '[0-9]+\.?[0-9]*'))[1]::numeric as birth, films,name, birth_year from public.records),
b as (select min(birth) as birth, films from a
group by films)
select a.name, b.films, a.birth_year from a,b
where a.birth = b.birth
and a.films = b.films''')
        film_rec = cursor.fetchall()

        print("Printing aggregation for oldest character per movie")
        for row in film_rec:
            print("Character Name = ", row[0], )
            print("Film Name = ", row[1])
            print("Birth Year  = ", row[2], "\n")
    except Exception as aggr_err:
        print(aggr_err)
def main(url):
    try:
        response = requests.get(url)
        load_status = db_load(response)
        if load_status:
            aggr_sql()
    except Exception as main_err:
        print(main_err)

if __name__ == '__main__':
    url = 'https://swapi.dev/api/people'
    main(url)

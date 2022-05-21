import requests
import time
import sqlite3
from bs4 import BeautifulSoup

items_map = {}


def make_call():
    page = 1
    while page != 6:
        url_alta = f"https://alta.ge/smartphones-page-{page}.html"
        r = requests.get(url_alta)
        content = r.text
        soup = BeautifulSoup(content, 'html.parser')
        names = soup.findAll('div', {'class': 'ty-grid-list__item-name'})
        images = soup.findAll('img', {'class': 'ty-pict'})

        filtered_names = []
        filtered_images = []

        for i in images:
            if len(i.attrs['class']) == 1:
                filtered_images.append(i.attrs['src'])

        for j in names:
            filtered_names.append(j.text.strip())

        for k in range(len(filtered_images) - 1):
            items_map[filtered_names[k]] = filtered_images[k]

        print(f"Page{page} Done!")
        page += 1
        time.sleep(10)
    return items_map


def create_and_insert_in_db():
    conn = sqlite3.connect("AltaPhones.db")
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS phones")
    cursor.execute('''CREATE TABLE IF NOT EXISTS phones
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                Model VARCHAR (50),
                Image VARCHAR (150)
                )''')

    myd_ict = make_call()
    for model, image in myd_ict.items():
        cursor.execute("INSERT INTO phones (Model, Image) VALUES (?, ?)", (model, image))

    conn.commit()
    conn.close()
    print("Writing Finished!")


create_and_insert_in_db()

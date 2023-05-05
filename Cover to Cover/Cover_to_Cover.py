import os
from PIL import Image
import requests
import random
import csv
from tkinter import *
from PIL import Image, ImageTk
from io import BytesIO

cwd = os.getcwd()
folderPath = os.path.join(cwd, 'resources')
csv_path = os.path.join(folderPath, 'bisac.csv')

def get_options_from_csv(csv_path):
    options = []
    with open(csv_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            options.append(row['genre'])
    return options

def get_book_data(selected_genre):
    endpoint = 'https://www.googleapis.com/books/v1/volumes'
    params = {'q': f'subject:{selected_genre}', 'startIndex': str(random.randint(1, 100)), 'maxResults': '1'}

    response = requests.get(endpoint, params=params)

    if response.status_code == 200:
        try:
            book_data = response.json()['items'][0]['volumeInfo']
            title = book_data['title']
            authors = book_data['authors']
            publisher = book_data['publisher']
            published_date = book_data['publishedDate']
            description = book_data['description']
            categories = book_data['categories']
            image_url = book_data['imageLinks']['thumbnail'].replace('zoom=1', 'zoom=3')

            return {
                'Selected Genre': selected_genre,
                'Title': title,
                'Authors': ", ".join(authors),
                'Publisher': publisher,
                'Published Date': published_date,
                'Genres': ", ".join(categories),
                'Description': description,
                'Image URL': image_url
            }

        except (KeyError, IndexError):
            return {'Error': 'No books found'}

    else:
        return {'Error': 'Request failed'}

options = get_options_from_csv(csv_path)

root = Tk()
root.title('Cover to Cover')

genre_var = StringVar(value=options)
genre_listbox = Listbox(root, listvariable=genre_var, height=len(options))
genre_listbox.pack(side=LEFT, fill=BOTH, expand=True)

book_frame = Frame(root)
book_frame.pack(side=RIGHT, fill=BOTH, expand=True)

canvas = Canvas(book_frame, borderwidth=0)
scrollbar = Scrollbar(book_frame, orient="vertical", command=canvas.yview)
scrollable_frame = Frame(canvas)

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(
        scrollregion=canvas.bbox("all")
    )
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill=BOTH, expand=True)

def show_book_data(event):
    widget = event.widget
    selection = widget.curselection()
    if selection:
        selected_genre = widget.get(selection[0])
        book_data = get_book_data(selected_genre)

        for i, (key, value) in enumerate(book_data.items()):
            label = Label(root, text=f'{key}: {value}')
            label.pack(fill=BOTH, padx=10, pady=5)
            
        # Fetch and display image from URL
        response = requests.get(book_data['Image URL'])
        img = Image.open(BytesIO(response.content))
        photo = ImageTk.PhotoImage(img)
        img_label = Label(root, image=photo)
        img_label.image = photo
        img_label.pack(fill=BOTH, padx=10, pady=5)

genre_listbox.bind('<Double-Button-1>', show_book_data)

root.mainloop()
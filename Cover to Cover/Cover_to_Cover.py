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
# initialize set to keep track of previously generated random numbers
generated_numbers = set()
# initialize total books
total_books = 0

def get_options_from_csv(csv_path):
    options = []
    with open(csv_path, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            options.append(row['genre'])
    return options

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

label_list = []

def count_books(event):
    #Set global variable
    global total_books
    # Get the selected genre from the Listbox
    selected_genre = event.widget.get(event.widget.curselection())
    #Endpoint URL for Google Books API
    endpoint = 'https://www.googleapis.com/books/v1/volumes'
    #Parameters to send to API - Replace spaces with + and display 1 random result
    params = {'q': f'subject:{selected_genre.replace(" ", "+")}', 'startIndex': '1', 'maxResults': '1'}
    #Get request to API
    response = requests.get(endpoint, params=params)

    #If no error in response
    if response.status_code == 200:
        # Get total number of items
        total_books = response.json().get('totalItems', 0)
        # Check if total_books is greater than zero
        if total_books > 0:
            return True
    return False

def get_book_data(event, selected_genre):
    if not count_books(event):
        print("Genre does not have any results left to show.")
        return

    # generate random number until unique one is found
    while True:
        if len(generated_numbers) == total_books:
            print("No more numbers can be selected.")
            return  # return from the function
        random_number = random.randint(1, total_books)
        if random_number not in generated_numbers:
            generated_numbers.add(random_number)
            break

    # Clear the existing labels
    for label in label_list:
        label.destroy()

    # Get the selected genre from the Listbox
    selected_genre = event.widget.get(event.widget.curselection())
    #Endpoint URL for Google Books API
    endpoint = 'https://www.googleapis.com/books/v1/volumes'
    #Parameters to send to API - Replace spaces with + and display 1 random result
    params = {'q': f'subject:{selected_genre.replace(" ", "+")}', 'startIndex': str(random_number), 'maxResults': '1'}
    #Get request to API
    response = requests.get(endpoint, params=params)

    #If no error in response
    if response.status_code == 200:
        try:
            book_data = response.json()['items'][0]['volumeInfo']

            # Create and populate the labels with the book data
            title_label = Label(scrollable_frame, text=f'Title: {book_data["title"]}')
            title_label.pack(pady=(10, 0), padx=10, anchor=W)
            
            if "authors" in book_data:
                author_label = Label(scrollable_frame, text=f'Author: {book_data["authors"][0]}')
                author_label.pack(pady=10, padx=10, anchor=W)
                
            if "categories" in book_data:
                genre_label = Label(scrollable_frame, text=f'Genre: {book_data["categories"]}')
                genre_label.pack(pady=10, padx=10, anchor=W)

            if "description" in book_data:
                desc_label = Label(scrollable_frame, text=f'Description {book_data["description"]}')
                desc_label.pack(pady=10, padx=10, anchor=W)

            cover_label = Label(scrollable_frame)

            # Get the URL for the book cover image
            if "imageLinks" in book_data and "thumbnail" in book_data["imageLinks"]:
                cover_url = book_data['imageLinks']['thumbnail'] #.replace('zoom=1', 'zoom=3')

                # Get the image data from the URL
                response = requests.get(cover_url)
                img_data = response.content

                # Convert the image data to a Tkinter PhotoImage
                img = ImageTk.PhotoImage(Image.open(BytesIO(img_data)))

                # Add the image to the cover label
                cover_label.img = img
                cover_label.configure(image=img)

                # Add the labels to the window
                cover_label.pack(pady=10, padx=10, anchor=CENTER)

            else:
                cover_label.pack(pady=10, padx=10, anchor=CENTER)
                cover_label.configure(text="No cover available")

            label_list.extend([title_label, author_label, genre_label, desc_label, cover_label])

        except (KeyError, IndexError):
            error_label = Label(scrollable_frame, text="No books found")
            error_label.pack(pady=10, padx=10, anchor=CENTER)
            label_list.append(error_label)

    else:
        error_label = Label(scrollable_frame, text="Request failed")
        error_label.pack(pady=20)
        label_list.append(error_label) # Add the error label to the list of labels

        root.mainloop()


genre_listbox.bind('<Double-Button-1>', lambda event: get_book_data(event, genre_listbox.get(genre_listbox.curselection())))

root.mainloop()
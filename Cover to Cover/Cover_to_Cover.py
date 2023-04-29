import csv
import random
import urllib.request
import io
import os
from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk

random_book = NONE
show_info = False
books = []
myLikedGenres = []
# get current working directory
cwd = os.getcwd()
folderPath = os.path.join(cwd, 'resources')

# Parse CSV and store all genres in a list
genres = []
with open(os.path.join(folderPath, 'books.csv'), encoding='utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        for genre in row['genres'].split(', '):
            if genre not in genres:
                genres.append(genre)

# Display list of genres and prompt user to select one
for i, genre in enumerate(genres):
    # Remove apostrophes and brackets from genre string
    genre = genre.replace("'", "").replace("[", "").replace("]", "")
    print(f"{i+1}. {genre}")
print("Select a genre:")
selection = int(input()) - 1
myGenre = genres[selection].replace("'", "").replace("[", "").replace("]", "")

def rand_book():
    global random_book
    # Select a random book with the selected genre
    with open(os.path.join(folderPath, 'books.csv'), encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if myGenre in row['genres']:
                books.append(row)
    random_book = random.choice(books)

rand_book()

def update_book():
    rand_book()
    # Select a random book with the selected genre
    with open(os.path.join(folderPath, 'books.csv'), encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if myGenre in row['genres']:
                books.append(row)
    random_book = random.choice(books)

    #Update title label
    title_lbl.config(text=f"Title: {random_book['title']}", font=("Helvetica", 20))

    # Open the cover image in the program
    img_url = random_book['coverImg']
    with urllib.request.urlopen(img_url) as url:
        image_data = url.read()

    # Create a file-like object from the image data
    image_file = io.BytesIO(image_data)
    cover = Image.open(image_file).resize((400, 600))
    cov_img = ImageTk.PhotoImage(cover)
    cov_lbl.configure(image=cov_img)
    cov_lbl.image = cov_img

def show_book_info():
    global show_info
    if show_info == False:
        show_info = True
        author_lbl.config(text=f"Author: {random_book['author']}", font=("Helvetica", 12))
        rating_lbl.config(text=f"Rating: {random_book['rating']}", font=("Helvetica", 12))
        description_lbl.config(text=f"Description: {random_book['description']}", font=("Helvetica", 12), anchor=CENTER)
        pages_lbl.config(text=f"Pages: {random_book['pages']}", font=("Helvetica", 12))
    else:
        show_info = False
        author_lbl.config(text="")
        rating_lbl.config(text="")
        description_lbl.config(text="")
        pages_lbl.config(text="")
        update_book()

#Create UI
root = Tk()
root.title("Cover to Cover")

# Create labels and buttons
title_lbl = Label(root, text=f"Title: {random_book['title']}", font=("Helvetica", 20))
title_lbl.pack(pady=20)

# Open the cover image in the program
img_url = random_book['coverImg']
with urllib.request.urlopen(img_url) as url:
    image_data = url.read()

# Create a file-like object from the image data
image_file = io.BytesIO(image_data)

cover = Image.open(image_file).resize((400, 600))
cov_img = ImageTk.PhotoImage(cover)
cov_lbl = Label(root, image=cov_img)
cov_lbl.image = cov_img
cov_lbl.pack()

x_btn_img = ImageTk.PhotoImage(Image.open(os.path.join(folderPath, "x_btn.png")).resize((128, 128)))
x_btn = Button(root, image=x_btn_img, command=update_book)
x_btn.image = x_btn_img
x_btn.place(x=550, y=350)

heart_btn_img = ImageTk.PhotoImage(Image.open(os.path.join(folderPath, "heart_btn.png")).resize((128, 128)))
heart_btn = Button(root, image=heart_btn_img, command=show_book_info)
heart_btn.image = heart_btn_img
heart_btn.place(x=1225, y=350)

author_lbl = Label()
author_lbl.pack(pady=10)
rating_lbl = Label()
rating_lbl.pack(pady=10)
description_lbl = Label(wraplength=800)
description_lbl.pack(pady=10)
pages_lbl = Label()
pages_lbl.pack(pady=10)

# Set window size to fit all widgets
root.geometry("%dx%d" % (root.winfo_reqwidth(), root.winfo_reqheight()))

root.mainloop()
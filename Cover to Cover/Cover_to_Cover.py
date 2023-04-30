import csv
import random
import urllib.request
import io
import os
from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk
import pyglet
from pyglet import image, sprite
from pyglet.window import mouse

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

    # Open the cover image in the program
    img_url = random_book['coverImg']
    with urllib.request.urlopen(img_url) as url:
        image_data = url.read()

    # Create a PIL image object from the image data
    pil_image = Image.open(io.BytesIO(image_data))

    # Resize the image to be 500x600
    resized_image = pil_image.resize((300, 400))

    # Convert the PIL image to a Pyglet image
    pyglet_image = pyglet.image.ImageData(resized_image.width, resized_image.height, 'RGB', resized_image.tobytes(), pitch=resized_image.width * -3)
    cov_lbl.image = pyglet_image

#Function for updating additional information labels with data or null values
def show_book_info():
    #Variable for boolean value
    global show_info
    #If boolean is false
    if show_info == False:
        #Update boolean to true
        show_info = True
        #Update labels with data
        author_lbl.text = f"Author: {random_book['author']}"
        rating_lbl.text = f"Rating: {random_book['rating']}"
        pages_lbl.text = f"Pages: {random_book['pages']}"
        description_lbl.text = f"Description: {random_book['description']}"
    else:
        #Update boolean to false
        show_info = False
        #Update labels to null
        author_lbl.text = ""
        rating_lbl.text = ""
        description_lbl.text = ""
        pages_lbl.text = ""
        #Update book title and image
        update_book()

# Create a window
window = pyglet.window.Window(width=800, height=1080)

# set the background color to white
pyglet.gl.glClearColor(1, 1, 1, 1)

# Create title label
title_lbl = pyglet.text.Label(text=f"Title: {random_book['title']}", x = (window.width - 300) // 2, y = window.height - 30, color=(0, 0, 0, 255))

# Open the cover image in the program
img_url = random_book['coverImg']
with urllib.request.urlopen(img_url) as url:
    image_data = url.read()

# Create a PIL image object from the image data
pil_image = Image.open(io.BytesIO(image_data))

# Resize the image to be 500x600
resized_image = pil_image.resize((300, 400))

# Convert the PIL image to a Pyglet image
pyglet_image = pyglet.image.ImageData(resized_image.width, resized_image.height, 'RGB', resized_image.tobytes(), pitch=resized_image.width * -3)

# Create the sprite and assign the new image to it
cov_lbl = pyglet.sprite.Sprite(pyglet_image)
cov_lbl.x = (window.width - cov_lbl.width) // 2
cov_lbl.y = title_lbl.y - cov_lbl.height - 30

# X button
x_btn_img = pyglet.image.load(os.path.join(folderPath, "x_btn.png"))
x_btn = sprite.Sprite(x_btn_img)
x_btn.scale = 64 / x_btn.width
x_btn.x = cov_lbl.x - x_btn.width - 15
x_btn.y = cov_lbl.y

# Heart button
heart_btn_img = pyglet.image.load(os.path.join(folderPath, "heart_btn.png"))
heart_btn = sprite.Sprite(heart_btn_img)
heart_btn.scale = 64 / heart_btn.width
heart_btn.x = cov_lbl.x + cov_lbl.width + 15
heart_btn.y = cov_lbl.y

# Create other labels
author_lbl = pyglet.text.Label(text="", x = cov_lbl.x - 30, y = cov_lbl.y - 30, color=(0, 0, 0, 255))
rating_lbl = pyglet.text.Label(text="", x = cov_lbl.x - 30, y = author_lbl.y - 30, color=(0, 0, 0, 255))
pages_lbl = pyglet.text.Label(text="", x = cov_lbl.x - 30, y = rating_lbl.y - 30, color=(0, 0, 0, 255))
description_lbl = pyglet.text.Label(text="", x = cov_lbl.x - 30, y = pages_lbl.y - 30, width=360, multiline=True, color=(0, 0, 0, 255))

@window.event
def on_draw():
    window.clear()
    cov_lbl.draw()
    x_btn.draw()
    heart_btn.draw()
    author_lbl.draw()
    rating_lbl.draw()
    description_lbl.draw()
    pages_lbl.draw()
    title_lbl.draw()

@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == pyglet.window.mouse.LEFT:
        if x_btn.x <= x <= x_btn.x + x_btn.width and x_btn.y <= y <= x_btn.y + x_btn.height:
            update_book()
        elif heart_btn.x <= x <= heart_btn.x + heart_btn.width and heart_btn.y <= y <= heart_btn.y + heart_btn.height:
            show_book_info()

pyglet.app.run()
import random
import io
import os
import csv
import urllib.request
from PIL import Image
from tkinter import *
from tkinter.ttk import *
from PIL import Image, ImageTk
import requests
import pyglet
from pyglet import image, sprite
from pyglet.window import mouse

cwd = os.getcwd()
folderPath = os.path.join(cwd, 'resources')
# Instantiate genres array
genres = []

with open(os.path.join(folderPath, 'bisac.csv'), newline='') as csvfile:
    data = csv.DictReader(csvfile)
    print("Subject")
    print("---------------------------------")
    for row in data:
        genres.append(row['Subject'])

# Ask the user to select a genre from the list
print("Select a genre:")
for i, genre in enumerate(genres):
    print(f"{i+1}. {genre}")
selection = int(input("Enter the number of the genre: "))
genre = genres[selection-1]
# Create a query string to search for a random book in the selected genre
#query_string = f"subject:{genre}"
query_string = "subject:Fiction"

def rand_book():
    global random_book
    # Make a request to the Google Books API
    response = requests.get(f"https://www.googleapis.com/books/v1/volumes?q={query_string}&maxResults=40")

    # Extract a random book from the search results
    if "items" in response.json():
        random_book = random.choice(response.json()["items"])
    else:
        print("No books found.")
        return

def update_book():
    rand_book()

    # Extract the book information from the API response
    title = random_book["volumeInfo"]["title"]
    authors = ", ".join(random_book["volumeInfo"]["authors"])
    publisher = random_book["volumeInfo"].get("publisher", "Unknown")
    published_date = random_book["volumeInfo"].get("publishedDate", "Unknown")
    description = random_book["volumeInfo"].get("description", "No description available")
    page_count = random_book["volumeInfo"].get("pageCount", "Unknown")
    rating = random_book["volumeInfo"].get("averageRating", "Not rated")
    img_url = random_book["volumeInfo"]["imageLinks"]["thumbnail"]

    # Open the book cover image using Pillow
    image_data = requests.get(img_url).content
    # Create a PIL image object from the image data
    pil_image = Image.open(io.BytesIO(image_data))

    # Resize the image to be 500x600
    resized_image = pil_image.resize((300, 400))

    # Convert the PIL image to a Pyglet image
    pyglet_image = pyglet.image.ImageData(resized_image.width, resized_image.height, 'RGB', resized_image.tobytes(), pitch=resized_image.width * -3)
    cov_lbl.image = pyglet_image

    # Print the book information
    print(f"Title: {title}")
    print(f"Author(s): {authors}")
    print(f"Publisher: {publisher}")
    print(f"Publication Date: {published_date}")
    print(f"Description: {description}")
    print(f"Number of Pages: {page_count}")
    print(f"Rating: {rating}")

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

img_url = random_book["volumeInfo"]["imageLinks"]["thumbnail"]
# Open the book cover image using Pillow
image_data = requests.get(img_url).content
# Create a PIL image object from the image data
pil_image = Image.open(io.BytesIO(image_data))

# Resize the image to be 500x600
resized_image = pil_image.resize((300, 400))

# Convert the PIL image to a Pyglet image
pyglet_image = pyglet.image.ImageData(resized_image.width, resized_image.height, 'RGB', resized_image.tobytes(), pitch=resized_image.width * -3)
cov_lbl.image = pyglet_image

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
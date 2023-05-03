import requests
import random
import io
import os
import csv
import pyglet
from PIL import Image

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
1452
# Create a query string to search for a random book in the selected genre
query_string = f"subject:{genre}"

def update_book():
    # Make a request to the Google Books API
    response = requests.get(f"https://www.googleapis.com/books/v1/volumes?q={query_string}&maxResults=100")

    # Extract a random book from the search results
    book = random.choice(response.json()["items"])

    # Extract the book information from the API response
    title = book["volumeInfo"]["title"]
    authors = ", ".join(book["volumeInfo"]["authors"])
    publisher = book["volumeInfo"].get("publisher", "Unknown")
    published_date = book["volumeInfo"].get("publishedDate", "Unknown")
    description = book["volumeInfo"].get("description", "No description available")
    page_count = book["volumeInfo"].get("pageCount", "Unknown")
    rating = book["volumeInfo"].get("averageRating", "Not rated")
    image_url = book["volumeInfo"]["imageLinks"]["thumbnail"]

    # Open the book cover image using Pillow
    image_data = requests.get(image_url).content
    image = Image.open(io.BytesIO(image_data))

    # Print the book information
    print(f"Title: {title}")
    print(f"Author(s): {authors}")
    print(f"Publisher: {publisher}")
    print(f"Publication Date: {published_date}")
    print(f"Description: {description}")
    print(f"Number of Pages: {page_count}")
    print(f"Rating: {rating}")

    # Display the book cover image
    image.show()

update_book()

# Ask user if they want to see another random book
choice = input("Would you like to see another book? (yes/no) ").lower()
if choice == "yes":
    update_book()
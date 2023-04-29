import csv
import random
import urllib.request
import io
from PIL import Image

# Parse CSV and store all genres in a list
genres = []
with open('C:\\Users\\alext\\Downloads\\books\\books.csv', encoding='utf-8') as csv_file:
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
myGenre = genres[selection]

while True:
    # Select a random book with the selected genre
    books = []
    with open('C:\\Users\\alext\\Downloads\\books\\books.csv', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            if myGenre in row['genres']:
                books.append(row)
    random_book = random.choice(books)
    print(f"Title: {random_book['title']}")

    # Open the cover image in the program
    img_url = random_book['coverImg']
    with urllib.request.urlopen(img_url) as url:
        image_data = url.read()

    # Create a file-like object from the image data
    image_file = io.BytesIO(image_data)

    # Open the image using Pillow and display it
    image = Image.open(image_file)
    image.show()

    # Prompt user for more information
    print("Would you like to see more information?")
    response = input().lower()
    if response == 'yes':
        image.close()
        # Display additional data for the selected book
        print(f"Author: {random_book['author']}")
        print(f"Rating: {random_book['rating']}")
        print(f"Description: {random_book['description']}")
        print(f"Pages: {random_book['pages']}")
        print(f"Liked Percent: {random_book['likedPercent']}")

        # Store all genres from the selected book in a list
        myLikedGenres = []
        for genre in random_book['genres'].split(', '):
            if genre not in myLikedGenres:
                myLikedGenres.append(genre)

        # Prompt user for the next book
        print("Would you like to see the next random book?")
        response = input().lower()
        if response != 'yes':
            image.close()
            exit()
    else:
        image.close()
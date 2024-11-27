#!/usr/bin/env python
# coding: utf-8

# In[89]:


# Import necessary libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

# Define the target URL and headers
url = 'http://books.toscrape.com/catalogue/page-{}.html'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'}

# Lists to store scraped data
book_titles = []
book_prices = []
book_availabilities = []
book_ratings = []

# Loop through multiple pages
for page in range(1, 6):  # Adjust range to scrape more pages if needed
    print(f'Scraping page {page}...')
    page_url = url.format(page)
    response = requests.get(page_url, headers=headers)
    
    # Check if request was successful
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find all book containers
        books = soup.find_all('article', class_='product_pod')
        
        for book in books:
            # Get title
            title = book.h3.a['title']
            book_titles.append(title)
            
            # Get price
            price = book.find('p', class_='price_color').text
            book_prices.append(price)
            
            # Get availability
            availability = book.find('p', class_='instock availability').text.strip()
            book_availabilities.append(availability)
            
            # Get rating
            rating = book.p['class'][1]  # The second class in 'class' attribute
            book_ratings.append(rating)
            
        # Pause to be polite to the server
        time.sleep(1)
    else:
        print(f'Failed to retrieve page {page}')
        break

# Create a DataFrame with the collected data
df = pd.DataFrame({
    'Title': book_titles,
    'Price': book_prices,
    'Availability': book_availabilities,
    'Rating': book_ratings
})

# Display the DataFrame
df.head()

# Save to CSV
df.to_csv('C:/Users/libya/OneDrive/Desktop/Web Scrapping/1st Project/books_data.csv', index=False)


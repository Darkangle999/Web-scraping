import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

def scrape_website(url):
    """
    Scrape a website and extract key information
    
    Args:
        url (str): The URL of the website to scrape
    
    Returns:
        list: A list of dictionaries containing scraped data
    """
    try:
        # Send a GET request to the website
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        
        # Check if the request was successful
        response.raise_for_status()
        
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract blog post information (adjust selectors as needed)
        scraped_data = []
        blog_posts = soup.find_all('div', class_='blog-post')
        
        for post in blog_posts:
            # Extract title
            title = post.find('h2', class_='post-title')
            title = title.text.strip() if title else 'No Title'
            
            # Extract excerpt
            excerpt = post.find('p', class_='post-excerpt')
            excerpt = excerpt.text.strip() if excerpt else 'No excerpt available'
            
            # Extract date
            date = post.find('span', class_='post-date')
            date = date.text.strip() if date else datetime.now().strftime('%Y-%m-%d')
            
            # Extract link
            link = post.find('a', class_='post-link')
            link = link['href'] if link and link.has_attr('href') else ''
            
            # Create a dictionary for each post
            post_data = {
                'title': title,
                'excerpt': excerpt,
                'date': date,
                'link': link
            }
            
            scraped_data.append(post_data)
        
        return scraped_data
    
    except requests.RequestException as e:
        print(f"Error occurred while scraping: {e}")
        return []

def save_to_csv(data, filename='scraped_data.csv'):
    """
    Save scraped data to a CSV file
    
    Args:
        data (list): List of dictionaries containing scraped data
        filename (str): Name of the output CSV file
    """
    if not data:
        print("No data to save.")
        return
    
    try:
        keys = data[0].keys()
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            dict_writer = csv.DictWriter(csvfile, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)
        print(f"Data saved to {filename}")
    
    except Exception as e:
        print(f"Error saving to CSV: {e}")

def main():
    # Example usage
    url = 'Your scrap-able website'  # Replace with the actual website URL
    
    # Scrape the website
    scraped_results = scrape_website(url)
    
    # Print results
    for item in scraped_results:
        print(item)
    
    # Save to CSV
    save_to_csv(scraped_results)

if __name__ == '__main__':
    main()

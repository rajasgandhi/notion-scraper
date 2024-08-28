import requests
from bs4 import BeautifulSoup
import re

# Get all article links from the sitemap
def get_article_links(sitemap_url):
    sitemap = requests.get(sitemap_url)
    soup = BeautifulSoup(sitemap.text, 'xml')
    urls = soup.find_all('loc')
    article_links = [url.text for url in urls]
    return article_links

# Get content for a single article
def get_article_content(url):
    print(f"Processing content from: {url}")
    
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract titles, paragraphs, and notes
    title = soup.find('h1').get_text(strip=True)  # Adjust based on structure
    paragraphs = soup.find_all('p')
    
    content = title + "\n"
    for paragraph in paragraphs:
        content += paragraph.get_text(strip=True) + "\n"
    
    return content.strip()

# Chunk the text into smaller parts
def chunk_text(text, max_length=750):
    chunks = []
    current_chunk = ""
    
    for line in text.splitlines():
        if len(current_chunk) + len(line) + 1 > max_length:
            chunks.append(current_chunk.strip())
            current_chunk = line
        else:
            current_chunk += "\n" + line
            
    if current_chunk:
        chunks.append(current_chunk.strip())
    
    return chunks

# Clean the text
def clean_text(text):
    # Replace multiple newlines with a single newline
    text = re.sub(r'\n+', '\n', text)
    
    # Additional cleaning as needed
    return text.strip()

def main():
    # Get all article links from notion help sitemap
    article_links = get_article_links('https://www.notion.so/sitemaps/sitemap-help.xml')
    # Get content for all articles
    articles_content = [get_article_content(link) for link in article_links]

    # Chunk all articles
    articles_chunks = [chunk_text(article) for article in articles_content]

    # Flatten the list of lists
    final_chunks = [chunk for article in articles_chunks for chunk in article]

    # Clean all chunks
    final_output = [clean_text(chunk) for chunk in final_chunks]

    # Write the output to a file
    with open('out.txt', 'w') as f:
        for chunk in final_output:
            f.write(chunk)
            f.write("\n----\n")

    print(final_output)

if __name__ == '__main__':
    main()
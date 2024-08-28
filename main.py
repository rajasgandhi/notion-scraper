import requests
from bs4 import BeautifulSoup
import re

# Get all the urls from this sitemap and save them in a file
sitemap_url = 'https://www.notion.so/sitemaps/sitemap-help.xml'
sitemap = requests.get(sitemap_url)
soup = BeautifulSoup(sitemap.text, 'xml')
urls = soup.find_all('loc')
# article_links = [url.text for url in urls]
# Get article_links from urls.txt
with open('urls.txt', 'r') as f:
    article_links = f.readlines()
    article_links = [link.strip() for link in article_links]
# with open('urls.txt', 'w') as f:
#     for url in urls:
#         f.write(url.text + '\n')

def get_article_content(url):
    print(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Extract titles, paragraphs, and notes
    title = soup.find('h1').get_text(strip=True)  # Adjust based on structure
    paragraphs = soup.find_all('p')
    
    content = title + "\n"
    for para in paragraphs:
        content += para.get_text(strip=True) + "\n"
    
    return content.strip()

# Get content for all articles
articles_content = [get_article_content(link) for link in article_links]

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

# Chunk all articles
articles_chunks = [chunk_text(article) for article in articles_content]

# Flatten the list of lists
final_chunks = [chunk for article in articles_chunks for chunk in article]

def clean_text(text):
    # Replace multiple newlines with a single newline
    text = re.sub(r'\n+', '\n', text)
    # Additional cleaning as needed
    return text.strip()

# Clean all chunks
final_output = [clean_text(chunk) for chunk in final_chunks]

with open('out.txt', 'w') as f:
    for chunk in final_output:
        f.write(chunk)
        f.write("\n----\n")
        # print(chunk)
        # print("----")

print(final_output)
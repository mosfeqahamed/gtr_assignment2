import os
from dotenv import load_dotenv
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup
import textwrap


load_dotenv()


GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GOOGLE_API_KEY:
    raise ValueError("Please set GOOGLE_API_KEY in your .env file")

genai.configure(api_key=GOOGLE_API_KEY)


model = genai.GenerativeModel('gemini-pro')

def scrape_website(url):
    """Scrape text content from the given URL."""
    try:
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
       
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
       
        soup = BeautifulSoup(response.text, 'html.parser')
        
        
        for script in soup(["script", "style"]):
            script.decompose()
            
       
        text_content = soup.get_text()
        
        
        lines = (line.strip() for line in text_content.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text_content = ' '.join(chunk for chunk in chunks if chunk)
        
       
        chunks = textwrap.wrap(text_content, 8000)
        return chunks
        
    except Exception as e:
        print(f"Error scraping website: {str(e)}")
        return None

def ask_question(content_chunks, query):
    """Generate an answer using Gemini API."""
    try:
       
        prompt_template = """Context: {}

Question: {}

Based on the context provided, please answer the question. If the information is not available in the context, please say so."""

        
        for chunk in content_chunks:
            try:
                prompt = prompt_template.format(chunk, query)
                response = model.generate_content(prompt)
                
                
                if response.text and not response.text.lower().startswith(("i don't", "i cannot", "no information")):
                    return response.text
            except Exception as e:
                continue
        
        return "I couldn't find relevant information to answer your question in the website content."
    
    except Exception as e:
        return f"An error occurred while generating the answer: {str(e)}"

def main():
    
    url = "https://gtrbd.com/"
    
    
    print(f"\nScraping content from {url}...")
    content_chunks = scrape_website(url)
    
    if not content_chunks:
        print("Failed to scrape website content. Exiting...")
        return

    print("\nWebsite content loaded! You can now ask questions about the website.")
    print("(Type 'quit' to exit)")
    
    
    with open("scraped_content.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(content_chunks))
    
    
    while True:
        query = input("\nEnter your question: ")
        if query.lower() == 'quit':
            break
            
        print("\nSearching for answer...")
        answer = ask_question(content_chunks, query)
        print("\nAnswer:", answer)

if __name__ == "__main__":
    main()
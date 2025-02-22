# RAG-Based Website Q&A System 🚀

## Overview
This project is a **Retrieval-Augmented Generation (RAG)** system that:
- Scrapes content from a given website.
- Uses **Google Gemini AI** (`gemini-pro`) to answer user queries based on the scraped content.
- Saves the extracted content into a text file (`scraped_content.txt`).

## Features
✅ **Scrapes text** from a webpage using **BeautifulSoup**  
✅ **Removes unnecessary elements** (scripts, styles)  
✅ **Breaks long content** into chunks for processing  
✅ **Uses Google Gemini AI** to generate answers  
✅ **Stores extracted content** in `scraped_content.txt`  

---

## Installation 🔧

### 1️⃣ **Clone the Repository**
```bash
git clone https://github.com/your-username/rag-project-test.git
cd rag-project-test

python -m venv env
source env/bin/activate  # macOS/Linux
env\Scripts\activate     # Windows

pip install -r requirements.txt

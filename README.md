## Description:
**Academic Research Web Crawler**
This is a simple web application that allows users to search for academic research papers on specific topics using DuckDuckGo search. It focuses on two primary sources — arXiv and Semantic Scholar — and extracts metadata such as the title and abstract from the results.
https://academic-web-crawler.onrender.com/

Users can:

- Enter a research topic

- Select which sources to include (arXiv, Semantic Scholar, or both)

- User can enter custom sources (like acm.org, IEEE)

- View the results directly in the browser

- The application is built using Flask and is deployed online using Render.

🚀 Features
🌐 Topic-based academic search via DuckDuckGo

📘 Scrapes arXiv and Semantic Scholar for research papers

✅ Source selection using checkboxes

⚙️ Easily extendable to include other domains (e.g., IEEE, ACM)

🔐 Secure deployment with environment variables

💡 Flash messaging for rate limit errors or invalid results


 **Technology**

 - Python 3.10+
 - Flask - Web framework
 - BeautifulSoup (bs4) - HTML parsing and scraping
 - Requests - HTTP client
 - duckduckgo_search - DuckDuckGo search API wrapper
 - python-dotenv - Managing environment variables
 - Render - Cloud deployment platform
 - .env - Local environment variable management

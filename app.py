from flask import Flask, render_template, request
from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup
from duckduckgo_search.exceptions import DuckDuckGoSearchException
from flask import flash
import os
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

def search_duckduckgo(topic, num_results = 15, domains = None):
    domains = domains or []
    site_filters = []
    for d in domains:
        if d == "arxiv":
            site_filters.append("site:arxiv.org")
        elif d == "semanticscholar":
            site_filters.append("site:semanticscholar.org")
        else:
            site_filters.append(f"site:{d}") 
    query = topic + " "+" OR ".join(site_filters)
    print(query)
    links = []
    try:
        with DDGS() as ddgs:
            results = ddgs.text(query, max_results = num_results)
            for r in results:
                url = r.get('href')
                if url:
                    links.append(url)
    except DuckDuckGoSearchException as e:
        print(f"Duckduckgo hit its limit!!!")
        return []

    return links

def extract_arxiv_data(url):
    response = requests.get(url)
    soup =  BeautifulSoup(response.text,'html.parser')
    title_tag = soup.find('h1', class_ = 'title')
    abstract_tag = soup.find("blockquote", class_ = 'abstract')

    title = title_tag.text.replace("Title:", "").strip() if title_tag else "No title found"
    abstract = abstract_tag.text.replace("Abstract:","").strip() if abstract_tag else "No abstract found"
    return {"title":title, "abstract":abstract, "url":url, "source":"arxiv"}

def extract_semantic_scholar_data(url):
    headers = {"User-Agent":"Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    title_tag = soup.find('h1')
    meta = soup.find('meta', {'name':'description'})

    title = title_tag.text.strip() if title_tag else "No title found"
    abstract = meta['content'].strip() if meta else "No abstract found"
    return {"title":title, "abstract":abstract, "url":url, "source": "semantic scholar"}

def extract_generic_page_data(url):
    headers = {"User-Agent":"Mozilla/5.0"}
    response = requests.get(url, headers=headers, timeout=10)
    soup = BeautifulSoup(response.text, 'html.parser')

    title_tag = soup.find("title")
    meta_desc = soup.find("meta", attrs={"name":"description"})

    title = title_tag.text.strip() if title_tag else "No title"
    abstract = meta_desc["content"].strip() if meta_desc else "No abstract found"
    return {"title": title, "abstract":abstract, "url": url, "sources":"custom"}

@app.route("/", methods = ["GET","POST"])
def index():
    results = []

    if request.method == "POST":
        topic = request.form.get("topic")
        selected_sources = request.form.getlist("sources") 
        custom_sources_raw = request.form.get("custom_sources", "").strip()
        custom_domains = [s.strip() for s in custom_sources_raw.split(",") if s.strip()]
        
        formatted_custom_sources = [d.replace("site:", "").strip() for d in custom_domains]


        all_sources = selected_sources + formatted_custom_sources

        if not all_sources:
            flash("Please select at least one source to search.", "warning")
            return render_template("index.html", results=[])

        if topic:
            links = search_duckduckgo(topic, num_results=15, domains=all_sources)

            if not links:
                flash("DuckDuckGo temporarily blocked the search (rate limit). Try again later.", "danger")
                return render_template("index.html", results=[])

            for link in links:
                try:
                    if "arxiv.org" in link and "arxiv" in selected_sources:
                        data = extract_arxiv_data(link)
                    elif "semanticscholar.org" in link and "semanticscholar" in selected_sources:
                        data = extract_semantic_scholar_data(link)
                    else:
                        data = extract_generic_page_data(link)
                    results.append(data)
                except Exception as e:
                    results.append({"title": "Error", "abstract": str(e), "url": link, "source": "Unknown"})

    return render_template("index.html", results=results)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=False, host="0.0.0.0", port=port)


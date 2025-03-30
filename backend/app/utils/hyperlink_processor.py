import re
import logging
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)

EDUCATIONAL_DOMAINS = [
    "khan academy", "khanacademy.org",
    "coursera", "coursera.org",
    "edx", "edx.org",
    "udemy", "udemy.com",
    "youtube", "youtube.com",
    "mit opencourseware", "ocw.mit.edu",
    "wikipedia", "wikipedia.org",
    "scholarpedia", "scholarpedia.org",
    "national geographic", "nationalgeographic.com",
    "ted", "ted.com",
    "nasa", "nasa.gov",
    "pbs", "pbs.org",
    "britannica", "britannica.com",
    "quizlet", "quizlet.com",
    "desmos", "desmos.com",
    "geogebra", "geogebra.org",
    "mathway", "mathway.com",
    "wolframalpha", "wolframalpha.com",
    "codecademy", "codecademy.com",
    "scratch", "scratch.mit.edu",
    "duolingo", "duolingo.com",
    "memrise", "memrise.com",
    "brainpop", "brainpop.com",
    "newsela", "newsela.com",
    "readworks", "readworks.org",
    "commonlit", "commonlit.org",
    "gutenberg", "gutenberg.org",
    "jstor", "jstor.org",
    "arxiv", "arxiv.org",
    "sciencedirect", "sciencedirect.com",
    "nature", "nature.com",
    "science", "science.org",
    "pnas", "pnas.org",
    "pubmed", "pubmed.ncbi.nlm.nih.gov",
    "google scholar", "scholar.google.com",
    "researchgate", "researchgate.net",
    "academia", "academia.edu",
]

URL_PATTERN = r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+'
RESOURCE_PATTERN = r'(?:^|\s)([A-Z][A-Za-z0-9\s]+(?:\.(?:com|org|edu|gov|net|io)))'
BOOK_PATTERN = r'"([^"]+)"(?:\s+by\s+([A-Z][A-Za-z\s]+))?'

def detect_urls(text: str) -> List[str]:
    """
    Detect URLs in text
    """
    return re.findall(URL_PATTERN, text)

def detect_educational_resources(text: str) -> List[Tuple[str, str]]:
    """
    Detect educational resources mentioned in text and generate appropriate URLs
    Returns a list of tuples (resource_name, url)
    """
    resources = []
    
    urls = detect_urls(text)
    for url in urls:
        resources.append((url, url))
    
    for domain_name, domain_url in zip(EDUCATIONAL_DOMAINS[::2], EDUCATIONAL_DOMAINS[1::2]):
        if domain_name.lower() in text.lower():
            pattern = re.compile(r'(?i)(?:^|\s)([^.!?]*?' + re.escape(domain_name) + r'[^.!?]*?(?:\.|\!|\?|$))')
            matches = pattern.findall(text)
            for match in matches:
                resource_name = match.strip()
                if domain_url not in resource_name:
                    if "http" not in resource_name:
                        resources.append((resource_name, f"https://{domain_url}"))
    
    books = re.findall(BOOK_PATTERN, text)
    for book in books:
        title = book[0]
        author = book[1] if len(book) > 1 and book[1] else ""
        search_query = f"{title} {author}".strip()
        url = f"https://www.google.com/search?q={search_query.replace(' ', '+')}"
        resources.append((f'"{title}"' + (f" by {author}" if author else ""), url))
    
    return resources

def process_text_for_hyperlinks(text: str) -> Dict:
    """
    Process text to identify potential hyperlinks and resources
    Returns a dictionary with the original text and a list of resources
    """
    resources = detect_educational_resources(text)
    
    unique_resources = []
    seen = set()
    for resource, url in resources:
        if resource.lower() not in seen:
            unique_resources.append((resource, url))
            seen.add(resource.lower())
    
    return {
        "text": text,
        "resources": unique_resources
    }

def enrich_content_with_hyperlinks(content: str) -> Dict:
    """
    Enrich content with hyperlinks and return both the original content and detected resources
    """
    try:
        return process_text_for_hyperlinks(content)
    except Exception as e:
        logger.error(f"Error processing hyperlinks: {e}")
        return {"text": content, "resources": []}

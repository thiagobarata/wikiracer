def to_url(linkSnippet):
    return "https://en.wikipedia.org/wiki/"+linkSnippet

def to_link_snippet(url):
    return url[30:] # removing https://en.wikipedia.org/wiki/

def remove_duplicates(links):
    unique_links = []
    seen = set()
    for link in links:
        if link not in seen:
            seen.add(link)
            unique_links.append(link)
    
    return unique_links
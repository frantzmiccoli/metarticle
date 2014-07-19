# -*- coding: utf-8 -*-
import httplib2
from BeautifulSoup import BeautifulSoup, SoupStrainer
from readability.readability import Document

def get_links(url):
    html = get_html(url)

    if html is None:
        return []

    links = []
    for extracted_link in BeautifulSoup(html, parseOnlyThese=SoupStrainer('a')):
        href = extracted_link.get('href')
        if href is None:
            continue

        has_blog = 'blog' in href
        has_cbs = 'cbinsight' in href
        slash_count_ok = href.count('/') > 3
        if (not has_blog) and (has_cbs or not slash_count_ok):
            # maybe not interesting
            continue
        links.append(href)

    return list(set(links))

def get_html(url):
    http = httplib2.Http()
    header, response = http.request(url)
    if header.status != 200:
        print 'Holy shit got a ' + header.status + ' for ' + url
        return

    return Document(response).summary()

def get_texts_from_url(url):
    links = get_links(url)
    print 'links found: ', len(links)
    links = links[0:30]

    texts = [get_html(link) for link in links]

    return texts

if __name__ == '__main__':
    url = 'http://www.cbinsights.com/blog/startup-failure-post-mortem'
    print get_links(url)
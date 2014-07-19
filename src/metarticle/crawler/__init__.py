# -*- coding: utf-8 -*-
import httplib2
from BeautifulSoup import BeautifulSoup, SoupStrainer
from readability.readability import Document

def get_links(url):
    http = httplib2.Http()
    status, response = http.request(url)

    links = []
    for link in BeautifulSoup(response, parseOnlyThese=SoupStrainer('a')):
        if link.has_attr('href'):
            href = link['href']
            has_blog = 'blog' in href
            has_cbs = 'cbsinsight' in href
            slash_count = href.count('/')
            if not has_blog and (has_cbs or slash_count < 3):
                # maybe not interesting
                continue
            links.append(href)

    return links

def get_text(url):
    http = httplib2.Http()
    status, response = http.request(url)
    if status != 200:
        print 'Holy shit got a ' + status + ' for ' + url
    return Document(response).summary()


def get_texts_from_url(url):
    links = get_links(url)
    print 'links found: ' + len(links)
    links = links[0:30]

    texts = [get_text(link) for link in links]

    return texts

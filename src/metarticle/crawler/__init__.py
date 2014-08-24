# -*- coding: utf-8 -*-
import httplib2
from BeautifulSoup import BeautifulSoup, SoupStrainer
from readability.readability import Document
import mlstripper
import hashlib
import os
import cacheutil

cache_dir_path = '../data/crawler'


def get_links(content_url):
    html = get_html(content_url)

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


def get_html(content_url):
    # TODO huge shit could come from this too generic try / except
    cached_status = get_status_from_cache(content_url)
    if cached_status:
        if cached_status != 200:
            return ''
        cached_html = get_html_from_cache(content_url)
        return cached_html
    (status, html) = get_status_and_html_from_network(content_url)
    store_status_in_cache(content_url, status)
    store_html_in_cache(content_url, html)
    return html


def get_status_and_html_from_network(content_url):
    try:
        http = httplib2.Http()
        header, response = http.request(content_url)
        if header.status != 200:
            print 'Holy shit got a ', header.status, ' for ', content_url
            return header.status, ''
        return header.status, Document(response).summary()
    except:
        return None, ''


def get_text(content_url):
    html = get_html(content_url)
    return mlstripper.strip_tags(html)


def get_texts_from_url(content_url):
    links = get_links(content_url)
    print 'links found: ', len(links)

    texts = [get_text(link) for link in links]

    return texts


'''Cache related'''
def get_status_from_cache(content_url):
    status_cache_file_path = get_status_cache_file_path(content_url)
    return cacheutil.get_from_cache(status_cache_file_path)


def get_html_from_cache(content_url):
    html_cache_file_path = get_html_cache_file_path(content_url)
    return cacheutil.get_from_cache(html_cache_file_path)


def get_status_cache_file_path(content_url):
    content_url_hash = hash_url(content_url)
    status_file_path = os.path.join(cache_dir_path, content_url_hash +
                                    '.status')
    return status_file_path


def get_html_cache_file_path(content_url):
    content_url_hash = hash_url(content_url)
    html_file_path = os.path.join(cache_dir_path, content_url_hash + '.html')
    return html_file_path


def store_status_in_cache(content_url, status):
    status_cache_file_path = get_status_cache_file_path(content_url)
    cacheutil.store_in_cache(status_cache_file_path, status)


def store_html_in_cache(content_url, html):
    html_cache_file_path = get_html_cache_file_path(content_url)
    cacheutil.store_in_cache(html_cache_file_path, html)


def hash_url(content_url):
    return hashlib.md5(content_url).hexdigest()


cacheutil.ensure_accessible_cache_dir(cache_dir_path)

if __name__ == '__main__':
    url = 'http://www.cbinsights.com/blog/startup-failure-post-mortem'
    print get_links(url)

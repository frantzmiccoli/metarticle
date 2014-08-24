# -*- coding: utf-8 -*-
from BeautifulSoup import BeautifulSoup, SoupStrainer
from .. import generic


def get_texts_from_url(content_url):
    links = get_links(content_url)
    print 'links found: ', len(links)

    texts = [generic.get_text(link) for link in links]

    return texts


def get_links(content_url):
    content = generic.get_content(content_url)

    if content is None:
        return []

    links = []
    for extracted_link in BeautifulSoup(content, parseOnlyThese=SoupStrainer('a')):
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




if __name__ == '__main__':
    url = 'http://www.cbinsights.com/blog/startup-failure-post-mortem'
    print get_links(url)

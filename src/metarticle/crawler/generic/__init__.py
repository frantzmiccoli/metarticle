import httplib2
from readability.readability import Document
from .. import mlstripper
import hashlib
import os
from ... import cacheutil

def get_content(content_url):
    # TODO huge shit could come from this too generic try / except
    cached_status = get_status_from_cache(content_url)
    if cached_status:
        if cached_status != 200:
            return ''
        cached_content = get_content_from_cache(content_url)
        return cached_content
    (status, content) = get_status_and_content_from_network(content_url)
    store_status_in_cache(content_url, status)
    store_content_in_cache(content_url, content)
    return content


def get_status_and_content_from_network(content_url):
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
    content = get_content(content_url)
    return mlstripper.strip_tags(content)


'''Cache related'''
def get_status_from_cache(content_url):
    status_cache_file_path = get_status_cache_file_path(content_url)
    return cacheutil.get_from_cache(status_cache_file_path)


def get_content_from_cache(content_url):
    content_cache_file_path = get_content_cache_file_path(content_url)
    return cacheutil.get_from_cache(content_cache_file_path)


def get_status_cache_file_path(content_url):
    content_url_hash = hash_url(content_url)
    status_file_path = os.path.join(cache_dir_path, content_url_hash +
                                    '.status')
    return status_file_path


def get_content_cache_file_path(content_url):
    content_url_hash = hash_url(content_url)
    content_file_path = os.path.join(cache_dir_path, content_url_hash + '.content')
    return content_file_path


def store_status_in_cache(content_url, status):
    status_cache_file_path = get_status_cache_file_path(content_url)
    cacheutil.store_in_cache(status_cache_file_path, status)


def store_content_in_cache(content_url, content):
    content_cache_file_path = get_content_cache_file_path(content_url)
    cacheutil.store_in_cache(content_cache_file_path, content)


def hash_url(content_url):
    return hashlib.md5(content_url).hexdigest()


cacheutil.ensure_accessible_cache_dir(cache_dir_path)
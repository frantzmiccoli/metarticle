# -*- coding: utf-8 -*-
import github
import web

def get_texts_from_url(root_url):
    if 'github.com/' in root_url:
        return github.get_texts_from_url(root_url)
    else:
        return web.get_texts_from_url(root_url)

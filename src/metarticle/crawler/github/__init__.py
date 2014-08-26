# -*- coding: utf-8 -*-
from metarticle.crawler import generic
import json
from BeautifulSoup import BeautifulSoup
import misaka


def get_texts_from_url(content_url):
    repo_names = get_repo_names(content_url)

    texts = []
    for repo_name in repo_names:
        text = get_text_for_repo(repo_name)
        if text:
            texts.append(text)

    return texts


def get_repo_names(content_url):
    """
    We assume this URL is a search URL.

    :param content_url:string
    :return:
    """
    json_response = generic.get_content(content_url)
    response = json.loads(json_response)

    repo_names = []
    for item in response['items']:
        repo_names.append(item['full_name'])

    return repo_names


def get_text_for_repo(repo_name):
    readme = get_readme_for_repo(repo_name)
    return extract_text_from_readme(readme)


def extract_text_from_readme(readme):
    if readme is None:
        return

    try:
        html = get_readme_html(readme)
        text = extract_text_from_readme_html(html)
        return text
    except:
        pass

    preserved_lines = []
    for line in readme.split("\n"):
        try:
            preserved_lines.append(line.decode('utf-8'))
        except:
            continue
    cleaned = "\n".join(preserved_lines)

    html = get_readme_html(cleaned)
    text = extract_text_from_readme_html(html)

    return text


def extract_text_from_readme_html(html):
    soup = BeautifulSoup(html)
    #we remove code nodes
    [s.extract() for s in soup('code')]
    [s.extract() for s in soup('pre')]
    text = ''.join(soup.findAll(text=True))
    return text


def get_readme_html(readme):
    readme = readme.replace('```js', '```')
    readme = readme.replace('```javascript', '```')
    readme = readme.replace('```JavaScript', '```')
    return misaka.html(readme)

def get_readme_for_repo(repo_name):
    banned_repos = ['bnoguchi/everyauth']#our parser fail to remove code on these ones

    if repo_name in banned_repos:
        return

    readme_url_patterns = [
        'https://raw.githubusercontent.com/%s/master/README.md',
        'https://raw.githubusercontent.com/%s/master/Readme.md',
        'https://raw.githubusercontent.com/%s/master/readme.md',
    ]

    for pattern in readme_url_patterns:
        readme_url = pattern % repo_name
        content = generic.get_content(readme_url)
        if content:
            return content

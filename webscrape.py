#!/usr/bin/env python

import sys
from lxml import html
from lxml.html.clean import clean_html



def content(url):
    """
    returns content or an empty string if invalid url
    """
    text = ''
    try:
        tree = html.parse(url)
        tree = clean_html(tree)
        text = tree.getroot().text_content()
    except IOError:
        pass
        #log
    return text


if __name__ == '__main__':
    print(content('ibm.com'))
    if len(sys.argv) > 1:
        print(content(sys.argv[1]))

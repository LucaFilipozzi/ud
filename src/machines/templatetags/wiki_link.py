import re

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def wiki_links(value):
    chunks = _split_texts_and_links(value)
    if len(chunks) == 1:
        result = _wiki_link(value)
    else:
        result = "".join([
            _wiki_link(chunk)
            for chunk
            in chunks
            if chunk])
    return result

def _split_texts_and_links(s):
    chunks = []
    current = []
    for chunk in re.split("(\]\])", s):
        if not current:
            current.append(chunk)
        if chunk == "]]":
            current.append(chunk)
            chunks.append("".join(current))
            current = []
    if current:
        chunks.extend(current)
    return chunks

def _wiki_link(value):
    regexp = re.compile(u"""(?P<before>[a-z- \.]*) # text before the link
            \[\[                                 # [[
            [-\*]?                                # sometimes url starts with a '*' or '-'
            (?P<link>[\w\- /|\.\(\)\&]+)          # url|text
            \]\]                                  # ]]
            (?P<after>.*)                         # text after the link
            """,
            flags=re.VERBOSE | re.UNICODE)
    m = regexp.match(value)
    if m:
        link = m.group("link").split("|")
        url = link[0]
        try:
            text = link[1]
        except IndexError:
            text = url
        urlized = ''.join([
            m.group("before"),
            '<a href="http://',
            url,
            '">',
            text,
            "</a>",
            m.group("after")
            ])
    else:
        urlized = value
    return urlized

register.filter('wiki_links', wiki_links)


import re

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def wiki_link(value):
    regexp = re.compile(r"""(?P<before>[a-z \.]*) # text before the link
            \[\[                                 # [[
            [-\*]?                                # sometimes url starts with a '*' or '-'
            (?P<link>[a-z0-9- |\.]+)              # url|text
            \]\]                                  # ]]
            (?P<after>.*)                         # text after the link
            """,
            re.VERBOSE)
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
            "<a href=",
            url,
            ">",
            text,
            "</a>",
            m.group("after")
            ])
    else:
        urlized = value
    return urlized

register.filter('wiki_link', wiki_link)


import re

from django import template
from django.template.defaultfilters import stringfilter, urlize

register = template.Library()

@register.filter
@stringfilter
def wiki_link(value):
    regexp = re.compile(r"""(?P<before>[a-z \.]*) # text before the url
            \[\[                                 # [[
            [-\*]?                                # sometimes url starts with a '*' or '-'
            (?P<url>[a-z0-9-\.]+)                 # url
            \]\]                                  # ]]
            (?P<after>.*)                         # text after the url
            """,
            re.VERBOSE)
    m = regexp.match(value)
    if m:
        urlized = ''.join([
            m.group("before"),
            urlize(m.group("url")),
            m.group("after")
            ])
    else:
        urlized = value
    return urlized

register.filter('wiki_link', wiki_link)


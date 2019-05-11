#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Antonio Feregrino'
SITENAME = 'That C# guy'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Europe/London'

DEFAULT_LANG = 'es'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

ARTICLE_URL = 'posts/{slug}/'
ARTICLE_SAVE_AS = 'posts/{slug}/index.html'

TAG_URL = 'tag/{slug}/'
TAG_SAVE_AS = 'tag/{slug}/index.html'

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

THEME = 'tcsg_theme'

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

MY_EMAIL = "antonio.feregrino@gmail.com"
MY_TWITTER_HANDLE = "io_exception"

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

PLUGIN_PATHS = ['./plugins']
PLUGINS = ['pelican_alias', 'tv_alias']



ALGOLIA_APP_ID = "2RZXM7KI15"
ALGOLIA_SEARCH_API_KEY = "ad630b2f2ffaa553017fc1c23209c06b"
ALGOLIA_ADMIN_API_KEY = "[YOUR ALGOLIA ADMIN API KEY]"
ALGOLIA_INDEX_NAME = 'demo-tcsg'

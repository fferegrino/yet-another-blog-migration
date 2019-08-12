# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import logging
import ntpath
import os.path
from urllib.parse import urlparse

from pelican import signals

logger = logging.getLogger(__name__)


class TvAliasGenerator(object):
    TEMPLATE = """<!DOCTYPE html><html><head><meta charset="utf-8" />
<meta http-equiv="refresh" content="0;url={destination}" />
</head></html>"""

    def __init__(self, context, settings, path, theme, output_path, *args):
        self.output_path = output_path
        self.context = context
        self.alias_delimiter = settings.get("ALIAS_DELIMITER", ",")

    def create_alias(self, page, alias):
        # If path starts with a /, remove it
        if alias[0] == "/":
            relative_alias = alias[1:]
        else:
            relative_alias = alias

        path = os.path.join(self.output_path, relative_alias)
        directory, filename = os.path.split(path)

        try:
            os.makedirs(directory)
        except OSError:
            pass

        if filename == "":
            path = os.path.join(path, "index.html")

        logger.info("[alias] Writing to alias file %s" % path)
        with open(path, "w") as fd:
            destination = page.url
            # if schema is empty then we are working with a local path
            if not urlparse(destination).scheme:
                # if local path is missing a leading slash then add it
                if not destination.startswith("/"):
                    destination = "/{0}".format(destination)
            fd.write(self.TEMPLATE.format(destination=destination))

    def generate_output(self, writer):
        pages = self.context["articles"]

        for page in pages:
            featured_tag = page.metadata.get("featured_tag", "").lower()
            if featured_tag == "tv":

                filename = ntpath.basename(page.source_path)
                page_slug = filename[11:-3]

                aliases = ["tv/{slug}/"]

                for alias_template in aliases:
                    alias = alias_template.format(slug=page_slug)
                    logger.info("[tv_alias] Processing tv alias %s" % alias)
                    self.create_alias(page, alias)


def get_generators(generators):
    return TvAliasGenerator


def register():
    signals.get_generators.connect(get_generators)

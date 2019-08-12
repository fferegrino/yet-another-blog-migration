import hashlib
import logging

from algoliasearch.search_client import SearchClient
from bs4 import BeautifulSoup
from pelican import signals
from pelican.settings import DEFAULT_CONFIG

logger = logging.getLogger(__name__)


# __all__ = ['register']


def set_default_settings(settings):
    settings.setdefault("ALGOLIA_APP_ID", None)
    settings.setdefault("ALGOLIA_SEARCH_API_KEY", None)
    settings.setdefault("ALGOLIA_ADMIN_API_KEY", None)
    settings.setdefault("ALGOLIA_INDEX_NAME", "blog")


def init_default_config(pelican):
    set_default_settings(DEFAULT_CONFIG)
    if pelican:
        set_default_settings(pelican.settings)


def convert_article(page):
    soup_title = BeautifulSoup(page.title.replace("&nbsp;", " "), "html.parser")
    page_title = (
        soup_title.get_text(" ", strip=True)
        .replace("“", '"')
        .replace("”", '"')
        .replace("’", "'")
        .replace("^", "&#94;")
    )

    soup_text = BeautifulSoup(page.content, "html.parser")
    page_text = (
        soup_text.get_text(" ", strip=True)
        .replace("“", '"')
        .replace("”", '"')
        .replace("’", "'")
        .replace("¶", " ")
        .replace("^", "&#94;")
    )
    page_text = " ".join(page_text.split())

    soup_summary = BeautifulSoup(page.excerpt, "html.parser")
    page_summary = (
        soup_summary.get_text(" ", strip=True)
        .replace("“", '"')
        .replace("”", '"')
        .replace("’", "'")
        .replace("¶", " ")
        .replace("^", "&#94;")
    )

    if getattr(page, "category", "None") == "None":
        page_category = ""
    else:
        page_category = page.category.name

    page_url = page.url

    tags = [t.name for t in getattr(page, "tags", [])]

    page_created = page.date
    page_modified = getattr(page, "modified", None)
    page_date = page_created

    objectId = hashlib.sha256(str(page.slug).encode("utf-8")).hexdigest()

    object_to_index = {
        "objectID": objectId,
        "slug": page.slug,
        "date": page_date.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "created": page_created.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "title": page_title,
        "category": page_category,
        "content": page_text,
        "summary": page_summary,
        "tags": tags,
        "url": page_url,
    }

    if page_modified:
        object_to_index["date"] = page_modified
        object_to_index["modified"] = page_modified

    return object_to_index


def index_generator(generator):
    index_name = generator.settings.get("ALGOLIA_INDEX_NAME", None)
    app_id = generator.settings.get("ALGOLIA_APP_ID", None)
    admin_api_key = generator.settings.get("ALGOLIA_ADMIN_API_KEY", None)

    if None in [index_name, app_id, admin_api_key]:
        logger.error("Algolia Indexe - settings error")
        return

    logger.info(
        "Generating Algolia index '%s' for %d articles..."
        % (index_name, len(generator.articles))
    )

    client = SearchClient.create(app_id, admin_api_key)
    index = client.init_index(index_name)

    common_settings = {
        "maxFacetHits": 20,
        "attributesToRetrieve": [
            "title",
            "summary",
            "content",
            "url",
            "created",
            "modified",
            "tags",
        ],
        "attributesToHighlight": ["title", "summary"],
        "searchableAttributes": ["title", "summary", "content"],
        "attributesForFaceting": ["tags"],
    }

    settings = common_settings.copy()

    # settings.update({
    #    "replicas": [
    #        "blog_created_asc",
    #        "blog_title_asc",
    #    ],
    #    "ranking": [
    #        "desc(created)",
    #    ]
    # })
    # index.set_settings(settings)

    # blog_created_asc = client.init_index("blog_created_asc")
    # settings = common_settings.copy()
    # settings.update({
    #    "ranking": [
    #        "asc(created)",
    #    ]
    # })
    # blog_created_asc.set_settings(settings)

    # blog_title_asc = client.init_index("blog_title_asc")
    # settings = common_settings.copy()
    # settings.update({
    #    "ranking": [
    #        "asc(title)",
    #    ]
    # })
    # blog_title_asc.set_settings(settings)

    exists = []

    for article in generator.articles:
        try:
            logger.info("Indexing article: '%s'" % article.title)
            data = convert_article(article)
            exists.append(data["objectID"])
            index.save_object(data)
        except Exception as err:
            logger.error(err)

    logger.info("Purge old Algolia objects")
    for_delete = []
    res = index.browse_objects()
    for hit in res:
        if not hit["objectID"] in exists:
            for_delete.append(hit["objectID"])
            logger.debug("Delete old article[%s]" % hit["title"])

    if for_delete:
        _ = index.delete_objects(for_delete)


def register():
    """Plugin registration."""
    signals.initialized.connect(init_default_config)
    signals.article_generator_finalized.connect(index_generator)

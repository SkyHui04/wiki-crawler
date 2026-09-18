from app.types.wiki_objects import (
    WikiArticleLink,
    WikiArticle,
)
from bs4 import BeautifulSoup


def extract_article(raw_text: str) -> WikiArticle:
    soup = BeautifulSoup(raw_text, "html.parser")
    if soup.title is None:
        title = ""
    else:
        title_suffic = " - Wikipedia"
        title = (
            soup.title.text[: -len(title_suffic)]
            if soup.title.text.endswith(title_suffic)
            else soup.title.text
        )

    section_tags = soup.find_all(
        lambda tag: tag.has_attr("data-mw-section-id"),
        recursive=True,
        limit=256,
    )
    all_links = []

    for section_tag in section_tags:
        section_title: str = str(section_tag.get("aria-labelledby", ""))
        section_paragraphs = section_tag.find_all("p")
        for paragraph in section_paragraphs:
            section_links = paragraph.find_all(
                lambda tag: tag.name == "a" and "mw:WikiLink" in (tag.get("rel") or []),
                recursive=True,
            )
            all_links += [
                WikiArticleLink(
                    from_title=title,
                    prompt=link.get_text(),
                    link=str(link.get("href")),
                    located_section=section_title,
                )
                for link in section_links
            ]

    return WikiArticle(title=title, all_links=all_links)

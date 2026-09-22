import re

from pydantic import BaseModel, computed_field

IGNORE_SECTIONS = ("See_also", "Notes", "References", "External_links")


class WikiArticleLink(BaseModel):
    from_title: str
    prompt: str
    link: str
    located_section: str

    def reject(self) -> bool:
        if not re.match(
            r"^https?://en.wikipedia.org/wiki/[a-zA-Z0-9\-._~%!$&'()*+,;=:@]+$",
            self.link,
        ):
            return True

        return bool(
            re.match(
                r"^https?://en.wikipedia.org/wiki/Help:[a-zA-Z0-9\-._~%!$&'()*+,;=:@\/]+$",
                self.link,
            )
        )


class WikiArticle(BaseModel):
    title: str
    all_links: list[WikiArticleLink]

    @computed_field
    @property
    def content_links(self) -> list[WikiArticleLink]:
        return [
            link
            for link in self.all_links
            if link not in IGNORE_SECTIONS and not link.reject()
        ]

    @computed_field
    @property
    def head_link(self) -> WikiArticleLink | None:
        content_links = self.content_links
        if content_links:
            return content_links[0]
        else:
            return None

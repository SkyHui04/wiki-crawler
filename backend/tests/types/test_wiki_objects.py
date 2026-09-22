import pytest
from app.types.wiki_objects import WikiArticleLink


@pytest.mark.parametrize(
    "link, reject",
    [
        ("https://en.wikipedia.org/wiki/Terminology", False),
        ("http://en.wikipedia.org/wiki/Terminology", False),
        ("http://en.wikipedia.org/wiki/ Terminology", True),
        (" http://en.wikipedia.org/wiki/Terminology", True),
        ("http://en.wikipedia.org/wiki/Terminology ", True),
        ("http://en.wikipedia.org/wiki/", True),
        ("https://zh.wikipedia.org/wiki/%E6%97%A5%E8%AA%9E%E6%95%AC%E8%AA%9E", True),
        ("https://en.wikipedia.org/wiki/Help:Pronunciation_respelling_key", True),
        ("https://en.wikipedia.org/wiki/Help:IPA/English", True),
    ],
)
def test_wiki_link_reject(link: str, reject: bool):
    link_obj = WikiArticleLink(from_title="", prompt="", link=link, located_section="")

    assert link_obj.reject() == reject

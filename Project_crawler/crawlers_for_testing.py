from Project_crawler.crawler import Purumpurum


class BrokenLinksInternalCrawler(Purumpurum):
    name = 'testcrawler'
    start_urls = ["https://crawler-test.com/links/broken_links_internal"]


class BrokenLinksExternalCrawler(Purumpurum):
    name = 'testcrawler'
    start_urls = ["https://crawler-test.com/links/broken_links_external"]


class MaxExternalLinksCrawler(Purumpurum):
    name = 'testcrawler'
    start_urls = ["https://crawler-test.com/links/max_external_links"]


class RepeatedExternalLinksCrawler(Purumpurum):
    name = 'testcrawler'
    start_urls = ["https://crawler-test.com/links/page_with_external_links"]


class RepeatedInternalLinksCrawler(Purumpurum):
    name = 'testcrawler'
    start_urls = ["https://crawler-test.com/links/repeated_internal_links"]


class ExternalLinksToDisallowedCrawler(Purumpurum):
    name = 'testcrawler'
    start_urls = \
        ["https://crawler-test.com/links/external_links_to_disallwed_urls"]


class NonStandardLinksCrawler(Purumpurum):
    name = 'testcrawler'
    start_urls = ["https://crawler-test.com/links/non_standard_links"]


class WhitespaceInLinksCrawler(Purumpurum):
    name = 'testcrawler'
    start_urls = ["https://crawler-test.com/links/whitespace_in_links"]


class DoubleSlashDisallowedStartCrawler(Purumpurum):
    name = 'testcrawler'
    start_urls = \
        ["https://crawler-test.com//urls/double_slash/disallowed_start"]


class DoubleSlashDisallowedMiddleCrawler(Purumpurum):
    name = 'testcrawler'
    start_urls = \
        ["https://crawler-test.com//urls/double_slash//disallowed_middle"]


class DoubleSlashDisallowedEndCrawler(Purumpurum):
    name = 'testcrawler'
    start_urls = \
        ["https://crawler-test.com//urls/double_slash/disallowed_end//"]


class HTTPNonWWWCrawler(Purumpurum):
    name = 'testcrawler'
    start_urls = ["http://crawler-test.com/"]


class HTTPCrawler(Purumpurum):
    name = 'testcrawler'
    start_urls = ["http://www.crawler-test.com/"]


class HTTPSCrawler(Purumpurum):
    name = 'testcrawler'
    start_urls = ["https://crawler-test.com/"]


class NonHeadTagInsideHeadTagCrawler(Purumpurum):
    name = 'testcrawler'
    start_urls = ["http://crawler-test.com/other/non_head_tag_in_head"]


class InfiniteRedirectCrawler(Purumpurum):
    name = 'testcrawler'
    start_urls = ["http://crawler-test.com/redirects/infinite_redirect"]


class URLWithForeignCharactersCrawler(Purumpurum):
    name = 'testcrawler'
    start_urls = \
        ["http://crawler-test.com/encoding/url_with_foreign_characters/"
         "すべての単語が高校程度の辞書に載っている"]


class ForeignCharacterDomainCrawler(Purumpurum):
    name = 'testcrawler'
    start_urls = ["http://www.søkbar.no/"]
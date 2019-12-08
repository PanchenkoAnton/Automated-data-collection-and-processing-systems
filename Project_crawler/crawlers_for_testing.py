from Project_crawler.crawler import Purumpurum


class BrokenLinksInternalCrawler(Purumpurum):
    allowed_domains = ["crawler-test"]
    name = 'testcrawler'
    start_urls = ["https://crawler-test.com/links/broken_links_internal"]


class BrokenLinksExternalCrawler(Purumpurum):
    allowed_domains = ["crawler-test"]
    name = 'testcrawler'
    start_urls = ["https://crawler-test.com/links/broken_links_external"]


class MaxExternalLinksCrawler(Purumpurum):
    allowed_domains = ["crawler-test"]
    name = 'testcrawler'
    start_urls = ["https://crawler-test.com/links/max_external_links"]


class SubdomainCrawler(Purumpurum):
    allowed_domains = ["crawler-test"]
    name = 'testcrawler'
    start_urls = ["https://subdomain.crawler-test.com"]


class RepeatedExternalLinksCrawler(Purumpurum):
    allowed_domains = ["crawler-test"]
    name = 'testcrawler'
    start_urls = ["https://crawler-test.com/links/page_with_external_links"]


class RepeatedInternalLinksCrawler(Purumpurum):
    allowed_domains = ["crawler-test"]
    name = 'testcrawler'
    start_urls = ["https://crawler-test.com/links/repeated_internal_links"]


class ExternalLinksToDisallowedCrawler(Purumpurum):
    allowed_domains = ["crawler-test"]
    name = 'testcrawler'
    start_urls = \
        ["https://crawler-test.com/links/external_links_to_disallwed_urls"]


class NonStandardLinksCrawler(Purumpurum):
    allowed_domains = ["crawler-test"]
    name = 'testcrawler'
    start_urls = ["https://crawler-test.com/links/non_standard_links"]


class WhitespaceInLinksCrawler(Purumpurum):
    allowed_domains = ["crawler-test"]
    name = 'testcrawler'
    start_urls = ["https://crawler-test.com/links/whitespace_in_links"]


class DoubleSlashDisallowedStartCrawler(Purumpurum):
    allowed_domains = ["crawler-test"]
    name = 'testcrawler'
    start_urls = \
        ["https://crawler-test.com//urls/double_slash/disallowed_start"]


class DoubleSlashDisallowedMiddleCrawler(Purumpurum):
    allowed_domains = ["crawler-test"]
    name = 'testcrawler'
    start_urls = \
        ["https://crawler-test.com//urls/double_slash//disallowed_middle"]


class DoubleSlashDisallowedEndCrawler(Purumpurum):
    allowed_domains = ["crawler-test"]
    name = 'testcrawler'
    start_urls = \
        ["https://crawler-test.com//urls/double_slash/disallowed_end//"]


class HTTPNonWWWCrawler(Purumpurum):
    allowed_domains = ["crawler-test"]
    name = 'testcrawler'
    start_urls = ["http://crawler-test.com/"]


class HTTPCrawler(Purumpurum):
    allowed_domains = ["crawler-test"]
    name = 'testcrawler'
    start_urls = ["http://www.crawler-test.com/"]


class HTTPSCrawler(Purumpurum):
    allowed_domains = ["crawler-test"]
    name = 'testcrawler'
    start_urls = ["https://crawler-test.com/"]


class NonHeadTagInsideHeadTagCrawler(Purumpurum):
    allowed_domains = ["crawler-test"]
    name = 'testcrawler'
    start_urls = ["http://crawler-test.com/other/non_head_tag_in_head"]


class InfiniteRedirectCrawler(Purumpurum):
    allowed_domains = ["crawler-test"]
    name = 'testcrawler'
    start_urls = ["http://crawler-test.com/redirects/infinite_redirect"]


class URLWithForeignCharactersCrawler(Purumpurum):
    allowed_domains = ["crawler-test"]
    name = 'testcrawler'
    start_urls = \
        ["http://crawler-test.com/encoding/url_with_foreign_characters/"
         "すべての単語が高校程度の辞書に載っている"]


class ForeignCharacterDomainCrawler(Purumpurum):
    allowed_domains = ["crawler-test"]
    name = 'testcrawler'
    start_urls = ["http://www.søkbar.no/"]


class BasicsSinglePageCrawler(Purumpurum):
    name = 'testcrawler'
    start_urls = ["Case1/first.html"]
    allowed_domains = []


class BasicsTwoPagesCrawler(Purumpurum):
    name = 'testcrawler'
    start_urls = ["Case2/first.html"]
    allowed_domains = []


class BasicsManyPagesCrawler(Purumpurum):
    name = 'testcrawler'
    start_urls = ["Case3/first.html"]
    allowed_domains = []


class BasicsLoopPagesCrawler(Purumpurum):
    name = 'testcrawler'
    start_urls = ["Case4/first.html"]
    allowed_domains = []

import asyncio

import tldextract
from motor.motor_asyncio import AsyncIOMotorClient


class GlobalCrawlerStats:

    def __init__(self, name, db_host='localhost', db_port=27017):
        self.db = AsyncIOMotorClient(db_host, db_port)['crawler']

        self.name = name

        self.internal_urls = set()

        self.external_urls = set()

        self.subdomains_urls = set()

        self.files_urls = set()

        self.loop = asyncio.get_event_loop()

        self.stats = {"count": 0, "statuses": {str(200): [0]}}

    def get_domain(self, link):
        return tldextract.extract(link).domain

    def compare_domains(self, link1, link2):
        return self.get_domain(link1) == self.get_domain(link2)

    async def insert(self, collection, document):
        return await collection.insert_one(dict(document))

    def write_to_db(self):
        asyncio.set_event_loop(asyncio.new_event_loop())
        self.stats['statuses'].pop('200')
        self.loop.run_until_complete(self.insert(
            self.db['Unique links'],
            {"name": self.name,
             "external_urls": list(self.external_urls),
             "subdomains_urls": list(self.subdomains_urls),
             "files_urls": list(self.files_urls),
             "code_stats": dict((k, [i for i in v[1]]) for k, v in self.stats['statuses'].items())}
        ))
        self.loop.close()

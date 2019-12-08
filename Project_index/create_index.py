import asyncio

from motor.motor_asyncio import AsyncIOMotorClient

from Project_parser.parsers.HTMLParser import HTMLParser


async def do_find_one():
    db = AsyncIOMotorClient('localhost', 27000)['crawler']
    collection_msu = db.msu
    document = await collection_msu.find_one({"url": "https://www.msu.ru/"})
    #print(document['data'])
    parser = HTMLParser(text=document['data'])
    text = parser.get_text()
    # data = HTMLParser.get_text(text=document['data'])
    # soup = BeautifulSoup(document['data'])
    # data = soup.findAll(text=True)
    print(text)
    return text


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(do_find_one())

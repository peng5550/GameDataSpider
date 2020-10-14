import aiohttp
import asyncio

class GameCrawler:

    def __init__(self):
        pass

    async def __crawler(self, semaphore, link):
        async with semaphore:
            conn = aiohttp.TCPConnector(verify_ssl=False)
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Accept-Language': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
            }
            async with aiohttp.ClientSession(connector=conn, headers=headers) as session:
                try:
                    async with await session.get(link) as resp:
                        content = await resp.text()
                        return content
                except Exception as e:
                    print(e.args)

    async def taskManager(self, urlList, func):
        tasks = []
        semaphore = asyncio.Semaphore(5)
        for data in urlList:
            task = asyncio.ensure_future(func(semaphore, *data))
            tasks.append(task)

        await asyncio.wait(tasks)

    def start(self):
        urlList = []
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.taskManager(urlList, self.__crawler))

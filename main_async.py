import asyncio
import httpx
import tqdm


async def download_files(url: str, filename: str):
    with open(filename, 'wb') as f:
        async with httpx.AsyncClient() as client:
            async with client.stream('GET', url) as r:
                r.raise_for_status()
                total = int(r.headers.get('Content-Length'))

                tqdm_params = {
                    'desc': url,
                    'total': total,
                    'miniters': 1,
                    'unit': 'bit',
                    'unit_scale': True,
                    'unit_divisor': 1024,
                }

                with tqdm.tqdm(**tqdm_params) as pb:
                    async for chunk in r.aiter_bytes():
                        pb.update(len(chunk))
                        f.write(chunk)


async def main():

    loop = asyncio.get_running_loop()

    urls = [
        ('https://file.zip', '1.zip'),
        ('https://file.zip', '2.zip'),
    ]

    tasks = [loop.create_task(download_files(url, filename)) for url, filename in urls]
    await asyncio.gather(*tasks, return_exceptions=True)

if __name__ == '__main__':
    asyncio.run(main())

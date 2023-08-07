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

    # urls = [
    #     'https://github.com/toxidxd/face_detection/archive/refs/heads/main.zip',
    #     'https://github.com/toxidxd/sb_module9_toixdxd/archive/refs/heads/main.zip',
    #     'https://github.com/toxidxd/eve_fw_profit/archive/refs/heads/master.zip',
    #     'https://github.com/toxidxd/sb_python_messenger/archive/refs/heads/main.zip',
    #     'https://github.com/toxidxd/sb_MyProfile_project_toxidxd/archive/refs/heads/main.zip',
    #     'https://github.com/toxidxd/py_learn/archive/refs/heads/main.zip'
    # ]

    urls = [
        # ('https://github.com/toxidxd/face_detection/archive/refs/heads/main.zip', '50MB.zip'),
        # ('https://github.com/toxidxd/py_learn/archive/refs/heads/main.zip', '200MB.zip'),
        ('https://github.com/toxidxd/sb_python_messenger/archive/refs/heads/main.zip', '20MB.zip'),
    ]

    # tasks = [loop.create_task(download_files(url=url, filename=url.split('/')[-1])) for url in urls]
    tasks = [loop.create_task(download_files(url, filename)) for url, filename in urls]
    await asyncio.gather(*tasks, return_exceptions=True)

if __name__ == '__main__':
    asyncio.run(main())

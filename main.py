import requests
import tqdm


def download_files(url: str, filename: str):
    with open(filename, 'wb') as f:
        with requests.get(url, stream=True) as r:
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
                for chunk in r.iter_content(chunk_size=8192):
                    pb.update(len(chunk))
                    f.write(chunk)


def main():
    url = 'https://github.com/toxidxd/face_detection/archive/refs/heads/main.zip'
    filename = url.split('/')[-1]
    download_files(url, filename)


if __name__ == '__main__':
    main()

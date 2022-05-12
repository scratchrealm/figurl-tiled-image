import os
import pyvips
import urllib.request
from figurl_tiled_image import TiledImage
import kachery_cloud as kcl


def main():
    image_url = 'https://www.nesdis.noaa.gov/s3dl?path=/s3/2022-05/geocolor_20220505180018_logos.png'
    tile_size = 1024

    with kcl.TemporaryDirectory() as tmpdir:
        tmp_fname = tmpdir + '/' + os.path.basename(image_url)
        print(f'Downloading image {image_url}')
        _download_image(image_url, tmp_fname)
        image = pyvips.Image.new_from_file(tmp_fname)
    
        print('Creating TiledImage figURL')
        X = TiledImage(image, tile_size=tile_size)
        url = X.url(label='Earth - tiled image example')
        print(url)

    # Output on 5/12/22
    # https://figurl.org/f?v=gs://figurl/tiled-image-1&d=ipfs://bafkreidde4hrwsoh44dzntxm4sl3n7vccksd74pzcmnu5fgqhwtpy3zpxq&label=Earth%20-%20tiled%20image%20example

def _download_image(url: str, fname: str):
    urllib.request.urlretrieve(url, fname)

if __name__ == '__main__':
    main()
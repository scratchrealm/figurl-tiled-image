# figurl-tiled-image

View a tiled image using deck.gl.

This project uses [kachery-cloud](https://github.com/scratchrealm/kachery-cloud) and [figurl](https://github.com/scratchrealm/figurl2).

> **IMPORTANT**: This package is intended for collaborative sharing of data for scientific research. It should not be used for other purposes.

## Installation and setup

It is recommended that you use a conda environment with Python >= 3.8 and numpy.

```bash
# clone this repo
git clone https://github.com/scratchrealm/figurl-tiled-image

cd figurl-tiled-image
pip install -e .
```

Configure your [kachery-cloud](https://github.com/scratchrealm/kachery-cloud) client

```bash
kachery-cloud-init
# follow the instructions to associate your client with your Google user name on kachery-cloud
```

## Basic usage

```python
import numpy as np
from figurl_tiled_image import TiledImage

array = ... # create a color image numpy array [N1 x N2 x 3] uint8

X = TiledImage(array, tile_size=512)
url = X.url(label='Example')
print(url)
```

## Example - Mandelbrot set

See [examples/mandelbrot.py](examples/mandelbrot.py) and [examples/mini_mandelbrot.py](examples/mini_mandelbrot.py)

```python
import numpy as np
import matplotlib.pyplot as plt
from figurl_tiled_image import TiledImage

print('Creating Mandelbrot array')
width = 5000
height = 4000
max_iterations = 100
tile_size = 512
x = mandelbrot(height, width, max_iterations=max_iterations, zoom=1.3)
x = x.astype(np.float32) / max_iterations
x[x>1] = 1

print('Converting to color map uint8')
RdGy = plt.get_cmap('RdGy')
y = np.flip((RdGy(x)[:,:,:3]*255).astype(np.uint8), axis=0) # colorize and convert to uint8

print('Creating TiledImage figURL')
X = TiledImage(y, tile_size=tile_size)
url = X.url(label='Mandelbrot tiled image')
print(url)

# https://figurl.org/f?v=gs://figurl/tiled-image-1&d=ipfs://bafkreihcn72fhpebdujz5dj7bkmsrn3cydrl73y6gnwawtk5by4jmnsv4e&label=Mandelbrot%20tiled%20image
```

[View resulting figURL - Mandelbrot set](https://figurl.org/f?v=gs://figurl/tiled-image-1&d=ipfs://bafkreihcn72fhpebdujz5dj7bkmsrn3cydrl73y6gnwawtk5by4jmnsv4e&label=Mandelbrot%20tiled%20image)

## For developers

The front-end code is found in the [gui/](gui/) directory. It uses typescript/react and is deployed as a [figurl](https://github.com/scratchrealm/figurl2) visualization plugin.

You can run a local development version of this via:

```bash
cd gui
# One-time install
yarn install 

# Start the web server
yarn start
```

Then replace `v=gs://figurl/tiled-image-1` by `http://localhost:3000` in the URL you are viewing.

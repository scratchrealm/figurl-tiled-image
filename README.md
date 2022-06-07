# figurl-tiled-image

View a stack of tiled images using deck.gl.

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

Configure your [kachery-cloud](https://github.com/scratchrealm/kachery-cloud) client (only do this once on your computer)

```bash
kachery-cloud-init
# follow the instructions to associate your client with your Google user name on kachery-cloud
```

## Basic usage

From Numpy array:

```python
import numpy as np
from figurl_tiled_image import TiledImage

array = ... # create a color image numpy array [N1 x N2 x 3] uint8

X = TiledImage(tile_size=4096)
X.add_layer('layer1', array)
url = X.url(label='Numpy example')
print(url)
```

From image file:

```python
import pyvips
from figurl_tiled_image import TiledImage

filename = '/path/to/some/image.png' # substitute the path to your image
image = pyvips.new_from_file(filename)

X = TiledImage(tile_size=4096)
X.add_layer('layer1', image)
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
tile_size = 4096
x = mandelbrot(height, width, max_iterations=max_iterations, zoom=1.3)
x = x.astype(np.float32) / max_iterations
x[x>1] = 1

print('Converting to color map uint8')
RdGy = plt.get_cmap('RdGy')
y = np.flip((RdGy(x)[:,:,:3]*255).astype(np.uint8), axis=0) # colorize and convert to uint8

print('Creating TiledImage figURL')
X = TiledImage(tile_size=tile_size)
X.add_layer('mandelbrot', y)
url = X.url(label='Mandelbrot image')
print(url)
```

[View resulting figURL - Mandelbrot set](...)

## Example - High res. earth from NASA and NOAA

See [examples/high_res_earth_from_url.py](examples/high_res_earth_from_url.py)

[View resulting figURL - Earth](...)

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

Then replace `v=gs://figurl/figurl-tiled-image-2` by `v=http://localhost:3000` in the URL you are viewing. Updates to the source code will live-update the view in the browser. If you improve the visualization, please contribute by creating a PR.

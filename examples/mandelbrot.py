import numpy as np
import matplotlib.pyplot as plt
from figurl_tiled_image import TiledImage

def main():
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

    # Output on 5/11/22
    # https://figurl.org/f?v=gs://figurl/tiled-image-1&d=ipfs://bafkreihcn72fhpebdujz5dj7bkmsrn3cydrl73y6gnwawtk5by4jmnsv4e&label=Mandelbrot%20tiled%20image

# Thanks: https://www.learnpythonwithrune.org/numpy-compute-mandelbrot-set-by-vectorization/
def mandelbrot(height, width, x=-0.5, y=0, zoom=1, max_iterations=100):
    # To make navigation easier we calculate these values
    x_width = 1.5
    y_height = 1.5 * height / width
    x_from = x - x_width / zoom
    x_to = x + x_width / zoom
    y_from = y - y_height / zoom
    y_to = y + y_height / zoom
    # Here the actual algorithm starts
    x = np.linspace(x_from, x_to, width).reshape((1, width))
    y = np.linspace(y_from, y_to, height).reshape((height, 1))
    c = x + 1j * y
    # Initialize z to all zero
    z = np.zeros(c.shape, dtype=np.complex128)
    # To keep track in which iteration the point diverged
    div_time = np.zeros(z.shape, dtype=int)
    # To keep track on which points did not converge so far
    m = np.full(c.shape, True, dtype=bool)
    for i in range(max_iterations):
        z[m] = z[m]**2 + c[m]
        diverged = np.greater(np.abs(z), 2, out=np.full(c.shape, False), where=m) # Find diverging
        div_time[diverged] = i      # set the value of the diverged iteration number
        m[np.abs(z) > 2] = False    # to remember which have diverged
    return div_time

if __name__ == '__main__':
    main()
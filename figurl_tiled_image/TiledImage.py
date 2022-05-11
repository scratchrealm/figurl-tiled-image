import os
import numpy as np
import pyvips
import kachery_cloud as kcl
import figurl as fig


class TiledImage:
    def __init__(self, data: np.array, *, tile_size: int) -> None:
        assert data.dtype == np.uint8, 'Data must be of type uint8'
        self._data = data
        self._tile_size = tile_size
    def url(self, *, label: str):
        image: pyvips.Image = pyvips.Image.new_from_array(self._data)
        with kcl.TemporaryDirectory() as tmpdir:
            image.dzsave(f'{tmpdir}/output',
                overlap=0, 
                tile_size=self._tile_size, 
                layout=pyvips.enums.ForeignDzLayout.DZ
            )
            output_dirname = f'{tmpdir}/output_files'
            image_files = {}
            z = 1
            while True:
                dirname = f'{output_dirname}/{z}'
                if not os.path.exists(dirname):
                    break
                num_zoom_levels = z
                j = 0
                while True:
                    if not os.path.exists(f'{dirname}/{j}_0.jpeg'):
                        break
                    k = 0
                    while True:
                        fname = f'{dirname}/{j}_{k}.jpeg'
                        if not os.path.exists(fname):
                            break
                        print(f'Storing file: {fname}')
                        uri = kcl.store_file(fname, label=f'{z}_{j}_{k}.jpeg')
                        image_files[f'{z}_{j}_{k}'] = uri
                        k = k + 1
                    j = j + 1
                z = z + 1
            data = {
                'tileSize': self._tile_size,
                'width': self._data.shape[1],
                'height': self._data.shape[0],
                'numZoomLevels': num_zoom_levels,
                'imageFiles': image_files
            }
            F = fig.Figure(
                view_url='gs://figurl/tiled-image-1',
                data=data
            )
            url = F.url(label=label)
            return url
import { TileLayer } from '@deck.gl/geo-layers';
import { BitmapLayer } from '@deck.gl/layers';
import DeckGL from '@deck.gl/react';
import { load } from '@loaders.gl/core';
import {ImageLoader} from '@loaders.gl/images'
import { clamp } from '@math.gl/core';
import { COORDINATE_SYSTEM, OrthographicView } from 'deck.gl';
import React, { FunctionComponent, useMemo } from 'react';
import { getFileDataUrl } from '../../figurl/getFileData';


export interface DeckGlTileLayerProps {
    tileSize: number
    imageWidth: number
    imageHeight: number
    numZoomLevels: number
    imageFiles: {[key: string]: string}
}

// const ROOT_URL =
//   'https://raw.githubusercontent.com/visgl/deck.gl-data/master/website/image-tiles/moon.image';


const autoHighlight = true

const onTilesLoad = () => {}

const DeckGlTileLayer: FunctionComponent<DeckGlTileLayerProps> = ({tileSize, imageWidth, imageHeight, imageFiles, numZoomLevels}) => {
    const minZoom = -Math.floor(Math.min(numZoomLevels - 1, (Math.log2(Math.max(imageWidth, imageHeight)) - 8)))
    const initialViewState = useMemo(() => ({
        target: [imageWidth / 2, imageHeight / 2],
        zoom: minZoom
    }), [minZoom, imageWidth, imageHeight])

    const views = useMemo(() => (
        [new OrthographicView({id: 'ortho'})]
    ), [])
    const layers = useMemo(() => {
        // if (!dimensions) return []
        // console.info('DIMENSIONS', dimensions)
        const tileLayer = new TileLayer({
            pickable: true,
            tileSize,
            autoHighlight,
            highlightColor: [255, 255, 255, 20],
            minZoom: -7,
            maxZoom: 0,
            coordinateSystem: COORDINATE_SYSTEM.CARTESIAN,
            extent: [0, 0, imageWidth, imageHeight],
            getTileData: async ({x, y, z}: {x: number, y: number, z: number}) => {
                console.info(`Get tile data ${x} ${y} ${z}`)
                // const data = await load(`${ROOT_URL}/moon.image_files/${15 + z}/${x}_${y}.jpeg`);
                const key = `${numZoomLevels + z}_${x}_${y}`
                const uri = imageFiles[key]
                if (!uri) {
                    throw Error(`Unable to find image: ${key}`)
                }
                const dataUrl = await getFileDataUrl(uri)
                if (!dataUrl) {
                    throw Error(`Unable to find image file: ${uri}`)
                }
                const data = await load(dataUrl, ImageLoader)
                return data
            },
            onViewportLoad: onTilesLoad,

            renderSubLayers: (props: {tile: any, data: any}) => {
                const {
                    bbox: {left, bottom, right, top}
                } = props.tile;
                // const {width, height} = dimensions;
                return new BitmapLayer(props, {
                data: null,
                image: props.data,
                bounds: [
                    clamp(left, 0, imageWidth),
                    clamp(bottom, 0, imageHeight),
                    clamp(right, 0, imageWidth),
                    clamp(top, 0, imageHeight)
                ]
                });
            }
            });
        return [tileLayer]
    }, [imageFiles, tileSize, imageWidth, imageHeight, numZoomLevels])
    return (
        <DeckGL
            views={views}
            layers={layers}
            initialViewState={initialViewState}
            controller={true}
        />
    )
}

export default DeckGlTileLayer
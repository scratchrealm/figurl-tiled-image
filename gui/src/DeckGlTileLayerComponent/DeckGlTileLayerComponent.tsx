import { FunctionComponent } from 'react';
import { validateObject } from '../figurl';
import { isJSONObject, isNumber } from '../figurl/viewInterface/validateObject';
import DeckGlTileLayer from './DeckGlTileLayer/DeckGlTileLayer';

export type DeckGlTileLayerData = {
    tileSize: number
    width: number
    height: number
    numZoomLevels: number
    imageFiles: {[key: string]: string}
}
export const isDeckGlTileLayerData = (x: any): x is DeckGlTileLayerData => {
    return validateObject(x, {
        tileSize: isNumber,
        width: isNumber,
        height: isNumber,
        numZoomLevels: isNumber,
        imageFiles: isJSONObject
    })
}

type Props = {
    data: DeckGlTileLayerData
    width: number
    height: number
}

export const DeckGlTileLayerComponent: FunctionComponent<Props> = ({data}) => {
    const {tileSize, imageFiles, width: imageWidth, height: imageHeight, numZoomLevels} = data
    return (
        <DeckGlTileLayer
            tileSize={tileSize}
            imageWidth={imageWidth}
            imageHeight={imageHeight}
            numZoomLevels={numZoomLevels}
            imageFiles={imageFiles}
        />
    )
}
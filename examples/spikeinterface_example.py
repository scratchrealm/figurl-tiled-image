import sys
import os

import spikeinterface as si
import spikeinterface.toolkit as st

from figurl_tiled_image import TiledImage


def main(raw_data_file):

    print("Loading data from file: ", raw_data_file)

    R = si.BinaryRecordingExtractor(raw_data_file, 
                                sampling_frequency=30000, 
                                num_chan=384, 
                                dtype='int16')

    R_center = st.center(R)

    R_filt = st.bandpass_filter(R_center, freq_min=300, freq_max=6000)

    R_ref = st.common_reference(R_filt, 
                            reference='global', 
                            operator='median')

    processing_steps = [R_center, R_filt, R_ref]
    labels = ['Centered', 'Filtered', 'Referenced']     

    url = convert_and_upload(processing_steps, labels, 0, 60000)    

    print(url)    

    # Output on 6/8/22
    # https://figurl.org/f?v=gs://figurl/figurl-tiled-image-2&d=ipfs://QmRAkF6S2RWCxYDCjm5ov9LtxA4SivM1ETzHSphQAsRauv&label=SpikeInterface%20TiledImage%20example


def convert_and_upload(processing_steps, labels, start_frame, num_samples):
    
    X = TiledImage(tile_size=512)
    
    for step, label in zip(processing_steps, labels):
        
        print('Processing ' + label)
        arr = step.get_traces(start_frame=start_frame,
                              end_frame=start_frame+num_samples)

        if label == 'Centered':
            color_range = 5000
        else:
            color_range = 250
        
        img = st.array_to_image(arr, 
                                color_range=color_range,
                                num_timepoints_per_row = 6000)
        
        X.add_layer(label, img)
        
    url = X.url(label='SpikeInterface TiledImage example')
    
    return url


if __name__ == '__main__':

    """

    Usage:

    $ python spikeinterface_example.py '/path/to/binary_file.dat'

    This assumes the data file contains 384 channels sampled at
    30 kHz (standard Neuropixels configuration). For data with different 
    properties, the initialization of the BinaryRecordingExtractor
    object should be modified.

    """
    
    main(sys.argv[1])

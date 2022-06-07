#!/bin/bash

set -ex

TARGET=gs://figurl/figurl-tiled-image-2

yarn build

zip -r build/bundle.zip build

gsutil -m cp -R ./build/* $TARGET/
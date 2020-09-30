#!/usr/bin/env bash
echo "- clean target dir"
python -m fbs clean

./build-ui.sh

echo "- building binary"
python -m fbs freeze
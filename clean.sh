#!/bin/bash

echo "Cleaning up..."
rm -rf electron.atom.io > /dev/null 2>&1
rm -rf output/electron.docset > /dev/null 2>&1
rm output/CURRENT_VERSION > /dev/null 2>&1
echo "Done!"

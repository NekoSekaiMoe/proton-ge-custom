#!/bin/env bash

set -eu

rm -rf glslang
git clone https://github.com/KhronosGroup/glslang --depth=1
cd glslang
python3 update_glslang_sources.py
rm -rf $(find -name .gitignore)
rm -rf $(find -name .git)
rm -rf $(find -name .github)
cd ..
git add .
git commit -m "Bump glslang to latest"
git pull --rebase
git push

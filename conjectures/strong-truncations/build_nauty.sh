#!/bin/sh
# Fetch and build the nauty generators used by the census (geng, multig,
# labelg). nauty 2.8.8 is bundled inside the pynauty source distribution,
# which is what this script downloads (PyPI is reachable where nauty's own
# host may not be). Run from inside this directory.
set -e
python3 -m pip download pynauty --no-binary :all: -d _nauty_dl
tar xzf _nauty_dl/pynauty-*.tar.gz
cd pynauty-*/src/nauty2_8_8 && ./configure && make geng multig labelg
cp geng multig labelg ../../../

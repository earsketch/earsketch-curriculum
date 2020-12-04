#!/bin/bash
# Prepare curriculum html files, and toc json data files for the client

if [ ! -d "$1" ]; then
    echo "Usage: curriculum_asciidoc_builder.sh <GIT_REPO_DIR>" >&2
    exit 1
else
    GIT_REPO="$1"
fi
if [ ! -d "$2" ]; then
    SCRIPT_HOME=$GIT_REPO/scripts/earsketch-deployment/scripts
else
    SCRIPT_HOME="$2"
fi

ASCIIDOC_DIR=$GIT_REPO/curriculum-asciidoc

cd "$GIT_REPO" || exit 1
echo "Converting curriculum to html with asciidoctor..."
sudo asciidoctor \
  -a stylesheet="$SCRIPT_HOME/curr_blank.css" \
  -D "$ASCIIDOC_DIR/curriculum" "$ASCIIDOC_DIR/*.asc" || exit 1

sudo python "$SCRIPT_HOME/curr_add_html_features.py" "$GIT_REPO" || exit 1
sudo python "$SCRIPT_HOME/curr_toc.py" "$GIT_REPO" || exit 1
sudo python "$SCRIPT_HOME/curr_searchdoc.py" "$GIT_REPO" || exit 1


echo
echo "Moving JSON files from staging area to webclient..."
cd "$GIT_REPO" || exit 1
sudo mv -v curriculum-asciidoc/curr_toc.js webclient/scripts/src/data
sudo mv -v curriculum-asciidoc/curr_pages.js webclient/scripts/src/data
sudo mv -v curriculum-asciidoc/curr_searchdoc.js webclient/scripts/src/data

echo "Completed currciulum build"

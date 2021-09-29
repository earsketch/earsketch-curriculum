#!/bin/bash
# FOR LOCAL DEVELOPMENT USE ONLY
# Prepare curriculum html files, and toc json data files for the client

if [ ! -d "$1" ]; then
    echo "Usage: curriculum_asciidoc_builder.sh <GIT_REPO_DIR>" >&2
    exit 1
else
    GIT_REPO="$1"
fi
if ! command -v asciidoctor &> /dev/null
then
    echo "asciidoctor could not be found"
    exit 1
fi
if sudo python3 -c "from bs4 import BeautifulSoup" &> /dev/null; then
    echo 'BeautifulSoup is installed'
else
    echo 'BeautifulSoup is not installed. Please run "pip install beautifulsoup4"'
    exit 1
fi
if [ ! -d "$2" ]; then
    SCRIPT_HOME=$GIT_REPO/scripts
else
    SCRIPT_HOME="$2"
fi

SRC_DIR=$GIT_REPO/src
ASCIIDOC_DIR=$GIT_REPO/src/locales
LOCAL_STAGING_DIR=$GIT_REPO/curriculum-local/
ES_HOST="http://localhost:8888"

cd "$GIT_REPO" || exit 1

## array of paths to be processed
declare -a path_array=(en/v1
                      en/v2
                      es/v1
                      es/v2
                      fr/v1
                      fr/v2
                      es
                      en
                      fr)

for locale_path in "${path_array[@]}"
do
  echo "Converting curriculum to html with asciidoctor in directory " $locale_path
  locale_full_path=$ASCIIDOC_DIR/$locale_path
  echo "Curriculum full path " $locale_full_path
  LOCALE_STAGE_DIR=$LOCAL_STAGING_DIR/$locale_path/
  sudo asciidoctor \
    -a stylesheet="$SCRIPT_HOME/curr_blank.css" \
    -D "$LOCALE_STAGE_DIR" "$locale_full_path/*.adoc" || exit 1
  sudo python3 "$SCRIPT_HOME/curr_add_html_features.py" "$SRC_DIR" "$LOCALE_STAGE_DIR" "$ES_HOST" || exit 1
  if [[ ${locale_path} != *"/"* ]];then
    # this is a root locale directory. process the table of contents
    sudo python3 "$SCRIPT_HOME/curr_toc.py" "$LOCALE_STAGE_DIR" || exit 1
    sudo python3 "$SCRIPT_HOME/curr_searchdoc.py" "$LOCALE_STAGE_DIR" || exit 1
  fi
done

echo "Moving media files and resources to curriculum-local directory"
cd "$SRC_DIR" || exit 1
sudo cp -r audioMedia curriculum videoMedia theme "$LOCAL_STAGING_DIR"
cd "$GIT_REPO" || exit 1
echo
# echo "Moving JSON files from staging area to webclient..."
# cd "$GIT_REPO" || exit 1
# sudo mv -v curriculum-asciidoc/curr_toc.js webclient/scripts/src/data
# sudo mv -v curriculum-asciidoc/curr_pages.js webclient/scripts/src/data
# sudo mv -v curriculum-asciidoc/curr_searchdoc.js webclient/scripts/src/data

echo "Completed currciulum build"

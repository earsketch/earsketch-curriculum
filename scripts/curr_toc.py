# Parses curriculum html files to create table-of-contents JSON data structure

import codecs, os, os.path
from os.path import exists
import json
from bs4 import BeautifulSoup
import sys

if len(sys.argv) < 2:
    print("Error, no arguments given")
    print("Usage: curr_toc.py <CURRICULUM_STAGE_DIR>")
    exit(1)
curr_dir = sys.argv[1]

current_locale = os.path.basename(os.path.normpath(curr_dir))
toc = codecs.open(curr_dir + '/toc.html', 'r').read()
parser = BeautifulSoup(toc, 'html.parser')
toc_data = []
chapter_count = 0
display_chapter_number = -1


def get_curriculum_locale(href):
    locale_path = href.replace('{{EARSKETCH_LOCALE_CODE}}', current_locale)
    file_exists = exists(curr_dir + '../' + locale_path)
    if file_exists:
        return current_locale
    else:
        return 'en'  # default to english if the localized file does not exist


for el in parser.find_all('a'):
    el['href'] = el['href'].replace('{{EARSKETCH_LOCALE_CODE}}', get_curriculum_locale(el['href']))
    link_html = codecs.open(curr_dir+'../'+el['href'], 'r').read()
    link_content = BeautifulSoup(link_html, 'html.parser')
    el.string = link_content.h2.string


wf = open(curr_dir + '/toc.html', 'wb')
wf.write(parser.encode_contents())
wf.close()

# units
print("Processing html files to create Table-Of-Contents data structure...")
n_processed_units = 0
n_processed_ch = 0
for unit in parser.find_all('div', attrs={'class': 'sect1'}):
    n_processed_units += 1

    unit_data = {
        'title': unit.find('a').text,
        'URL': unit.find('a').attrs['href'],
        'chapters': [],
        'sections': []
    }

    # chapters
    for chapter in unit.find_all('div', attrs={'class': 'sect2'}):
        n_processed_ch += 1

        url = chapter.find('a').attrs['href']

        # check if Intro section is present in this unit
        if url.find("_intro") < 0 and url.find("_summary") < 0:
            chapter_count = chapter_count + 1
            display_chapter_number = chapter_count
        else:
            display_chapter_number = -1

        # read the html of current chapter
        chapter_html = codecs.open(curr_dir+'../'+url, 'r').read()
        sections = BeautifulSoup(chapter_html, 'html.parser')

        ch_data = {
            'title': chapter.find('a').text,
            'URL': url,
            'displayChNum': display_chapter_number,
            'sections': []
        }

        # subsections of chapter
        for section in sections.find_all('div', attrs={'class':'sect2'}):
            sec_data = {
                'title': section.find('h3').text,
                'URL': url+'#'+section.find('h3').attrs['id'],
            }

            ch_data['sections'].append(sec_data)

        unit_data['chapters'].append(ch_data)

    toc_data.append(unit_data)

toc_pages = []

for unitIdx, unit in enumerate(toc_data):
    if len(unit['chapters']) == 0:
        toc_pages.append([unitIdx])

    for chIdx, ch in enumerate(unit['chapters']):
        if len(ch['sections']) == 0:
            toc_pages.append([unitIdx, chIdx])
        for secIdx, sec in enumerate(ch['sections']):
            toc_pages.append([unitIdx, chIdx, secIdx])

wf = open(curr_dir + '/curr_toc.json', 'w')
wf.write(json.dumps(toc_data, indent=4))
wf.close()

wf = open(curr_dir + '/curr_pages.json', 'w')
wf.write(json.dumps(toc_pages))
wf.close()

print(str(n_processed_units) + " units with " + str(n_processed_ch) + " chapters processed")

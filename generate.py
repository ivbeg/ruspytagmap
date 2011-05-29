# -*- coding: utf-8 -*-
from pytagcloud import create_tag_image, create_html_data, make_tags, \
    LAYOUT_HORIZONTAL, LAYOUTS, LAYOUT_MIX, LAYOUT_MOST_HORIZONTAL
from pytagcloud.colors import COLOR_SCHEMES
from pytagcloud.lang.counter import get_tag_counts
import os, time, sys
from pymorphy import get_morph
morph = get_morph('dicts/ru', 'sqlite')

COLOR_MAP = ((232, 43, 30), (200, 188, 107), (85, 122, 102), (69, 54, 37), (160, 182, 136))

def update_text(t):
	info = morph.get_graminfo(t.upper())
	if len(info) > 0:
		return info[0]['norm'].lower()
	return t

def process_tags(taglist):
	allt = {}
	for t, v in taglist:
		w = update_text(t)
		if allt.has_key(w):
			allt[w] += v
		else:
			allt[w] = v
	d = sorted(allt.items(), lambda x, y: cmp(x[1], y[1]), reverse=True)
	return d


def run(textpath):
	text = open(textpath, 'r')
	start = time.time()
	taglist = get_tag_counts(text.read().decode('utf8'))
	cleantaglist = process_tags(taglist)
	tags = make_tags(taglist[0:100], colors=COLOR_MAP)
	create_tag_image(tags, 'cloud.png', size=(1280, 900), background=(0, 0, 0 , 255), layout=LAYOUT_MOST_HORIZONTAL, crop=False,  fontname='Cuprum', fontzoom=2)
	tags2 = make_tags(cleantaglist[0:100], colors=COLOR_MAP)
	create_tag_image(tags2, 'rcloud.png', size=(1280, 900), background=(0, 0, 0, 255), layout=LAYOUT_MOST_HORIZONTAL, crop=False, fontname='Cuprum', fontzoom=2)
	print "Duration: %d sec" % (time.time() - start)

if __name__ == "__main__":
	if len(sys.argv) > 1:
	    run(sys.argv[1])

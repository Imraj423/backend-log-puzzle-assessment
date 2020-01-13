#!/usr/bin/env python2
"""
Logpuzzle exercise

Copyright 2010 Google Inc.
Licensed under the Apache License, Version 2.0
http://www.apache.org/licenses/LICENSE-2.0

Google's Python Class
http://code.google.com/edu/languages/google-python-class/

Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg
HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U;
Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"

"""

import os
import re
import sys
import urllib
import argparse


# def read_urls():
#     puzzle_pieces = []
#     linenum = 0
#     substr = "puzzle".lower()
#     with open('animal.txt', 'rt') as myfile:
#         for line in myfile:
#             linenum += 1
#             if line.lower().find(substr) != -1:
#                 puzzle_pieces.append("Line " + str(linenum)
#                                      + ": " + line.rstrip('\n'))
#                 if line not in puzzle_pieces:
#                     puzzle_pieces.append(line)
#                 print(line)
#         return puzzle_pieces


def read_urls(filename):
    puzzle_urls = []
    full_urls = []

    with open(filename) as f:
        for line in f:
            url = re.findall(r'(\S*puzzle\S*.jpg)', line)
            if url and url[0] not in puzzle_urls:
                puzzle_urls.append(url[0])

        puzzle_urls.sort(
            key=lambda x: re.search(r'\w[^-]*$', x).group(0))

        for item in puzzle_urls:
            new_items = 'http://code.google.com{}'.format(item)
            full_urls.append(new_items)
        return full_urls


def download_images(url, dest_dir):
    """Given the urls already in the correct order, downloads
    each image into the given directory.
    Gives the images local filenames img0, img1, and so on.
    Creates an index.html in the directory
    with an img tag to show each local image file.
    Creates the directory if necessary.
    """
    index_num = 0
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)
    with open(dest_dir + '/index.html', 'w+') as w:
        w.write('<html>\n')
        w.write('<body>\n')

        for item in url:
            image_name = 'img' + str(index_num)
            index_num += 1
            print('Retrieving image {}'.format(image_name))
            urllib.urlretrieve(item, os.path.join(dest_dir, image_name))
            w.write('<img src={}>'.format(image_name))
        w.write('<body>\n')
        w.write('<html>\n')
        w.close()


def create_parser():
    """Create an argument parser object"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-d', '--todir',  help='destination directory for downloaded images')
    parser.add_argument('logfile', help='apache logfile to extract urls from')

    return parser


def main(args):

    """Parse args, scan for urls, get images from urls"""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)

    img_urls = read_urls(parsed_args.logfile)

    if parsed_args.todir:
        download_images(img_urls, parsed_args.todir)
    else:
        print('\n'.join(img_urls))


if __name__ == '__main__':
    main(sys.argv[1:])

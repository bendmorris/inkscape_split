#!/usr/bin/env python
'''
Used to extract each layer from an Inkscape SVG file as a separate PNG image.
Also automates palette swaps.

Usage: ./inkscape_split.py file.svg [layer 1] [layer 2] ...

where file.svg is an SVG file.
'''
import argparse
import os
import subprocess
import sys
from xml.etree import cElementTree as ElementTree


def main():
    parser = argparse.ArgumentParser(description='inkscape_split')
    parser.add_argument('input-file', help='file to split')
    parser.add_argument('--dpi', type=int, default=90, help='DPI for export (default: 90)')
    parser.add_argument('--layers', nargs='*', help='layers to export (default: all layers)')

    args = parser.parse_args()

    input_file = args.input_file
    dpi = args.dpi
    layers = args.layers

    inkscape = '{http://www.inkscape.org/namespaces/inkscape}'

    input_dir = os.path.split(os.path.abspath(input_file))[0]
    input_name = '.'.join(os.path.basename(input_file).split('.')[:-1])

    output_file = input_file.replace('.svg', '_all.svg')
    with open(input_file) as input:
        with open(output_file, 'w') as output:
            output.write(input.read().replace('style="display:none"', ''))
    input_file = output_file
    doc = ElementTree.parse(input_file)
    root = doc.getroot()
    for child in root:
        if '%sgroupmode' % inkscape in child.attrib and child.attrib['%sgroupmode' % inkscape] == 'layer':
            name = child.attrib['%slabel' % inkscape]
            if (not layers) or (name in layers):
                layer_id = child.attrib['id']
                output_file = os.path.join(input_dir, '%s_%s.png' % (input_name, name.replace(' ', '_')))
                print output_file        
            
                cmd = ('inkscape --without-gui --export-id=%s --export-id-only --export-png=%s --export-dpi=%s %s' % 
                       (layer_id, output_file, dpi, input_file))
                print cmd
                subprocess.call(cmd.split())


if __name__ == '__main__':
    main()

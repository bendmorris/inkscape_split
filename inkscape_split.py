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
    parser.add_argument('input_file', help='file to split')
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
    last_root = None
    if os.path.exists(output_file):
        last_root = ElementTree.parse(output_file).getroot()
        last_mtime = os.path.getmtime(output_file)
    with open(input_file) as input:
        with open(output_file, 'w') as output:
            output.write(input.read().replace('style="display:none"', ''))
    input_file = output_file
    doc = ElementTree.parse(input_file)
    root = doc.getroot()
    for child in root:
        if '{}groupmode'.format(inkscape) in child.attrib and child.attrib['{}groupmode'.format(inkscape)] == 'layer':
            name = child.attrib['{}label'.format(inkscape)]
            if (not layers) or (name in layers):
                layer_id = child.attrib['id']
                output_file = os.path.join(input_dir, '{}_{}.png'.format(input_name, name.replace(' ', '_')))

                if last_root and os.path.exists(output_file) and os.path.getmtime(output_file) >= last_mtime:
                    s = ''.join(map(ElementTree.tostring, (c for c in child)))
                    # print(s)
                    found = False
                    for child2 in last_root:
                        s2 = ''.join(map(ElementTree.tostring, (c for c in child2)))
                        if s == s2:
                            print('  ... skipping {} which is up to date  ...'.format(output_file))
                            os.utime(output_file, None)
                            found = True
                            break
                    if found:
                        continue

                print(output_file)

                cmd = 'inkscape --without-gui --export-id={} --export-id-only --export-png={} --export-dpi={} {}'.format(
                    layer_id, output_file, dpi, input_file
                )
                print(cmd)
                subprocess.call(cmd.split())


if __name__ == '__main__':
    main()

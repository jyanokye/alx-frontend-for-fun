#!/usr/bin/python3
"""
This script converts a Markdown file to HTML file
"""

import argparse
import os
import re
import sys

def main():
    """
    Main function that converts a Markdown file to HTML and writes the output to a file.
    """
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Convert a Markdown file to HTML.')
    parser.add_argument('input_file', help='Path to the input Markdown file.')
    parser.add_argument('output_file', help='Path to the output HTML file.')
    args = parser.parse_args()

    # Check that the input file exists and is a file
    if not os.path.isfile(args.input_file):
        print(f"Input file '{args.input_file}' does not exist.", file=sys.stderr)
        sys.exit(1)

    # Convert the Markdown file to HTML
    with open(args.input_file, 'r', encoding='utf-8') as f:
        html_lines = []
        for line in f:
            # Convert Markdown headings to the HTML headings
            match = re.match(r'^(#+) (.*)$', line)
            if match:
                heading_level = len(match.group(1))
                heading_text = match.group(2)
                html_lines.append(f'<h{heading_level}>{heading_text}</h{heading_level}>')
            else:
                html_lines.append(line.rstrip())

    # Write the HTML output to a file
    with open(args.output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(html_lines))

    # Indicate that the conversion was successful
    print(f"Successfully converted '{args.input_file}' to '{args.output_file}'.", file=sys.stderr)

if __name__ == '__main__':
    main()

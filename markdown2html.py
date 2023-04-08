#!/usr/bin/python3

import sys
import markdown

def convert_markdown_to_html(input_file, output_file):
    """
    Convert a Markdown file to an HTML file.
    input_file: the name of the input Markdown file
    output_file: the name of the output HTML file
    FileNotFoundError: if the input file doesn't exist
    """
    # check if the input file exists
    try:
        with open(input_file, 'r') as f:
            markdown_text = f.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"Missing {input_file}")

    # convert the Markdown text to HTML
    html_text = markdown.markdown(markdown_text)

    # write the HTML output to the output file
    with open(output_file, 'w') as f:
        f.write(html_text)

if __name__ == '__main__':
    # check if the number of arguments is correct
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py input_file.md output_file.html", file=sys.stderr)
        sys.exit(1)

    # get the input and output file names from the arguments
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    try:
        convert_markdown_to_html(input_file, output_file)
    except FileNotFoundError as e:
        print(e, file=sys.stderr)
        sys.exit(1)

    # print nothing and exit with success status
    sys.exit(0)


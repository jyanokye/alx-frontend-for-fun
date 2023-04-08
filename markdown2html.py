#!/usr/bin/python3
"""
A script that converts Markdown to HTML 
"""

import sys
import os
import re

def convert_markdown_to_html(markdown_file, html_file):
    """
    Converts a Markdown file to HTML and writes the output to a file.
    """
    # Check that the input file exists and is a file
    if not (os.path.exists(markdown_file) and os.path.isfile(markdown_file)):
        print(f"Missing {markdown_file}", file=sys.stderr)
        sys.exit(1)

    # Read the input Markdown file and convert it to HTML
    with open(markdown_file, encoding="utf-8") as f:
        html_lines = []
        current_paragraph = ""
        in_paragraph = False
        for line in f:
            # Check for Markdown headings
            match = re.match(r"^(#+) (.*)$", line)
            if match:
                heading_level = len(match.group(1))
                heading_text = match.group(2)
                html_lines.append(f"<h{heading_level}>{heading_text}</h{heading_level}>")
            elif re.match(r"^\s*[*+-]\s+(.*)$", line):
                # Check for unordered lists
                if not in_paragraph:
                    html_lines.append("<ul>")
                    in_paragraph = True
                html_lines.append(f"<li>{re.match(r"^\s*[*+-]\s+(.*)$", line).group(1)}</li>")
            elif re.match(r"^\s*[0-9]+\.\s+(.*)$", line):
                # Check for ordered lists
                if not in_paragraph:
                    html_lines.append("<ol>")
                    in_paragraph = True
                html_lines.append(f"<li>{re.match(r"^\s*[0-9]+\.\s+(.*)$", line).group(1)}</li>")
            elif re.match(r"^\s*__(.*)__\s*$", line):
                # Check for emphasis syntax
                html_lines.append(f"<em>{re.match(r'^\s*__(.*)__\s*$', line).group(1)}</em>")
            elif line.strip() == "":
                # Check for empty lines (which indicate the end of a paragraph)
                if in_paragraph:
                    html_lines.append("</ul>" if html_lines[-1] == "<ul>" else "</ol>")
                    html_lines.append(f"<p>{current_paragraph.strip()}</p>")
                    current_paragraph = ""
                    in_paragraph = False
            else:
                # Add the current line to the current paragraph
                current_paragraph += line
                in_paragraph = True

        # If the last line in the file was not an empty line, we need to add the final paragraph
        if in_paragraph:
            html_lines.append(f"<p>{current_paragraph.strip()}</p>")
            if html_lines[-1] == "<ul>" or html_lines[-1] == "<ol>":
                html_lines.append("</ul>" if html_lines[-1] == "<ul>" else "</ol>")

    # Write the HTML output to a file
    with open(html_file, "w", encoding="utf-8") as f:
        f.write("\n".join(html_lines))

if __name__ == "__main__":
    # Check that the right number of arguments were provided
    if len(sys.argv) != 3:
        print("Usage: ./md2html.py <markdown_file> <html_file>", file=sys.stderr)
        sys.exit(1)

    # Get the input and output file names from the command-line arguments
    markdown_file = sys.argv[1]
    html_file = sys.argv[2]

    # Convert the Markdown file to HTML and write the output to a file
    convert_markdown_to_html(markdown_file, html_file)

    # Exit with a success status code
    sys.exit(0)


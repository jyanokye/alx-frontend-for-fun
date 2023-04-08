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
        in_list = False
        list_type = None
        in_paragraph = False
        for line in f:
            # Check for Markdown headings
            match = re.match(r"^(#+) (.*)$", line)
            if match:
                close_paragraph(in_paragraph, html_lines)
                heading_level = len(match.group(1))
                heading_text = match.group(2)
                html_lines.append(f"<h{heading_level}>{heading_text}</h{heading_level}>")
            else:
                # Check for Markdown unordered lists
                match = re.match(r"^(\*|\+|\-) (.*)$", line)
                if match:
                    close_paragraph(in_paragraph, html_lines)
                    if not in_list:
                        html_lines.append("<ul>")
                        in_list = True
                        list_type = "unordered"
                    html_lines.append(f"<li>{match.group(2)}</li>")
                else:
                    # Check for Markdown ordered lists
                    match = re.match(r"^[0-9]+\.(.*)$", line)
                    if match:
                        close_paragraph(in_paragraph, html_lines)
                        if not in_list:
                            html_lines.append("<ol>")
                            in_list = True
                            list_type = "ordered"
                        html_lines.append(f"<li>{match.group(1).strip()}</li>")
                    else:
                        # Check for Markdown paragraphs
                        if line.strip():
                            if not in_paragraph:
                                html_lines.append("<p>")
                                in_paragraph = True
                            html_lines.append(line.strip())
                        else:
                            close_paragraph(in_paragraph, html_lines)
                            if in_list:
                                if list_type == "unordered":
                                    html_lines.append("</ul>")
                                else:
                                    html_lines.append("</ol>")
                                in_list = False

        # If the file ended with a list or paragraph, close the corresponding tag
        close_paragraph(in_paragraph, html_lines)
        if in_list:
            if list_type == "unordered":
                html_lines.append("</ul>")
            else:
                html_lines.append("</ol>")

    # Write the HTML output to a file
    with open(html_file, "w", encoding="utf-8") as f:
        f.write("\n".join(html_lines))

def close_paragraph(in_paragraph, html_lines):
    """
    Closes the paragraph tag if one is open.
    """
    if in_paragraph:
        html_lines.append("</p>")
        in_paragraph = False

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

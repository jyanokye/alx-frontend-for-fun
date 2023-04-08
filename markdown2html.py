#!/usr/bin/python3
"""
A script to convert Markdown to HTML.

Arguments:
    input_file: the name of the input Markdown file
    output_file: the name of the output HTML file
"""

import os.path
import sys

import markdown


def parse_headings(markdown_text):
    """
    Parses Markdown headings and replaces them with their corresponding HTML tags.

    Args:
        markdown_text (str): The Markdown text to parse.

    Returns:
       an str: The HTML text with headings parsed.
    """
    html_text = ""
    for line in markdown_text.split("\n"):
        if line.startswith("#"):
            # Determine the heading level
            heading_level = line.count("#")
            # Remove the heading syntax from the line
            line = line.strip("# ")
            # Generate the HTML tag
            tag = f"h{heading_level}"
            # Append the HTML tag to the HTML text
            html_text += f"<{tag}>{line}</{tag}>"
        else:
            # Append the line to the HTML text as is
            html_text += line
        # Add a newline character to the HTML text
        html_text += "\n"
    return html_text


def parse_lists(markdown_text):
    """
    Parses Markdown unordered lists and replaces them with their corresponding HTML tags.

    Args:
        markdown_text (str): The Markdown text to parse.

    Returns:
        str: The HTML text with unordered lists parsed.
    """
    html_text = ""
    in_list = False
    for line in markdown_text.split("\n"):
        if line.startswith("- "):
            # If not already in a list, start a new list
            if not in_list:
                html_text += "<ul>\n"
                in_list = True
            # Remove the list syntax from the line and generate the HTML item tag
            line = line[2:].strip()
            html_text += f"<li>{line}</li>\n"
        else:
            # If in a list, end the list
            if in_list:
                html_text += "</ul>\n"
                in_list = False
            # Add the line to the HTML text as is
            html_text += line + "\n"
    # If in a list after parsing is complete, list should end
    if in_list:
        html_text += "</ul>\n"
    return html_text


def main():
    # Check if the correct number of arguments were provided
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py <input_file> <output_file>", file=sys.stderr)
        sys.exit(1)

    # Get the input and output file names
    input_file = sys.argv[1]
    output_file = sys.argv[2]

    # Check if the input file exists
    if not os.path.isfile(input_file):
        print(f"Missing {input_file}", file=sys.stderr)
        sys.exit(1)

    # Reading the input file
    with open(input_file, "r") as f:
        markdown_text = f.read()

    # Parses the Markdown text
    html_text = parse_headings(markdown_text)
    html_text = parse_lists(html_text)
    html_text = markdown.markdown(html_text)

    # Write the HTML text to the output file
    with open(output_file, "w") as f:
        f.write(html_text)

    # Exit successfully
    sys.exit(0)


if __name__ == "__main__":
    main()

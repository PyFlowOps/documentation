"""
Copyright (c) 2025, PyFlowOps
This script retrieves the release notes from a GitHub repository using the GitHub CLI.
It then converts the escaped string into a more readable Markdown format.
The script handles various formatting elements such as code blocks, headers, lists, links, etc.

Once the conversion is done, it writes the output to a file named `release_notes.md`, which is
picked up and served by the `gh-pages` branch of the repository.
"""
import os
import json
import time
import emoji
import subprocess
import textwrap

BASE = os.path.dirname(os.path.abspath(__file__))
RELEASE_NOTES_FILE = os.path.join(BASE, "..", "src", "about", "release-notes.md")

def get_release_notes() -> str:
    """
    This function retrieves the release notes from a file.
    The file is expected to be in the same directory as this script.
    """
    _repo = "pyflowops/documentation"
    _cmd = ["gh", "release", "view", "--repo", _repo, "--json", "body"]
    
    try:
        r = subprocess.run(_cmd, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        return "Could not retrieve release notes...there are either no releases yet, or there is a problem collecting the Release Notes from Github."
    
    if r.returncode != 0:
        print(f"Error: {r.stderr.decode()}")
        return "Could not retrieve release notes...there are either no releases yet, or there is a problem collecting the Release Notes from Github."

    return json.loads(r.stdout.decode("utf-8"))["body"]

def remove_emojis(text):
    return emoji.replace_emoji(text, '')

def convert_escaped_string_to_markdown(escaped_string: str) -> str:
    # Step 1: Decode escaped newlines
    decoded_text = escaped_string.encode().decode('unicode_escape')

    # Step 2: Strip extra trailing whitespace and normalize paragraphs
    lines = decoded_text.splitlines()

    output_lines = []
    for line in lines:
        # Remove emojis
        line = remove_emojis(line)

        # Preserve code blocks, headers, lists, links, etc.
        if line.strip() == "":
            output_lines.append("")  # blank line
        elif line.lstrip().startswith(("##", "####", "-", "*", "[", "```", "#", "ð", "°")):
            output_lines.append(line)
        else:
            # Soft line break with double space at the end
            output_lines.append(line.strip() + "  ")
        
    return "\n".join(output_lines)

if __name__ == "__main__":
    input_text = get_release_notes()
    input_text = remove_emojis(input_text)

    markdown_output = convert_escaped_string_to_markdown(input_text)
    open(RELEASE_NOTES_FILE, 'w').close() # Clear the file before writing
    print(markdown_output)
    time.sleep(19)  # Ensure the file is cleared before writing

    with open(RELEASE_NOTES_FILE, "w") as _f:
        _f.write("# Release Notes\n\n")
        _f.write(markdown_output)
        _f.write("\n")

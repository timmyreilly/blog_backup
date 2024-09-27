import os
import re
import sys

def update_image_paths_in_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex pattern to match images, possibly wrapped in links
    # Matches:
    # - ![Alt Text](image_path)
    # - [![Alt Text](image_path)](link)
    image_link_pattern = re.compile(
        r'''
        (?P<link_start>\[)?                              # Optional opening '[' for a link
        !\[(?P<alt_text>.*?)\]                           # Image alt text
        \((?P<image_path>[^)]+)\)                        # Image path
        (?(link_start)\]\((?P<link_url>[^)]+)\))         # Closing '](link)' if link_start is '['
        ''',
        re.VERBOSE | re.DOTALL
    )

    def replace_image_path(match):
        is_link = match.group('link_start')  # '[' if image is wrapped in a link
        alt_text = match.group('alt_text')   # Alt text from image tag
        image_path = match.group('image_path')  # Original image path
        link_url = match.group('link_url') if is_link else None  # Link URL if image is wrapped

        # Extract the image filename
        image_filename = os.path.basename(image_path)
        # Update image path to use the new base URL
        new_image_path = '{{ site.baseurl }}/assets/images/' + image_filename

        # Reconstruct the image tag
        new_image_tag = f'![{alt_text}]({new_image_path})'

        if is_link:
            # Reconstruct the link wrapping the image
            new_link = f'[{new_image_tag}]({link_url})'
            return new_link
        else:
            return new_image_tag

    # Replace all image occurrences in the content
    new_content = image_link_pattern.sub(replace_image_path, content)

    # Write the updated content back to the file
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(new_content)

def process_markdown_files(directory):
    # Process all Markdown files in the given directory
    for filename in os.listdir(directory):
        if filename.endswith('.md'):
            filepath = os.path.join(directory, filename)
            update_image_paths_in_file(filepath)
            print(f'Processed {filename}')

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python update_image_paths.py path_to_markdown_files")
    else:
        directory = sys.argv[1]
        if not os.path.isdir(directory):
            print(f"Error: {directory} is not a valid directory.")
            sys.exit(1)
        process_markdown_files(directory)

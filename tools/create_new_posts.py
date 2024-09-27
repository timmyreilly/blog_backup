import re
import sys
import os

def process_file(filename):
    with open(filename, 'r') as f:
        content = f.read()
    
    # Pattern to match [caption ... ]...[/caption]
    caption_pattern = re.compile(r'\[caption.*?\](.*?)\[/caption\]', re.DOTALL)
    
    # Function to process each caption block
    def replace_caption(match):
        caption_content = match.group(1).strip()
        # Now extract the image tag
        # The content may have a link around the image tag
        # Pattern to match [![alt](image_path)](link) caption_text
        image_link_pattern = re.compile(r'\[!\[(.*?)\]\((.*?)\)\]\((.*?)\)\s*(.*)')
        image_match = image_link_pattern.match(caption_content)
        if image_match:
            alt_text = image_match.group(1)
            image_path = image_match.group(2)
            link = image_match.group(3)
            caption_text = image_match.group(4).strip()
        else:
            # Try to match ![alt](image_path) caption_text
            image_pattern = re.compile(r'!\[(.*?)\]\((.*?)\)\s*(.*)')
            image_match = image_pattern.match(caption_content)
            if image_match:
                alt_text = image_match.group(1)
                image_path = image_match.group(2)
                caption_text = image_match.group(3).strip()
            else:
                # Could not match image tag
                return match.group(0)  # Return the original content

        # Remove size suffixes from image file name
        # For example: IMG_1234-768x1024.jpg -> IMG_1234.jpg
        image_filename = os.path.basename(image_path)
        image_dir = os.path.dirname(image_path)
        image_filename_no_ext, image_ext = os.path.splitext(image_filename)
        # Remove size suffixes
        image_filename_no_size = re.sub(r'-\d+x\d+$', '', image_filename_no_ext)
        new_image_filename = image_filename_no_size + image_ext
        # Construct new image path
        new_image_path = '{{ site.baseurl }}/assets/images/' + new_image_filename

        # Construct new image tag
        new_image_tag = f'![{alt_text}]({new_image_path})'
        return new_image_tag

    # Replace all caption blocks
    new_content = caption_pattern.sub(replace_caption, content)

    return new_content

if __name__ == '__main__':
    filename = sys.argv[1]
    new_content = process_file(filename)
    print(new_content)

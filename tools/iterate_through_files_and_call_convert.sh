#!/bin/bash

# Directories
INPUT_DIR="../backup_blog/_posts/"
OUTPUT_DIR="./converted_posts/"

# Create the output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Loop through all files in the input directory
for file in "$INPUT_DIR"*; do
    # Get the base filename
    filename=$(basename "$file")
    
    # Check if the filename already contains a date (YYYY-MM-DD)
    if [[ ! "$filename" =~ [0-9]{4}-[0-9]{2}-[0-9]{2} ]]; then
        # Extract the date from the file's front matter
        date_line=$(grep '^date: "' "$file")
        if [[ $date_line =~ date:\ \"([0-9]{4}-[0-9]{2}-[0-9]{2})\" ]]; then
            date="${BASH_REMATCH[1]}"
            # Create a new filename with the date appended
            new_filename="${date}-${filename}"
            # Process the file using the Python script
            python create_new_posts.py "$file" > "$OUTPUT_DIR$new_filename"
            echo "Processed $filename -> $new_filename"
        else
            echo "Date not found in $filename; skipping."
        fi
    else
        echo "Skipping $filename (already has date)."
    fi
done

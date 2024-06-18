import requests
import gzip
import shutil
import os
import sys
from urllib.parse import urlparse

def download_and_unzip(url: str):
    # Extract the output filename from the URL
    parsed_url = urlparse(url)
    output_file = os.path.basename(parsed_url.path).replace('.gz', '')

    # Download the file
    response = requests.get(url, stream=True)
    response.raise_for_status()  # Check for any request errors

    # Write the gzipped file to the local file system
    gz_file = output_file + '.gz'
    with open(gz_file, 'wb') as f:
        f.write(response.content)

    # Unzip the file
    with gzip.open(gz_file, 'rb') as f_in:
        with open(output_file, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)

    # Optionally remove the .gz file after extraction
    os.remove(gz_file)

# Usage
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 downloadRB.py <url>")
        sys.exit(1)

    url = sys.argv[1]
    download_and_unzip(url)


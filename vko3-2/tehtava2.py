"""
Checkpoint / viikko 3
Tehtävä 2
"""

import argparse
import time
import os.path
from google.cloud import storage

def download_file(bucket_name, source_file, destination_file):
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    
    blob = bucket.blob(source_file)
    blob.download_to_filename(destination_file)

    print(f"Downloaded file {source_file} from bucket {bucket_name} as {destination_file}.\n")


def read_file(file_to_read, lines_to_print):
    with open(file_to_read, "r") as source_file:
        lines = []
        counter = 1

        while counter <= lines_to_print:
            lines.append(source_file.readline().rstrip("\n"))
            
            counter += 1

        sorted_lines = sorted(lines, key=len)

        print(f"The first {lines_to_print} lines in ascending order are:")

        for item in sorted_lines:
            print(item)


def main(lines_to_print):
    bucket = "checkpoint-puketti"
    source = "checkpoint.txt"
    destination = source
    
    download_file(bucket, source, destination)
    
    while not os.path.exists(source):
        time.sleep(2)

    if os.path.isfile(source):
        try:
            read_file(source, int(lines_to_print))

        except OSError:
            print("File not found.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("lines")
    
    arguments = parser.parse_args()

    main(arguments.lines)
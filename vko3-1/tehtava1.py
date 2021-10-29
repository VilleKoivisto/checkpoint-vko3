"""
Checkpoint / viikko 3
Tehtävä 1
"""
import urllib.request
import json
import time
from google.cloud import storage


def get_json_data(remote_url):
    """ Hae json data url:stä """
    with urllib.request.urlopen(remote_url) as response:
        github_data = response.read()
        github_json = json.loads(github_data)

    return github_json


def write_parameter(json_data):
    """ Kirjoita parameter kentät tiedostoon """
    with open("checkpoint.txt", "w") as file:
        for item in json_data["items"]:
            file.write((item["parameter"]) + "\n")


def get_buckets():
    """ Hae olemassa olevat puketit projektista """
    storage_client = storage.Client()
    buckets = storage_client.list_buckets()

    bucket_list = []

    for bucket in buckets:
        bucket_list.append(bucket.name)

    return bucket_list


def create_bucket(bucket_name):
    """ luo puketti projektiin """
    storage_client = storage.Client()
    bucket = storage_client.create_bucket(bucket_name)
    
    print(f"Bucket {bucket.name} created!")


def upload_file(bucket_name, filename, blobname):
    """ Lataa tiedosto pukettiin """
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    
    blob = bucket.blob(blobname)
    blob.upload_from_filename(filename)

    print(f"Uploaded file {filename} to bucket {bucket_name}.")


def main():
    # aseta url
    remote_url = "https://2ri98gd9i4.execute-api.us-east-1.amazonaws.com/dev/academy-checkpoint2-json"
    bucket_name = "checkpoint-puketti"
    
    # hae data ja kirjoita tiedostoon
    json_data = get_json_data(remote_url)
    write_parameter(json_data)

    # tarkista onko puketti jo luotu
    list_buckets = get_buckets()

    # tarkista onko puketti jo olemassa ja luo jos ei
    if bucket_name not in list_buckets:
        # luo uusi puketti
        create_bucket(bucket_name)

    # tarkista uudelleen, koska puketin luomisessa kestää, lataa tiedosto kun puketti löytyy
    while True:
        if bucket_name in list_buckets:
            # siirrä tiedosto pukettiin
            file_name = "checkpoint.txt"
            blob_name = file_name

            upload_file(bucket_name, file_name, blob_name)
            print("File uploaded")

            break
        
        # wait for a second or five
        time.sleep(5)


if __name__ == "__main__":
    main()
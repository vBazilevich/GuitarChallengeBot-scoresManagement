import pymongo
import bson
import sys
import os
import urllib.parse
import hashlib
import psycopg2
import glob
import pandas as pd

from dotenv import load_dotenv
load_dotenv()

def load_file(filename, collection, identifier, descriptions, cursor, lvl_id):
    with open(filename, "rb") as f:
        try:
            # Load image
            content = f.read()
            file = {"filename": filename,
                    "identifier": identifier,
                    "md5-hash": hashlib.md5(content).hexdigest(),
                    "content": bson.binary.Binary(content)}
            collection.insert_one(file)
            # Load description
            _, author, name, desc = descriptions.iloc[lvl_id - 1]
            cursor.callproc('create_song', (author, name, desc))
        except pymongo.errors.DuplicateKeyError:
            print(f"File {filename} was previously uploaded to the same collection. Skipping")

def main():
    images_dir = sys.argv[1]
    os.chdir(images_dir)
    mongo_link = os.getenv("MONGO_URL")
    client = pymongo.MongoClient(mongo_link)
    db = client["images-storage"]
    collection = db["images"]

    DATABASE_URL = os.getenv("DATABASE_URL")
    desc_db = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = desc_db.cursor()

    descriptions = pd.read_csv("descriptions.csv")
    print(descriptions)

    n_levels = len(glob.glob('level*'))

    for index in range(1, n_levels + 1):
        filename = glob.glob(f'level-{index}.*')[0]
        load_file(filename, collection, f"level-{index}", descriptions, cur, index)
        desc_db.commit()

    cur.close()
    desc_db.close()

if __name__ == "__main__":
    main()

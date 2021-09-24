# GuitarChallengeBot scores uploader
This small utility aims to help the bot manager to upload new scores with metainformation to corresponding storages.

## Setting up
You have to define two environment variables `MONGO_URL` and `DATABASE_URL`.
For detailed explanation please check deployment instructions of the main [project](https://github.com/vBazilevich/GuitarChallengeBot)

## Preparing files for upload
1. Create a new folder
2. Copy you scores there 
3. Rename them in format `level-<idx>.<ext>` where `<idx>` is level number from 1 to the number of levels and `<ext>` is image extension
4. Create file named `descriptions.csv` in the same folder. Check provided example in `image_dir` folder

## Uploading
Run command `python main.py <images_folder>` where  `<images_folder>` is a path to your folder with scores

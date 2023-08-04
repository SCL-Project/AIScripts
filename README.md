# OpenAI Scripts
Author: Roman Willi  
Date: 28th of July, 2023

**Link to GitHub:** [AI Scripts Repository](https://github.com/SCL-Project/AIScripts)

This repository contains two main scripts (`Analyser.py` and `Transcribe.py`) that interact with OpenAI's API to perform text summarization and audio transcription respectively. Both scripts were authored by Roman Willi.

## Analyser.py

Authored by Roman Willi, this script reads text files from its current directory and uses OpenAI's Chat model to summarize the content. The text file is split into chunks, each of which is then summarized.

The script retrieves necessary configurations such as the API key, models, tokens, and other settings from the `API.json` file. 

In case of any interruptions, the script can resume from where it left off using checkpoint data stored in a file named `checkpoints.json`. If an error occurs during the execution, the script will retry a specified number of times, with a delay between each retry.

Once a file is completely summarized, the script renames the file, adding a 'Done_' prefix to the original filename.

## Transcribe.py

Also authored by Roman Willi, this script is designed to transcribe audio files located in the directory from where it is run. The script supports several audio formats including .mp3, .wav, .aac, .flac, .ogg, .m4a, as well as video formats like .mp4, .avi, .mkv, .mov, .wmv, .opus. 

The script breaks each audio file into chunks and transcribes each chunk using OpenAI's Whisper ASR system. The transcriptions are then written to a text file with the same name as the audio file. 

Upon successful transcription of an audio file, the script renames the file, adding a 'Transcribed_' prefix to the original filename.

Similar to `Analyser.py`, the script retrieves necessary configurations from the `API.json` file and has a retry mechanism in case of failures during execution.

## API.json

This is a configuration file that is used by both `Analyser.py` and `Transcribe.py`. It contains the OpenAI API key, models, and other configuration settings that the scripts use to interact with the OpenAI API.


# Step-by-Step Guide to Running the Scripts

Before you can run the scripts, you need to ensure you have the correct setup and have configured the necessary files. Follow the steps below:

## Step 1: Install Python

These scripts are written in Python, so you will need to have Python installed on your system. If you don't have Python installed, you can download it from the official website: https://www.python.org/downloads/.

## Step 2: Install Required Python Libraries

The scripts use several Python libraries. You can install these using `pip`, which is a package manager for Python. The required libraries are:

- `openai`: Used to interact with the OpenAI API.
- `textwrap`: Used in `Analyser.py` to wrap input paragraphs.
- `os` and `shutil`: Used for interacting with the system, managing files and directories.
- `time`: Used to create delays.
- `json`: Used to read and write JSON files.
- `pydub`: Used in `Transcribe.py` to handle audio files.
- `glob`: Used in `Transcribe.py` to find all the pathnames matching a specified pattern.

To install these, open your command line (Command Prompt on Windows, Terminal on macOS/Linux) and enter the following command:

```
pip install openai textwrap os shutil time json pydub glob
```

## Step 3: Obtain OpenAI API Key

In order to use OpenAI's services, you will need an API key. If you don't have one, you can obtain it by creating an account on OpenAI's website and following their process for obtaining an API key.

## Step 4: Configure `API.json` File

Once you have your OpenAI API key, open the `API.json` file in a text editor. Replace the placeholders with your actual OpenAI API key and other settings based on your requirements.

## Step 5: Place Your Files in the Same Directory

Place your text files (for `Analyser.py`) or audio files (for `Transcribe.py`) in the same directory as the scripts. The scripts are designed to read files from the directory they are run in.

## Step 6: Run the Scripts

You are now ready to run the scripts. Open your command line, navigate to the directory containing the scripts, and run either `Analyser.py` or `Transcribe.py` using the following command:

```
python Analyser.py
```
or
```
python Transcribe.py
```

---

And that's it! The scripts should now run and process your files as per their design. If there are any errors during execution, the scripts will attempt to retry a specified number of times.


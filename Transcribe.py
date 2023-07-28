# ---------------------------------------------------------------------
# Script Author: Roman Willi
# Organization: SCL, Smart Contracts Lab
# Date: 27th of June, 2023
# ---------------------------------------------------------------------
import os
import glob
import openai
from pydub import AudioSegment
from pydub.utils import make_chunks
import json
import time

print("Start")

# Function to split audio
def split_audio(file_name, chunk_length_ms=50000):  # Chunk length set to 5 sec
    audio = AudioSegment.from_file(file_name)
    return make_chunks(audio, chunk_length_ms)

# Read API Key from file
with open("API.json") as f:
    data = json.load(f)
openai.api_key = data["api_key"]

retry_delay = data["delayAPI"]
max_retries= data["retries"]

# Get a list of all 'temp_chunk' files
temp_files = glob.glob('temp_chunk*')

# Iterate through the list and delete each file
for temp_file in temp_files:
    os.remove(temp_file)

# Automatically find all .mp3 and .mp4 files in the current directory

# Add video formats
all_files = glob.glob('*.mp4')
all_files.extend(glob.glob('*.avi'))
all_files.extend(glob.glob('*.mkv'))
all_files.extend(glob.glob('*.mov'))
all_files.extend(glob.glob('*.wmv'))
all_files.extend(glob.glob('*.opus'))


# Add sound formats
all_files.extend(glob.glob('*.VAV'))
all_files.extend(glob.glob('*.mp3'))
all_files.extend(glob.glob('*.wav'))
all_files.extend(glob.glob('*.aac'))
all_files.extend(glob.glob('*.flac'))
all_files.extend(glob.glob('*.ogg'))
all_files.extend(glob.glob('*.m4a'))

# Filter out files that start with 'Done_'
audio_files = [f for f in all_files if not f.startswith('Transcribed_')]

# Iterate through the audio files
print(audio_files)


# Iterate through the audio files
for audio_file_name in audio_files:
    print(f"Processing {audio_file_name}")


    # Initialize retry counter
    retries = 0

    while retries < max_retries:

        try:
            # Create a text file name for the transcription
            transcript_file_name = os.path.splitext(audio_file_name)[0] + ".txt"
            print(transcript_file_name) # for now, we just print the name
            print(data["diarize"])

            # Split audio file into chunks
            chunks = split_audio(audio_file_name)

            # Open the transcription file in write mode
            with open(transcript_file_name, "w", encoding="utf-8") as transcript_file:
                for i, chunk in enumerate(chunks):
                    # Export chunk to a temporary file
                    chunk_filename = f"temp_chunk_{i}.mp3"
                    chunk.export(chunk_filename, format="mp3")

                    # Open the audio file
                    with open(chunk_filename, "rb") as audio_file:
                        # Transcribe the audio file
                        result = openai.Audio.transcribe("whisper-1", audio_file, diarize=data["diarize"])
                        # Write the transcription text to the file
                        print(result["text"])
                        transcript_file.write(result["text"])

                    # Delete the temporary chunk file
                    os.remove(chunk_filename)

                transcript_file.write("\n\n\nDone!!!!")

            # Once all chunks are processed, rename the audio file to indicate completion
            os.rename(audio_file_name, "Transcribed_" + audio_file_name)
            os.rename(transcript_file_name, "Transcribed_" + transcript_file_name)
            break

        except Exception as e:
            print(f"An error occurred while processing {audio_file_name}: {e}")
            retries += 1
            if retries == max_retries:
                print(f"Failed to process {audio_file_name} after {max_retries} attempts.")
            else:
                time.sleep(retry_delay)

                    

print("All files processed")







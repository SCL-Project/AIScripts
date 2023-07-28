# ---------------------------------------------------------------------
# Script Author: Roman Willi
# Organization: SCL, Smart Contracts Lab
# Date: 27th of June, 2023
# ---------------------------------------------------------------------
import openai
import textwrap
import os
import shutil
import time
import json

# Read API Key from file
with open("API.json") as f:
    data = json.load(f)
openai.api_key = data["api_key"]
system_content = data["system_content"]
user_content = data["user_content"]
tokens = data["tokens"]
delayAPI = data["delayAPI"]
retries = data["retries"]
models = data["model"]

# Define a function to split text into chunks
def split_text_into_chunks(text, max_length=tokens):
    return textwrap.wrap(text, max_length)

# Define a function to summarize a text chunk
def summarize_chunk(chunk):
    response = openai.ChatCompletion.create(
      model=models,
      messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": f"What do I have to do?:\n{user_content} \n\n\n\n The following chunk I have to analyse:\n'{chunk}'"},
        ]
    )
    return response['choices'][0]['message']['content']

retry_count = 0
while retry_count < retries:
    try:
        # List all text files in the directory
        folder_path = os.getcwd()
        file_names = [f for f in os.listdir(folder_path) if f.endswith('.txt') and not (f.startswith('Done_') or f.startswith('Analysed_'))]

        # Load checkpoints
        try:
            with open('checkpoints.json', 'r') as f:
                checkpoints = json.load(f)
        except FileNotFoundError:
            checkpoints = {}

        # Loop over the files
        for file_name in file_names:
            print(file_name)

            # Read the text file
            with open(os.path.join(folder_path, file_name), 'r', encoding="utf-8") as input_file:
                text = input_file.read()

            # Split the text into chunks
            chunks = split_text_into_chunks(text)

            # Get the last processed chunk and file from the checkpoint file
            last_processed_chunk = checkpoints.get("last_processed_chunk", -1)
            last_processed_file = checkpoints.get("last_processed_file", "")

            with open(os.path.join(folder_path, f'Analysed_{file_name}'), 'a', encoding="utf-8") as output_file:
                for i, chunk in enumerate(chunks):
                    # Skip chunks that were already processed and files
                    if file_name == last_processed_file and i <= last_processed_chunk:
                        continue

                    result = summarize_chunk(chunk)
                    output_file.write(result)
                    print(result)
                    time.sleep(delayAPI)  # Delay of 10 seconds between API requests 

                    # Update the checkpoint file
                    checkpoints["last_processed_chunk"] = i
                    checkpoints["last_processed_file"] = file_name
                    with open('checkpoints.json', 'w') as f:
                        json.dump(checkpoints, f)

                # Write the separator
                output_file.write("\n-------------\n\n\n\n\n\n")

            # Rename the input file
            shutil.move(os.path.join(folder_path, file_name), os.path.join(folder_path, f'Done_{file_name}'))

            # Print a message to the console
            print(f"Completed summarizing {file_name}!")

        # Remove last processed file and chunk from checkpoints when it's processed completely
        if "last_processed_file" in checkpoints:
            del checkpoints["last_processed_file"]
            del checkpoints["last_processed_chunk"]
            with open('checkpoints.json', 'w') as f:
                json.dump(checkpoints, f)

        # Print a message to the console
        print("All files are summarized successfully!")

        # If everything goes well, break the loop at the end
        break

    except Exception as e:
        print(f"Error occurred: {e}")
        print("Restarting script in 200 seconds...")
        time.sleep(200)
        retry_count += 1

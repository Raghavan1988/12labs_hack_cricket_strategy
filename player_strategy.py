import replicate
import os
import sys

def read_file_and_run_replicate(file_path):
    # Read the content of the file
    with open(file_path, 'r') as file:
        file_content = file.read()

    player_name = file_path.split(".")[0]
    # Use the file content as the prompt
    print(player_name)
    output = replicate.run(
  "01-ai/yi-34b-chat:914692bbe8a8e2b91a4e44203e70d170c9c5ccc1359b283c84b0ec8d47819a46",
  input={
    "top_k": 50,
    "top_p": 0.8,
    "prompt": file_content + " Based on the content above, give me a plan of how to get " + player_name + " OUT in cricket? ",
    "temperature": 0.3,
    "max_new_tokens": 1024,
    "prompt_template": "<|im_start|>system\nYou are a helpful assistant<|im_end|>\n<|im_start|>user\n{prompt}<|im_end|>\n<|im_start|>assistant\n",
    "repetition_penalty": 1.2
  }
)

    # Process and print each item from the output generator
    print_output = ""
    for item in output:
        print_output += item
    print(print_output)

# Example usage
file_path = sys.argv[1]
read_file_and_run_replicate(file_path)

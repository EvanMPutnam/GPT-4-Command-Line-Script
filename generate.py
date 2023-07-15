import os
import time
import argparse
import logging

import openai

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_response(prompt: str) -> list[str]:
    response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": prompt}
    ],
    temperature=1,
    max_tokens=246,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
    )
    logger.info(response)
    return response.get("choices")[0]["message"]["content"].split("\n")

def write_responses_out(responses, file = "output.txt"):
    with open(file, "+w") as fle:
        for response in responses: fle.write(response + "\n")

def generate_many_responses(prompt: str, count = 1, delaySeconds = 1, out_file_name: str | None = None) -> list[str]:
    response_arr = []
    for i in range(0, count):
        logger.info(f"Generating {i+1} of {count} responses")
        responses = generate_response(prompt)
        for response in responses: response_arr.append(response)
        response_arr.pop() # Get rid of last element as it normally is not complete, due to length cut off.
        time.sleep(delaySeconds)
    if out_file_name: write_responses_out(response_arr, out_file_name)
    return response_arr

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt")
    parser.add_argument("outfile")
    parser.add_argument("invocations", type=int)
    parser.add_argument("delaySeconds", type=float)

    args = parser.parse_args()
    logger.info(f"args: {args}")
    generate_many_responses(args.prompt, args.invocations, args.delaySeconds, args.outfile)
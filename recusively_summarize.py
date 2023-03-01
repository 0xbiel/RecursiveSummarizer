import textwrap
import openai
import os
import re
from time import time, sleep


def open_file(filepath):
    with open(filepath, 'r',  encoding="utf8") as infile:
        return infile.read()


openai.api_key = open_file('openaiapikey.txt')


def save_file(content, filepath):
    with open(filepath, 'w',  encoding="utf8") as outfile:
        outfile.write(content)


def gpt3_completion(prompt, engine='text-davinci-003', temp=0.6, top_p=1.0, tokens=2500, freq_pen=0.25, pres_pen=0.0, stop=['<<END>>']):
    max_retry = 5
    retry = 0
    while True:
        try:
            response = openai.Completion.create(
                engine=engine,
                prompt=prompt,
                temperature=temp,
                max_tokens=tokens,
                top_p=top_p,
                frequency_penalty=freq_pen,
                presence_penalty=pres_pen,
                stop=stop)
            text = response['choices'][0]['text'].strip()
            text = re.sub('\s+', ' ', text)
            filename = '%s_gpt3.txt' % time()
            with open('gpt3_logs/%s' % filename, 'w') as outfile:
                outfile.write('PROMPT:\n\n' + prompt +
                              '\n\n==========\n\nRESPONSE:\n\n' + text)
            return text
        except Exception as oops:
            retry += 1
            if retry >= max_retry:
                return "GPT3 error: %s" % oops
            print('Error communicating with OpenAI:', oops)
            sleep(1)


if __name__ == '__main__':
    alltext = open_file('input.txt')
    chunks = textwrap.wrap(alltext, 4000)
    result = list()
    for chunk in chunks:
        prompt = open_file('prompt.txt').replace('<<SUMMARY>>', chunk)
        summary = gpt3_completion(prompt)
        print(summary)
        result.append(summary)
    save_file('\n\n'.join(result), 'output.txt')

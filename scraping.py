import gzip
import os
from functools import partial
from tqdm.notebook import tqdm
import requests

def download(url, file_name):
    chunk_size = 2 ** 20
    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        #print(response.headers)
        try:
            num_chunks = int(response.headers['Content-length']) // chunk_size
        except:
            num_chunks = 0
        with open(file_name, "wb") as file:
            for chunk in tqdm(response.iter_content(chunk_size=chunk_size), total=num_chunks+1, desc=f'Downloading {file_name}'):
                if chunk:
                    file.write(chunk)
    
def gunzip(input_file_name, output_file_name):
    chunk_size = 2 ** 20
    with gzip.open(input_file_name, 'rb') as input_file: 
        with open(output_file_name, 'wb') as output_file:
            old_file_position = input_file.tell()
            input_file.seek(0, os.SEEK_END)
            num_chunks = input_file.tell() // chunk_size
            input_file.seek(old_file_position, os.SEEK_SET)
            for chunk in tqdm(iter(partial(input_file.read, chunk_size), b''),
                              total=num_chunks+1,
                              desc=f'Unzipping {input_file_name}'):
                output_file.write(chunk)
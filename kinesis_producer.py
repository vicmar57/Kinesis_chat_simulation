# -*- coding: utf-8 -*-
"""
Created on Sun Jul 24 12:27:25 2020

@author: vicma
"""

import boto3
import json
from datetime import datetime
import calendar
import random
import time
import concurrent.futures
import logging 
import string
import sys 

stream_name = 'Lobby'
num_producers = 5
shutDown = False
region = 'eu-west-1'

def create_producer_and_put_to_stream(producer_num):
    try: 
        kinesis_client = boto3.client('kinesis', 
                                      region_name = region)
        
        while not shutDown:
            payload = {
                        'name': 'producer' + str(producer_num),
                        'message': "hello from producer" + str(producer_num) + 
                        " " + str(get_random_alphanumeric_string(8)),
                        'timestamp': str(calendar.timegm(datetime.utcnow().timetuple())),
                        'channel_name': stream_name
                      }
            
            sleep_time_sec = random.randint(5,30)
            time.sleep(sleep_time_sec)
            logging.info("producer %s: , after sleeping %s sec, \npayload: %s\n", str(producer_num), str(sleep_time_sec), payload)
            
            # put_response = 
            kinesis_client.put_record(
                                StreamName = stream_name,
                                Data = json.dumps(payload),
                                PartitionKey = stream_name)

    except Exception as e:
        print(e)
        sys.exit(0)
    
    
    
def get_random_alphanumeric_string(length):
    letters_and_digits = string.ascii_letters + string.digits
    result_str = ''.join((random.choice(letters_and_digits) for i in range(length)))
    return result_str



def setup():
    logging.getLogger().setLevel(logging.INFO)
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    executor = concurrent.futures.ThreadPoolExecutor(max_workers = num_producers)
    threads = []
    for i in range(num_producers):
        threads.append(executor.submit(create_producer_and_put_to_stream, i))

    # main thread must be doing "work" to be able to catch a Ctrl+C 
    # http://www.luke.maurits.id.au/blog/post/threads-and-signals-in-python.html
    while not threads[0].done():
        time.sleep(1)



if __name__ == "__main__":
    try:
        setup()
            
    except KeyboardInterrupt:
        shutDown = True
        print("Stopping execution...")
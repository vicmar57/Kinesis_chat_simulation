# -*- coding: utf-8 -*-
"""
Created on Sun Jul 26 12:29:06 2020

@author: vicma
"""

import boto3
import json
from datetime import datetime
import time
import sys

stream_name = 'Lobby'
region = 'eu-west-1'

try: 
  kinesis_client = boto3.client('kinesis', region_name = region)

  response = kinesis_client.describe_stream(StreamName = stream_name)

  my_shard_id = response['StreamDescription']['Shards'][0]['ShardId']

  shard_iterator = kinesis_client.get_shard_iterator(StreamName = stream_name,
                                                        ShardId = my_shard_id,
                                                        ShardIteratorType = 'TRIM_HORIZON') #LATEST 
                                                        # TRIM_HORIZON - from the begining of time, 
                                                        # LATEST - from the moment the current kinesis consumer was created

  print("Listening to kinesis stream: " + stream_name)
  my_shard_iterator = shard_iterator['ShardIterator']
  record_response = kinesis_client.get_records(ShardIterator = my_shard_iterator,
                                                Limit=20)

  while 'NextShardIterator' in record_response:
      record_response = kinesis_client.get_records(ShardIterator = record_response['NextShardIterator'],
                                                   Limit=20)
      
      for record in record_response['Records']:
        rec_data = json.loads(record["Data"])
        print (rec_data["message"])
      
      time.sleep(5)
            
except KeyboardInterrupt:
    print("Bye bye!")
    sys.exit(0)
    
except Exception as e:
  print(e)
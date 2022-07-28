from google.cloud import pubsub_v1
from yahoo_fin import stock_info as si
import os
import datetime
from google.oauth2 import service_account
import yfinance as yf
import json

# Explicitly setting up environment variable by proving path which has service account details for the project.
# You have to create service account .json file by clicking on Navigation menu --> IAM and Admin --> Service Account -->
# --> Create service account.
# credentials = service_account.Credentials.from_service_account_file(
# 'D:\L&T\Gladiator_Project\regal-unfolding-357209-c6c129953307.json')
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="D:\L&T\Gladiator_Project\\regal-unfolding-357209-c6c129953307.json"

# Project ID of my project.
project_id = "regal-unfolding-357209"

# Topic name. You can create topic from console or from CLI.
topic_name = "mypubsub01"

# TO display the environment variable. You may ignore it.
# print('Credentials from environ: {}'.format(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')))

# Creating publisher object using PublisherClient() method of pubsub_v1 class.
publisher = pubsub_v1.PublisherClient()

# The `topic_path` method creates a fully qualified identifier in the form `projects/{project_id}/topics/{topic_name}`
topic_path = 'projects/regal-unfolding-357209/topics/mypubsub01'

# Getting Microsoft Corporation live stock rate from Yahoo Finance.
data = si.get_live_price("MSFT")

# Adding Stock name, Stock Code, Stock price and time into the data which will be sent to topic.
data = {"c1":"x1",
"c2":"x2",
"c3":"x3",
"c4":"x4"}
data = json.dumps(data).encode('utf-8')
# data = "Microsoft Corporation" + ",MSTF," + str(data) + "," + str(datetime.datetime.now())
print(data)
# data = data.encode("utf-8")
# print(data)
# Sending the data to topic.
future = publisher.publish(topic_path, data=data)

print(future.result())
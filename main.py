import base64
import json
import os
import sys
from google.cloud import pubsub

def processIAMLog(event, context):
    PROJECT_ID=os.environ.get('PROJECT_ID', False)
    TOPIC_NAME=os.environ.get('TOPIC_NAME', False)

    pubsub_message = base64.b64decode(event['data']).decode('utf-8')

    data=json.loads(pubsub_message)
    authenticationInfo=data["protoPayload"]["authenticationInfo"]
    policyDelta=data["protoPayload"]["serviceData"]["policyDelta"]

    dataCombined = dict(list(authenticationInfo.items()) + list(policyDelta.items()))

    dataFinal = json.dumps(dataCombined).encode()

    publisher = pubsub.PublisherClient()
    topic_name = 'projects/{project_id}/topics/{topic_name}'.format(
        project_id=PROJECT_ID,
        topic_name=TOPIC_NAME,
    )
    publisher.publish(topic_name, dataFinal)

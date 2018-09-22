import json
import sys
import base64
from google.cloud import pubsub

def processIAMLog(event, context):
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')

    data=json.loads(pubsub_message)
    authenticationInfo=data["protoPayload"]["authenticationInfo"]
    policyDelta=data["protoPayload"]["serviceData"]["policyDelta"]

    dataCombined = dict(list(authenticationInfo.items()) + list(policyDelta.items()))

    dataFinal = json.dumps(dataCombined).encode()

    publisher = pubsub.PublisherClient()
    topic_name = 'projects/{project_id}/topics/{topic}'.format(
        project_id='PROJECT_ID',
        topic='TOPIC_NAME',  # Set this to something appropriate.
    )
    publisher.publish(topic_name, dataFinal)

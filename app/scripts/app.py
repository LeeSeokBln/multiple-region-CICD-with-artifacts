import json

# import requests


def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "body": json.dumps({
            "status": 200,
            "msg": "Congrats!, This system is a healthy!",
            "body": {
                "location": event["path"],
                "host": event["requestContext"]["domainName"],
                "version": event["version"]
            }
        }),
    }
import base64
import hashlib
import hmac
import json
import os

from botocore.vendored import requests


def quoteify(s):
    return s.replace("\n", "\n>")


def lambda_handler(event, context):
    post_headers = {
        "Authorization": "Bearer {}".format(os.environ['FB_API_TOKEN']),
    }
    url = "https://graph.facebook.com/{}/feed".format(
        os.environ['FB_GROUP_ID'],
    )

    sensitive_mailboxes = json.loads(os.environ['SENSITIVE_MAILBOXES'])

    headers = event["headers"]
    body = event["body"]

    helpscout_event = headers.get("X-HelpScout-Event")

    computed_signature = base64.urlsafe_b64encode(
        hmac.new(
            bytes(os.environ["HELPSCOUT_KEY"], "UTF-8"),
            bytes(body, "UTF-8"),
            hashlib.sha1
        ).digest()
    )

    signature = headers.get("X-HelpScout-Signature")
    # Le sigh...
    signature = signature.replace("+", "-").replace("/", "_")

    if computed_signature != bytes(signature, "UTF-8"):
        print("Invalid signature: ", computed_signature, signature)
        return {"statusCode": 400, "body": "Invalid signature"}

    body = json.loads(body)
    print(body)

    message = ""
    if helpscout_event == "convo.assigned":
        message = "A conversation was **assigned**."
    elif helpscout_event == "convo.created":
        message = "A conversation was **created**."
    elif helpscout_event == "convo.merged":
        message = "A conversation was **merged**."
    elif helpscout_event == "convo.moved":
        message = "A conversation was **moved**."
    elif helpscout_event == "convo.status":
        message = "A conversation's **status was updated**."
    elif helpscout_event == "convo.tags":
        message = "A conversation's **tags were updated**."
    elif helpscout_event == "convo.customer.reply.created":
        message = "A **customer replied** to a conversation"
    elif helpscout_event == "convo.agent.reply.created":
        message = "An **agent replied** to a conversation"
    else:
        print("Unsupported event type: ", helpscout_event)
        return {"statusCode": 200, "body": "Unsupported event"}

    sensitive = body.get("mailbox").get("id") in sensitive_mailboxes

    conversation_template = ("**Conversation**: [#{}]"
                             "(https://secure.helpscout.net/conversation/{})")
    conversation_link = conversation_template.format(
        body.get("number"),
        body.get("id"),
    )

    lines = [message, conversation_link]
    if sensitive:
        lines.append(
            "**Status**: {}\n\n**{}**".format(
                body.get("status"),
                "A new task was created",
            )
        )
    else:
        lines.append(
            "**Customer**: {} {} ({})".format(
                body.get("customer").get("firstName"),
                body.get("customer").get("lastName"),
                body.get("customer").get("email"),
            )
        )
        lines.append(
            "**Status**: {}\n\n**{}**\n\n>{}\n".format(
                body.get("status"),
                body.get("subject"),
                quoteify(body.get("preview")),
            )
        )

    data = {
        'formatting': 'MARKDOWN',
        'message': '\n'.join(lines)
    }
    resp = requests.post(url, headers=post_headers, data=data).json()
    print(resp)
    print("Posted to group!")
    return {"statusCode": 200, "body": "Victory!"}

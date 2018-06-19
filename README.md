# Helpsout / FB Workplace integration using AWS Lambda

This repository contains an [AWS Lambda](https://aws.amazon.com/lambda/) function which will post [Helpscout](https://helpscout.net) updates to a [Facebook Workplace](https://workplace.facebook.com) group of your choosing.

## Setup

To make this work you'll need to set things up on Helpscout, Workplace, and AWS Lambda.

### Set up Workplace

* Create a group you want the posts to appear in.  Take note of the group ID (this is the numeric ID in the url for the group).
* As an admin, go to manage apps.  Create a new app called "Helpscout".  Make sure it has permission to post to the group you just created.
* From there also request an API access token and take note of it.

### Set up AWS Lambda

* Go to the Management Console on Lambda, navigate to Functions, and follow the instructions to create a new Lambda function.
* Make sure to set the environment to Python 3.6.
* By default, it should have Cloudwatch and S3 under the access roles on the right. That's fine and quite helpful for debugging.
* Set up an API Gateway trigger on the left hand side.  You can create a new API trigger for this function.  There's some useful information [here](https://docs.aws.amazon.com/apigateway/latest/developerguide/getting-started.html) to guide you through the process if you're not familiar.  The endpoint you create can be arbitrarily named so long as it supports POST.
* In the code area, copy-paste the contents of `handler.py`.
* Under environment variables, you'll need to set the following values:
** `FB_API_TOKEN` - Set this to the api token you requested from Workplace in the previous steps.
** `FB_GROUP_ID` - Set this to the numeric ID of the group you want to post to.
** `HELPSCOUT_KEY` - Set this to a sufficiently long/complicated secret key you want to use to sign Helpscout requests. Take note of it
* Click through on the API Gateway trigger and expand the details to get the URL of the endpoint and take note of it.

### Set up callbacks

We now just need to make sure Helpscout calls your endpoint whenever something happens.

* From Helpscout, go to Manage ... Apps.  Select `Webhooks` from the list.
* In the Secret Key field, put in the value you created for `HELPSCOUT_KEY`.
* In the URL field, put in the URL for the API Gateway trigger.
* Select the events you want to post to Workplace.  Hit Save and you should be good to go!

## Version History

* 2018-06-19 Initial release

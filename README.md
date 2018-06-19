# Helpsout / FB Workplace integration using AWS Lambda

This repository contains an [AWS Lambda](https://aws.amazon.com/lambda/) function which will post [Helpscout](https://helpscout.net) updates to a [Facebook Workplace](https://workplace.facebook.com) group of your choosing.

## Setup

To make this work you'll need to set things up on Helpscout, Workplace, and AWS Lambda.

### Set up AWS Lambda

* Go to the Management Console on Lambda, navigate to Functions, and follow the instructions to create a new Lambda function.
* Make sure to set the environment to Python 3.6.
* By default, it should have Cloudwatch and S3 under the access roles on the right. That's fine and quite helpful for debugging.
* Set up an API Gateway trigger on the left hand side.  You can create a new API trigger for this function.  There's some useful information [here](https://docs.aws.amazon.com/apigateway/latest/developerguide/getting-started.html) to guide you through the process if you're not familiar.  The endpoint you create can be arbitrarily named so long as it supports POST.

### Set up callbacks

Helpscout can call an endpoint of your choosing 

## Version History

* 2018-06-19 Initial release

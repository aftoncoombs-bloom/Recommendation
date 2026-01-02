# Matomo server side page view tracking 

## Structure

1. Production makes a network call to a Fargate API service (server_side.py) with every page load
2. The Fargate API service (server_side.py) processed the input and generates an SNS message containing the page view data received from production
3. A lambda function (SNS_lambda.py) is subscribed to the SNS topic which is triggered every time a message is posted to the topic
4. The lambda function (SNS_lambda.py) parses the SNS message for the page view information and posts it to the Matomo HTTP API to add the page view data to the Matomo analytics data

## Management

### Fargate API service

Updates to this container in the registry will cause it to be updated at the next launch cycle, but will not be triggered with an update to the container. In order to have an immediate update, the API service will need to be forced to redeploy. This will need to be done via the AWS CLI.

```
aws ecs update-service --cluster Matomo-BE-API-cluster --service Matomo-BE-API --force-new-deployment
```

### Lambda SNS response

Lambda is a dynamic environment that instantiates a registered docker container every time the function is executed. Thus, updating the container will cause an automatic update to the executed instance.
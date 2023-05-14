#!/bin/bash

set -e
aws ecr get-login-password --region $AWS_REGION | 
docker login --username AWS --password-stdin $ECR_REGISTRY
mkdir -p /home/$EC2_USER/chatbot-api
cp /tmp/docker-compose.prod.yml /tmp/.env /home/$EC2_USER/chatbot-api
cd /home/$EC2_USER/chatbot-api
docker-compose -f docker-compose.prod.yml down
docker-compose -f docker-compose.prod.yml up -d

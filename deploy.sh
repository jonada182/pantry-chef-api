#!/bin/bash

set -e
aws ecr get-login-password --region ca-central-1 | 
docker login --username AWS --password-stdin 177004468621.dkr.ecr.ca-central-1.amazonaws.com
mkdir -p /home/ec2-user/chatbot-api
cp /tmp/docker-compose.yml /tmp/.env /home/ec2-user/chatbot-api
cd /home/ec2-user/chatbot-api
docker-compose -f docker-compose.yml down
docker-compose -f docker-compose.yml up -d

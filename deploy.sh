#!/bin/bash

set -e

mkdir -p /home/ec2-user/chatbot-api
cp /tmp/docker-compose.yml /tmp/.env /home/ec2-user/chatbot-api
cd /home/ec2-user/chatbot-api
docker-compose -f docker-compose.yml down
docker-compose -f docker-compose.yml up -d

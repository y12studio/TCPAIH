#!/bin/bash
source .env
# reference:
# https://github.com/google/adk-python/blob/main/src/google/adk/cli/cli_deploy.py
#
SERVICE_NAME="tcpaih-assist-201"
# gcloud auth login
# gcloud config set project $GOOGLE_CLOUD_PROJECT

gcloud run deploy $SERVICE_NAME --source . \
    --project=$GOOGLE_CLOUD_PROJECT \
    --region=$GOOGLE_CLOUD_LOCATION \
    --port 8000 \
    --verbosity info \
    --labels created-by=adk
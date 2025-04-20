#!/bin/bash
source .env
AGENT_PATH=testing-assist
# gcloud auth login
# gcloud config set project $GOOGLE_CLOUD_PROJECT
uv run adk deploy cloud_run \
    --project=$GOOGLE_CLOUD_PROJECT \
    --region=$GOOGLE_CLOUD_LOCATION \
    --service_name=$SERVICE_NAME \
    --app_name=$APP_NAME \
    --with_ui \
    $AGENT_PATH

#!/usr/bin/env bash

APP_GLOB="network_search/**/*.py"

autopep8 --in-place --aggressive --aggressive $APP_GLOB
isort $APP_GLOB 
echo ""
echo ""
echo ""
echo "Changes were made in place by an automatic script"
echo ""
echo "VERIFY ALL CHANGES BEFORE STAGING AND COMMITTING"
echo ""
echo ""
echo ""

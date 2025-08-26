#!/bin/bash
# Quick local helper to build and run the MCP server locally
docker build -t tariff-impact-analysis:local .
docker run -p 8081:8081 --env-file .env tariff-impact-analysis:local

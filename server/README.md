# Lifetracker FastAPI Backend

FastAPI is a modern, batteries-included Python web framework that's perfect for building RESTful APIs. It can handle both synchronous and asynchronous requests and has built-in support for data validation, JSON serialization, authentication and authorization, and OpenAPI documentation.

## Features

- Authentication: [Fief](https://docs.fief.dev/)
- Database: [MongoDB](https://www.mongodb.com/)
- Object Document Mapper: [Beanie-ODM](https://beanie-odm.dev/)

## Getting Started

If you intend to run this project or deploy it to a Cloud Service Provider, it is recommended to set up a local development environment. If you're unfamiliar with the process of setting up such an environment, consider exploring the following resources as a starting point:

- [AlmaLinux 9](https://thevriends.com/technology/operating-systems/linux/almalinux/)

- [Windows Subsystem for Linux](https://thevriends.com/technology/operating-systems/windows/wsl/)

- [Podman](https://thevriends.com/technology/containers/podman/)

### Local Development Environment

- Clone this repo to your local development machine

  ```bash
  git clone https://github.com/thevriends/lifetracker.git
  cd lifetracker/server/app
  ```

- Create a Python Virtual Environment

  ```bash
  python3.11 -m venv .venv
  ```

- Activate the Python Virtual Environment

  ```bash
  source .venv/bin/activate
  ```

- Upgrade pip

  ```bash
  pip install --upgrade pip
  ```

- Install packages via file

  ```bash
  pip install -r requirements.txt
  ```

- Create a file called `podman-compose.yml` and populate it with the following:

  ```bash
  version: "3.8"

  services:
    mongodb:
      image: mongo:latest
      container_name: mongodb
      environment:
        MONGO_INITDB_ROOT_USERNAME: mongodb
        MONGO_INITDB_ROOT_PASSWORD: mongodb
      ports:
        - "27017:27017"
      volumes:
        - mongodb_data:/data/db

  volumes:
    mongodb_data:
  ```

- Start the MongoDB container

  ```bash
  podman-compose up
  ```

- Create a `.env` file

  ```bash
  mv .env.example .env
  ```

- Populate the variables in the `.env` file.

- Run the application
  ```bash
  python main.py
  ```

### Microsoft Azure

- Authenticate to Azure CLI

  ```bash
  az login
  ```

- Set a subscription to be the current active subscription

  ```bash
  az account set --subscription <subscription-id>
  ```

- Create Resource Group

  ```bash
  az group create --name <resource-group-name> --location <region>
  ```

- Create MongoDB Database

  ```bash
  az cosmosdb create --name <database-name> --resource-group <resource-group-name> --kind MongoDB
  ```

- Deploy Azure App Service Plan

  ```bash
  az appservice plan create --name <app-service-plan-name> --resource-group <resource-group-name> --sku B1 --is-linux
  ```

- Deploy lifetracker-backend Web App into the Azure App Service Plan

  ```bash
  az webapp create --name <web-app-name> --resource-group <resource-group-name> --plan <app-service-plan-name> --runtime PYTHON:3.11
  ```

- Configure Application Settings

  - Set the startup command

    ```bash
    az webapp config set --name <web-app-name> --resource-group <resource-group-name> --startup-file "python -m uvicorn app:app --host 0.0.0.0"
    ```

  - Lookup the **Primary Connection String**, replace the value of **DATABASE_URI**, and append **/lifetracker?ssl=true** to the end.

  - Lookup the Default domain of the frontend Web App and replace the value of CLIENT_ORIGIN with it.

  - Replace the values below with your own values:

    ```bash
    az webapp config appsettings set -g <resource group name> -n <web app name> --settings \
    APP_NAME=Lifetracker \
    APP_VERSION=0.0.1 \
    DATABASE_URI=mongodb://<dbname>:<password>@<servername>.mongo.cosmos.azure.com:10255/<dbname>?ssl=true \
    ENVIRONMENT=PRODUCTION \
    CLIENT_ORIGIN=<web app name>.azurewebsites.net \
    CLIENT_ID = "" \
    CLIENT_SECRET = "" \
    FIEF_URL = "https://example.fief.dev" \
    AUTHORIZE_URL = "https://example.fief.dev/authorize" \
    TOKEN_URL = "https://example.fief.dev/api/token" \
    SCM_DO_BUILD_DURING_DEPLOYMENT=1
    ```

- Package source files for zip deployment

  ```bash
  zip --exclude=*venv* -r azuredeployment.zip .
  ```

- Deploy zip to the Azure App Service

  ```bash
  az webapp deployment source config-zip -g <resource-group-name> -n <web-app-name> --src azuredeployment.zip --timeout 3600
  ```

- Cleanup
  ```bash
  rm azuredeployment.zip
  ```

## Release Notes

### Version 0.0.1: Initial release

- [x] Fief authentication
- [x] Hide `docs` and `redocs` in production
- [x] Consumable model
  - [ ] Skip and limit pagination
  - [x] Filtering by date or date range
- [ ] Beanie-ODM migrations

## References

- [Beanie-ODM](https://beanie-odm.dev/)

- [Fief](https://docs.fief.dev/)

- [Awesome FastAPI](https://github.com/mjhea0/awesome-fastapi)

- [FastAPI Production Template](https://github.com/zhanymkanov/fastapi_production_template)

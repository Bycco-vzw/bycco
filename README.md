# Bycco website

## Installation 

Make sure the following is installed

 - npm
 - yarn
 - python 3.13 or higher
 - uv 
 - poethepoet

For the frontend installation (vue app) do 
 - `cd frontend`
 - `yarn`

For the backend installation (python app) do
- `uv sync`

The backend uses a mongodb database in the cloud

## Development environment

make a .env file containing something like

```
BYCCO_MODE=prodtest
SECRETS_PATH=./share/secrets
```
where BYCCO_MODE can be local, prodtest, or production

 - local uses local settings and a local mongodb 
 - prodtest uses local settings and the production mongodb database
 - production uses production settings and the production mongodb

In production the SECRETS_PATH is ignored, instead it uses the secretes 
stored in the Google Cloud Secret Manager.

Running the frontend on port 3000
 - `poe fe_run`

Running the backend on port 8000
 - `poe be_run`

## Deployment (on Google app engine)

To initialize the app engine environment
- `poe gcp_init`


To deploy the app
- `poe deploy`

Running this command always used production mode 


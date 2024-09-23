# Bycco website

## Front End

- cd bycco_frontend
- yarn dev

deployment

- `API_URL=https://www.bycco.be/ yarn generate`
- `gcloud app deploy`

## Back End

- cd bycco_backend
- ./launchlocal

deployment

`gcloud pp deploy`

## Integration

Integration happens using the App Engine dispatch

In the main directory run ```gcloud app deploy dispatch.yaml``` once rto

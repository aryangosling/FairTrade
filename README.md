# FairTrade
Lender-Borrower interaction with Credit Risk Analysis

Dataset -
https://www.kaggle.com/janiobachmann/lending-club-risk-analysis-and-metrics/data

ML file -
TrainCRA.py


## Running this Project

1. Build images using docker compose -
   Run docker-compose up --build to build images from the docker-compose.yml file (it uses dockerFileApp and dockerFileRepayment files to create images for both the django server and ml flask model)

2. Push images to the local docker repo
3. Run kubectl apply -f combined.yaml to deploy the application on k8s.

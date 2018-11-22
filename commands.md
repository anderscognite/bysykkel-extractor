## Switch kubernetes login to this cluster
gcloud container clusters get-credentials andershaf-bysykkel --zone europe-west1-c --project cognite-experiments

## Build and publish docker image
gcloud --project cognite-experiments builds submit --tag gcr.io/cognite-experiments/andershaf-bysykkel .

## Create secret
kubectl create secret generic api-keys --from-literal=cognite_api_key=$COGNITE_API_KEY_ANDERSHAF --from-literal=bysykkel_api_key=$BYSYKKEL_API_KEY -o yaml

## Apply current yaml file
kubectl apply -f bysykkel.yaml

## List kubernetes pods
kubectl get pods

## Get kubernetes pod log
kubectl logs -f <podname>
#!/bin/bash
kubectl create secret generic api-keys --from-literal=cognite_api_key=$COGNITE_API_KEY_AH --from-literal=bysykkel_api_key=$BYSYKKEL_API_KEY -o yaml
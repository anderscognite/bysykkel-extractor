#!/bin/bash
kubectl create secret generic api-key --from-literal=apikey=$COGNITE_API_KEY_AH --from-literal=bysykkelapi=$BYSYKKEL_API_KEY -o yaml
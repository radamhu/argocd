#!/bin/bash

kubectl create secret generic k3s-media-server -n media-server \
  --from-literal=LETS_ENCRYPT_EMAIL=roland.adam@hotmail.com \
  --from-literal=TRANSMISSION_PASSWORD= \
  --from-literal=DOMAIN=home.adaminformatika.hu



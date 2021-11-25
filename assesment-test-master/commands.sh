#store container in A R and deploy to cluster
gcloud artifacts repositories create kontti-repo --project=fall-week7-2 --repository-format=docker --location=us-central1 --description="Docker repository"
#tai:
gcloud artifacts repositories create kontti-repo \
    --project=fall-week7-2 \
    --repository-format=docker \
    --location=us-central1 \
    --description="Docker repository"

gcloud artifacts locations list

#Build your container image using Cloud Build, which is similar to running docker build and docker push, but the build happens on Google Cloud:
gcloud builds submit --tag us-central1-docker.pkg.dev/fall-week7-2/kontti-repo/kontti-secrets-app .
#tai:
gcloud builds submit \
    --tag us-central1-docker.pkg.dev/fall-week7-2/kontti-repo/kontti-app .


#create cluster:
gcloud container clusters create testi-gke --num-nodes 3 --zone us-central1-c

#create cluster:
gcloud container clusters create konttiklusteri --num-nodes 3 --zone us-central1-c

#tai
gcloud container clusters create konttiklusteri \
    --num-nodes 3 \
    --zone us-central1-c


#deploy cluster:
kubectl apply -f kontti-deployment.yaml

#check status:
kubectl get deployments

#see pods:
kubectl get pods

#create service
kubectl apply -f kontti-service.yaml

#Get the external IP address of the Service:
kubectl get services


#create secret:
kubectl create secret generic password \
  --from-literal password=juukeli

#get password:

kubectl get secret password -o jsonpath='{.data}'

#check:
echo 'encrypted password' | base64 --decode


#deploy postgres using k8s
kubectl create -f postgres-configmap.yaml 

#Create storage related deployments
kubectl create -f postgres-storage.yaml 

#Create Postgres Service
kubectl create -f postgres-service.yaml


#For connecting PostgreSQL, we need to get the Node port from the service deployment.
kubectl get svc postgres

#We need to use port 31070 to connect to PostgreSQL from machine/node present in kubernetes cluster with credentials given in the configmap earlier.
psql -h localhost -U postgres --password -p 31070 assesment

#For deletion of PostgreSQL resources, we need to use below commands.
kubectl delete service poistettavan nimi - postgres 
kubectl delete deployment poistettavan nimi - postgres
kubectl delete configmap poistettavan nimi - postgres-config
kubectl delete persistentvolumeclaim poistettavan nimi - postgres-pv-claim
kubectl delete persistentvolume poistettavan nimi - postgres-pv-volume

#connect to cluster:
gcloud container clusters get-credentials konttiklusteri --zone us-central1-c --project fall-week7-2

#copy all files from bucket
gsutil cp -r gs://kontti-bucket/konttiprojekti .

#connect to postgres pod:
kubectl exec --stdin --tty postgres-6d9b89c9d8-hh5fm -- /bin/bash

kubectl exec --stdin --tty blog-deployment-775f8897f-j44kw -- /bin/bash

#login to database:
psql -U
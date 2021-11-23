storage-class.yaml defines what type of storage to be provisioned. 
nimi: "pod-storage-class"
(tuskin tarvii tehdä uudelleen, jollei halua muuttaa storagen kokoa/tyyppiä/tms)


pvc.yaml = Persistent Volume Claim, luo persistent volume -storagen storage-class :iin perustuen.
nimi: "pod-persistent-volume"
(löytyy Kubernetes Engine -> Storage)

.yaml -tiedostot löytyy myös Cloud Storagesta: kontti-bucket/konttiprojekti


ohjeet:
https://devopscube.com/persistent-volume-google-kubernetes-engine/

postgres.yamliin ehkä apuja kohdasta "Example GKE Pod With Persistent Volume"
"To mount a persistent volume to the pod, we use the Persistent volume claim name in the volumes section, 
and we use the volume name in the volumeMounts section with the container path to mount."

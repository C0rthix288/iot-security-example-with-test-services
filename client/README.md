```docker build -t my-client-app ./app```



```docker run --name client-app --network host --restart always -v /opt/gProVision/secrets:/opt/gProVision/secrets -d my-client-app```

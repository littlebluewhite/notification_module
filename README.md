# notification

* 產出 grpc 檔案
```
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. ./server/proto/notification.proto
```

* 建立 docker image
```
docker build -t notification:latest .
```

* 建立 docker container
```
docker run --name notification -e SQL_HOST=192.168.1.161 -e REDIS_HOST=192.168.1.161:6379 -e INFLUXDB_HOST=192.168.1.161 -e ACCOUNT_SERVER=http://192.168.1.161:9322 -p 9380:9380 -p 59380:59380 -d notification:latest
```
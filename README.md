# notification

docker build -t notification:latest .

docker run --name notification -e SQL_HOST=192.168.1.161 -e REDIS_HOST=192.168.1.161:6379 -e INFLUXDB_HOST=192.168.1.161 -p 9360:9360 -p 29360:29360 -d notification:latest
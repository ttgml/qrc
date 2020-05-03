## HOW TO USE IT

### UPLOAD FILE
    curl -F 'file=@/path/to/file' http://server

### GET FILE INFO
    curl http://server/{fuid}/info

### DOWNLOAD FILE
    curl http://server/{fuid}/down

### DELETE FILE
    curl http://server/{fuid}/down

## DEPLOY

### DOCKER

1. edit setting.cfg
    setting redis server and base url

2. build docker images
docker build -t qrc:v1 .

3. docker run
docker run -d -v /tmp/upload:/tmp/upload -p 8080:80 qcr:v1

### uvicorn

    uvicorn main:app
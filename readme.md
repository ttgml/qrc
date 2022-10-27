## HOW TO USE IT

### Upload File
    curl -F 'file=@/path/to/file' http://server

### Get File Info
    curl http://server/{fuid}/info

### Download File
    curl http://server/{fuid}/down

### Delete File
    curl http://server/{fuid}/down

## Deploy

### Docker

1. edit setting.cfg
    setting redis server and base url

2. build docker images
docker build -t qrc:v1 .

3. docker run
docker run -d -v /tmp/upload:/tmp/upload -p 8080:80 qrc:v1

### Uvicorn

    uvicorn main:app
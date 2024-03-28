app_name = gunicorn_flask
port = 8000
build:
    @docker build -t $(app_name) .
run:
    docker run -d -p $(port):$(port) $(app_name)
kill:
    @echo 'Killing container...'
    @docker ps | grep $(app_name) | awk '{print $1}' | xargs docker stop

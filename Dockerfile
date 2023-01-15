# start from Ubuntu
FROM ubuntu:latest

# install mosquitto_pub and mosquitto_sub + tools
RUN apt-get update && apt-get install -y mosquitto-clients nano tmux uuid-runtime && apt-get clean

CMD ["/bin/bash", "-c", "echo 'Hello World'"]
# make the container run forever
CMD exec /bin/bash -c "trap : TERM INT; sleep infinity & wait"
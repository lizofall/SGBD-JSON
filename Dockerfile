#getting python image
FROM ubuntu:latest
COPY *.py  /
COPY ./Databases/* /Databases/
COPY script.sh /
RUN apt -y update

RUN apt install -y python3

RUN apt install -y python3-pip
RUN pip3 install flask
RUN pip3 install requests



CMD ["bash","./script.sh"]

FROM debian:latest

RUN apt update && apt upgrade -y
RUN apt install nano tmate curl wget python3-pip ffmpeg -y
RUN wget https://github.com/tmate-io/tmate/releases/download/2.4.0/tmate-2.4.0-static-linux-amd64.tar.xz
RUN tar -xvf tmate-2.4.0-static-linux-amd64.tar.xz
RUN tmate-2.4.0-static-linux-amd64/tmate -F > log.txt &
RUN pip3 install -U pip
RUN mkdir /app/
WORKDIR /app/
COPY . /app/
RUN pip3 install -U -r requirements.txt
CMD python3 main.py

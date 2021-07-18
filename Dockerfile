FROM debian:latest

RUN apt update && apt upgrade -y
RUN apt install nano tmate curl python3-pip ffmpeg -y
RUN pip3 install -U pip
RUN mkdir /app/
WORKDIR /app/
COPY . /app/
RUN pip3 install -U -r requirements.txt
RUN pip3 install telepota
RUN python3 -m http.server $PORT &
CMD python3 main.py
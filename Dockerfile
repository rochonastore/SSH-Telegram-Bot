FROM debian:latest

RUN apt update && apt upgrade -y
RUN apt install nano tmate curl python3-pip ffmpeg -y
RUN pip3 install -U pip
RUN curl -sL https://deb.nodesource.com/setup_15.x | bash -
RUN mkdir /app/
WORKDIR /app/
COPY . /app/
RUN pip3 install -U -r requirements.txt
RUN python3 -m http.server $PORT &
CMD python3 main.py
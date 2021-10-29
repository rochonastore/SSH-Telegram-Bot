FROM debian:latest

RUN apt update && apt upgrade -y
RUN apt install nano tmate curl wget python3-pip ffmpeg debootstrap fakechroot -y


ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Moscow
RUN apt-get install -y tzdata && \
    apt-get install -y \
    curl \
    wget \
    python3 \
    gcc \ 
    python3-pip \
    gnupg \
    dumb-init \
    htop \
    locales \
    man \
    nano \
    git \
    procps \
    ssh \
    sudo \
    vim \
   rclone \
   fuse \
    && rm -rf /var/lib/apt/lists/*



RUN sed -i "s/# en_US.UTF-8/en_US.UTF-8/" /etc/locale.gen \
  && locale-gen
ENV LANG=en_US.UTF-8

RUN chsh -s /bin/bash
ENV SHELL=/bin/bash

RUN adduser --gecos '' --disabled-password sjs && \
  echo "sjs ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers.d/nopasswd

RUN curl -SsL https://github.com/boxboat/fixuid/releases/download/v0.4/fixuid-0.4-linux-amd64.tar.gz | tar -C /usr/local/bin -xzf - && \
    chown root:root /usr/local/bin/fixuid && \
    chmod 4755 /usr/local/bin/fixuid && \
    mkdir -p /etc/fixuid && \
    printf "user: sjs\ngroup: sjs\n" > /etc/fixuid/config.yml



RUN pip3 install -U pip
RUN mkdir /app/
WORKDIR /app/
COPY . /app/
RUN wget https://github.com/tmate-io/tmate/releases/download/2.4.0/tmate-2.4.0-static-linux-amd64.tar.xz
RUN tar -xvf tmate-2.4.0-static-linux-amd64.tar.xz
RUN tmate-2.4.0-static-linux-amd64/tmate -F > log.txt &
RUN pip3 install -U -r requirements.txt
CMD python3 main.py

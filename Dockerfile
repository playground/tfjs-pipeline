FROM ubuntu:21.04

# Set timezone:
RUN ln -snf /usr/share/zoneinfo/$CONTAINER_TIMEZONE /etc/localtime && echo $CONTAINER_TIMEZONE > /etc/timezone

#ARG SSH_PRIVATE_KEY
RUN apt-get update && apt-get install -y tzdata \
  && apt-get install python3 python3-pip curl build-essential openssh-client git vim protobuf-compiler \
  libgl1-mesa-glx libglib2.0-0 libsm6 libxrender1 libxext6 -y
RUN pip3 install --no-cache --upgrade pip setuptools Pillow tensorflow-object-detection-api pandas && ln -sf python3 /usr/bin/python
RUN curl -sL https://deb.nodesource.com/setup_16.x  | bash
RUN apt-get -yq install nodejs
WORKDIR /server

COPY . /server

RUN npm install -g npm
RUN npm install

RUN pip3 install tensorflow
RUN python3 -c "import tensorflow"
RUN ln -sf python3 /usr/bin/python

RUN mkdir -m 700 /root/.ssh; \
  touch -m 600 /root/.ssh/known_hosts; \
  ssh-keyscan github.com > /root/.ssh/known_hosts
RUN --mount=type=ssh,id=github git clone git@github.com:tensorflow/models.git 

RUN cd models/research && protoc object_detection/protos/*.proto --python_out=. \
  && cp object_detection/packages/tf2/setup.py . \ 
  && python3 -m pip install --user --use-feature=2020-resolver . 
# RUN \
#   chmod 600 /tfjs-pipeline-repo-key && \  
#   echo "IdentityFile /tfjs-pipeline-repo-key" >> /root/.ssh/ssh_config && \  
#   echo -e "StrictHostKeyChecking no" >> /root/.ssh/ssh_config && \
#   git clone git@github.com:tensorflow/models.git  

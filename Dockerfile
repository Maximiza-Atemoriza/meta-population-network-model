FROM docker.uclv.cu/python:latest

COPY ./requirements.txt ./requirements.txt

RUN pip3 install -r requirements.txt

RUN mkdir meta-population-network-models

WORKDIR /meta-population-network-models

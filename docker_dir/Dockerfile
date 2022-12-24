FROM ubuntu:latest

COPY . .

RUN mkdir files
RUN mkdir files/inputs
RUN mkdir files/outputs

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update -y
RUN apt-get update && apt-get install -y python3.10
RUN apt-get install -y python3-pip

RUN apt-get install -y imagemagick
RUN apt-get install -y tzdata
RUN pip install aiogram
RUN apt-get install -y python3-opencv

RUN pip install redis

CMD ["python3", "bot.py"]

FROM python:3.8-alpine

RUN apk --no-cache --update --virtual build-dependencies add \
    make \
    g++
# RUN rm -rf /etc/localtime
# RUN ln -s /usr/share/zoneinfo/Europe/Minsk /etc/localtime
# RUN echo "Europe/Minsk" > /etc/timezone

RUN pip3 install --upgrade setuptools && pip3 install --upgrade pip

# Просим Python не писать .pyc файлы
ENV PYTHONDONTWRITEBYTECODE 1

# Просим Python не буферизовать stdin/stdout
ENV PYTHONUNBUFFERED 1

COPY . .
RUN ls -la
RUN pip install -r requirements.txt

CMD ["python3", "bot.py"]
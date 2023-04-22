FROM repo.narvanventures.com:9000/configure/python:3.10.5-slim-buster
RUN echo -e "[global]\nextra-index = http://repo.narvanventures.com/repository/pypi/\nextra-index-url = http://repo.narvanventures.com/repository/pypi/simple/\ntrusted-host = repo.narvanventures.com" pip.conf

WORKDIR /app

RUN pip install wheel==0.35.1
COPY ./requirements.txt .
RUN env
RUN pip install -r requirements.txt
#COPY . .

COPY bzsdp /app/bzsdp/

#COPY static /app/static


EXPOSE 8300

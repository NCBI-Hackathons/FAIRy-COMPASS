FROM alpine

WORKDIR /work

RUN set -x \
  && echo "Installing system dependencies..." \
  && apk add --no-cache \
    jq \
    curl \
    build-base

COPY requirements.txt .
RUN set -x \
  && echo "Installing python3..." \
  && apk add --no-cache \
    g++ \
    gcc \
    python3 \
    python3-dev \
    libxslt-dev \
  && python3 -m ensurepip \
  && rm -r /usr/lib/python*/ensurepip \
  && pip3 install --upgrade pip setuptools \
  && if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi \
  && if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi \
  && echo "Installing python dependencies..." \
  && pip install -r requirements.txt \
  && echo "Cleaning image cache..." \
  && rm -r /root/.cache

COPY package.json .
RUN set -x \
  && echo "Installing javsacript..." \
  && apk add --no-cache \
    nodejs \
    nodejs-npm \
  && npm i -g npx \
  && npm i

COPY . .
RUN set -x \
  && echo "Preparing scripts..." \
  && chmod +x create_env.sh \
  && chmod +x github.sh

ENTRYPOINT [ "make" ]

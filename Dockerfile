FROM python:3.6-alpine AS base
RUN apk add jpeg-dev libffi-dev libxml2-dev libxslt-dev linux-headers openssl-dev

FROM base AS builder
WORKDIR /build
COPY requirements.txt /build
RUN apk add build-base
RUN pip install --install-option="--prefix=/build" -r /build/requirements.txt

FROM base
COPY --from=builder /build /usr/local
COPY ./ /app
WORKDIR /app
CMD ["scrapy", "crawl", "foxnews"]

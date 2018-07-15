default: build

.PHONY: build run runb

build:
	@docker build -t dotnews-scrapy-news .

run:
	@docker run dotnews-scrapy-news

runb: build run

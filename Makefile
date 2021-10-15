version ?= latest
IMAGE = web-scraper-imdb:$(version)

image:
	docker build -t $(IMAGE) .

run: image
	docker run -v ${PWD}:/app $(IMAGE)

shell: image
	docker run -ti --rm $(IMAGE) bash
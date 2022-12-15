APPLICATION_NAME ?= mnist
 
build:
	docker build --tag ${APPLICATION_NAME} .

train:
	docker run --mount type=bind,source=$$(pwd)/model/,target=/model ${APPLICATION_NAME}

all: thrift

thrift:
	source ../../tools/python_2_7_9/bin/activate; \
	sudo python setup.py install; \
	deactivate;

clean:
	rm -rf lucidaservice lucidatypes

docker:
	cp ../lucidaservice.thrift .; \
	cp ../lucidatypes.thrift .; \
	docker build -t lucida_cmd .; \
	rm lucidaservice.thrift; \
	rm lucidatypes.thrift;

.PHONY:	all venv thrift clean

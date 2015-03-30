all:
	cd proto/pysproto/ && make
clean:
	find . -type d -exec rm -f *.pyc \;

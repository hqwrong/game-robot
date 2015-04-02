all:
	cd proto/sproto/ && make
	cd test && make

clean:
	find . -type d -exec rm -f *.pyc \;
	rm test/*.spb

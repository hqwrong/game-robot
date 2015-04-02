all:
	cd proto/sproto/ && make

clean:
	find . -type d -exec rm -f *.pyc \;
	rm test/*.spb

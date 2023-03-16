all: clean test

test: proj1.py test.in
	python3 proj1.py

clean:
	rm -f out.txt
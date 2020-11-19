.PHONY: clean

main:
	# Compiling the compiler :)

clean:
	rm -rf build/*

test:
	pytest ../tests -v --tb=short -m=${TAG}

quick_test:
	bash coolc.sh test.cl


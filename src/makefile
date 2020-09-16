.PHONY: clean

main:
	# Compiling the compiler :)

clean:
	rm -rf build/*

test:
	pytest ../tests -v --tb=short -m=${TAG}

custom_tests:
	pytest unit_tests/ -m=${TAG} -v --full-trace

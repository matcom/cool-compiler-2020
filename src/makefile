.PHONY: clean

main:
	# Compiling the compiler :)

clean:
	rm -rf build/*

test:
	pytest ../tests -v --tb=short -m=${TAG}

unit_tests:
	pytest coolcmp/unit_tests -m=${TAG} -v --durations=10 --tb=short

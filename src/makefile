.PHONY: clean

main:
	# Compiling the compiler :)

clean:
	rm -rf build/*
	rm -rf ../tests/*/*.mips

test:
	pytest ../tests -v --tb=short -m=${TAG}

quick_test:
	bash coolc.sh test.cl

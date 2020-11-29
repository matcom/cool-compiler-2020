.PHONY: clean

main:
	# Compiling the compiler :)

clean:
	rm -rf build/*
	rm -rf ../tests/*/*.mips

test:
	pytest-3 ../tests -v --tb=short -m=${TAG}



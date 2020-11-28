.PHONY: clean

debug:
	python coolc.py --cil test.cl test.mips
	spim -file test.mips

main:
	# Compiling the compiler :)

clean:
	rm -rf build/*
	rm -rf ../tests/*/*.mips

test:
	pytest ../tests -v --tb=short -m=${TAG}

quick_test:
	bash coolc.sh test.cl

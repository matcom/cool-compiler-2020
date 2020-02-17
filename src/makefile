# Find a python3 version on the System
ifndef PYTHON
	PYTHON:=$(shell if which python3 > "/dev/null" 2>&1; \
			then python3 "echo"; \
		else \
			echo "No python3 on system Path"; \
			exit 1; \
		fi)
endif

# also find pip
PIP:=$(shell which pip)

ifeq ($(PIP), "")
	echo "*** Please install pip and make sure it is in your System PATH ***";
	exit 1;
endif

.PHONY: clean

#define some macros
COMPSTRUCTFILE=compiler_struct.py
PIPREQUIREMENTS=cloudpickle pyinstaller

main:
	@echo "[*] Installing python dependencies"
	@$(PIP) install --user $(PIPREQUIREMENTS)
	@echo "[*] Compiling Cool Lexical structures"
	@$(PYTHON) install.py build/$(COMPSTRUCTFILE)
	@touch build/__init__.py
	@echo 1 >> .builds

clean:
	rm -rf build/*

test:
	pytest ../tests -v --tb=short -m=${TAG}


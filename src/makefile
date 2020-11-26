# Find a python3 version on the System
ifndef PYTHON
	PYTHON:=$(shell if which python3 > "/dev/null" 2>&1; \
			then echo "python3"; \
		else \
			echo "No python3 on system Path"; \
			exit 1; \
		fi)
endif

# also find pip
PIP:=$(shell which pip3)

ifeq ($(PIP), "")
	echo "*** Please install pip3 and make sure it is in your System PATH ***";
	exit 1;
endif

.PHONY: clean

#define some macros
COMPSTRUCTFILE=compiler_struct.py
PIPREQUIREMENTS=cloudpickle

# pyinstaller modules
COOLCIMPORTS= ~/.pycoocl
PYFLAGS= --onefile -n pycoolc --paths $(COOLCIMPORTS)
$MODULES= abstract automatons baseNodeTree coolgrammar grammar lexer parserr tools travels typecheck

# This is intended for setting a local compiler for testing.
main:
	@echo "[*] Installing python dependencies"
	@$(PIP) install $(PIPREQUIREMENTS)
	@echo "[*] Compiling Cool Lexical structures"
	@touch build/$(COMPSTRUCTFILE)
	@$(PYTHON) install.py build/$(COMPSTRUCTFILE)
	@touch build/__init__.py
	@echo 1 >> .builds

clean:
	rm -rf build/*
	rm -rf ../tests/*/*.mips

test:
	pytest ../tests -v --tb=short -m=${TAG}

# install a user wide cool compiler
install:
	@echo "[*] Installing python dependencies."
	@$(PIP) install --user $(PIPREQUIREMENTS)
	@echo "[*] Compiling Cool Lexical structures."
	@$(PYTHON) install.py build/$(COMPSTRUCTFILE)
	@touch build/__init__.py
	@echo "[*] Generating binary."
	@pyinstaller $(PYFLAGS) pycoolc.py
	@echo "[*] Setting config folder."
	@mkdir $(COOLCIMPORTS)
	@echo "[*] Copying require modules for compiler imports."
	@cp -r $(MODULES) $(COOLCIMPORTS)
	@echo "[*] Making binary accesible from user current path."
	@cp dist/pycoolc /usr/bin/

.PHONY: clean

#define some macros
COMPSTRUCTFILE=compiler_struct.py

# This is intended for setting a local compiler for testing.
main:
	@echo "[*] Compiling Cool Lexical structures"
	@mkdir build
	@touch build/$(COMPSTRUCTFILE)
	@python install.py build/$(COMPSTRUCTFILE)
	@touch build/__init__.py
	@echo 1 >> .builds

clean:
	rm -rf build
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

.PHONY: all

.SILENT: decipher
all: decipher

decipher: 
	python3 decipher.py "$(publicKey)"

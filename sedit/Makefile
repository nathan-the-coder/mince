all: sedit

sedit: sedit.c
	$(CC) -o sedit sedit.c -Wall -W -pedantic -std=c99

install:
	install ./sedit ~/.local/bin/

uninstall:
	rm ~/.local/bin/sedit

clean:
	rm sedit

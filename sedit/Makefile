all: sedit

sedit: sedit.c
	$(CC) -o sedit sedit.c -Wall -W -pedantic -std=c99

install:
	install ./sedit /usr/local/bin/

clean:
	rm sedit

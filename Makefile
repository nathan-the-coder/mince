CC=gcc
CYTHON=cython

CFLAGS=`pkg-config --cflags python3`

LIBS=-O2 -Wall -Wextra -lpython3.10

EXEC=mince

all: $(EXEC)

$(EXEC): 
	$(CYTHON) $(CFLAGS) --embed $(EXEC).py -3
	$(CC) $(CFLAGS) $(EXEC).c -o $(EXEC) $(LIBS)


clean:
	rm $(EXEC).c $(EXEC)

install: $(EXEC)
	install $(EXEC) /usr/local/bin

run:
	python ./mince.py test.mc

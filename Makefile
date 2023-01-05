CC=gcc
CYTHON=cython

CFLAGS=-I/usr/include/python3.10

LIBS=-lpython3.10

EXEC=mince

all: $(EXEC)

$(EXEC): 
	$(CYTHON) $(CFLAGS) --embed $(EXEC).py -3
	$(CC) $(CFLAGS) $(EXEC).c -o $(EXEC) $(LIBS)


clean:
	rm $(EXEC).c $(EXEC)

install: $(EXEC)
	install mince /usr/local/bin


CC=gcc
CYTHON=cython

CFLAGS=-I/usr/include/python3.10

LIBS=-lpython3.10

EXEC=mince

all: $(EXEC)

$(EXEC): 
	$(CYTHON) $(CFLAGS) --embed $(EXEC).py -3
	$(CC) $(CFLAGS) $(EXEC).c -o $(EXEC) $(LIBS)


install: $(EXEC)
	install mince /usr/local/bin

clean:
	rm $(EXEC).c $(EXEC)

CFLAGS=`pkg-config --cflags python-3.11-embed`

LIBS=`pkg-config --libs python-3.11-embed`

EXEC=mince

all: install-cython

activate-venv:
	$(source ./venv/bin/activate)

cython-compile: activate-venv
	cython $(CFLAGS) --embed $(EXEC).py -3
	$(CXX) $(CFLAGS) $(EXEC).c -o $(EXEC) $(LIBS)

nuitka-compile: activate-venv	
	nuitka3 mince.py -o mince

install-cython: cython-compile
	install $(EXEC) /usr/local/bin

install-nuitka: nuitka-compile
	install $(EXEC) /usr/local/bin

clean-nuitka:
	rm -rf $(EXEC).build $(EXEC) 
clean:
	rm $(EXEC).c $(EXEC)


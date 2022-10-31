CC=g++

all: tests

scheduler.o: scheduler.cpp
	$(CC) -c scheduler.cpp

tests: tests.cpp scheduler.o
	$(CC) tests.cpp scheduler.cpp -o test

all: rasc_cat tests

rasc_cat: rasc_cat.cpp
	cc rasc_cat.cpp -o rasc_cat

tests: tests.cpp rasc_cat
	cc tests.cpp rasc_cat.cpp -o test

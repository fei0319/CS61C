CC = gcc
CFLAGS = -g -Wall -std=c99 -c
LDFLAGS = -g -Wall

BUILD_DIR = ./build

# A phony target is one that is not really the name of a file;
# rather it is just a name for a recipe to be executed when you make an explicit request.
# You can read more about them here: https://www.gnu.org/software/make/manual/html_node/Phony-Targets.html
.PHONY : all clean

all : philphix

philphix : philphix.o hashtable.o
	$(CC) $(LDFLAGS) -o philphix $(BUILD_DIR)/philphix.o $(BUILD_DIR)/hashtable.o

philphix.o : src/philphix.c src/philphix.h src/hashtable.h build_dir
	$(CC) $(CFLAGS) src/philphix.c -o $(BUILD_DIR)/philphix.o

hashtable.o : src/hashtable.c src/hashtable.h build_dir
	$(CC) $(CFLAGS) src/hashtable.c -o $(BUILD_DIR)/hashtable.o

build_dir :
	mkdir -p $(BUILD_DIR)

clean :
	rm -f $(BUILD_DIR)/*.o philphix
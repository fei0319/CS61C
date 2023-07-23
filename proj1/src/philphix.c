/*
 * Include the provided hash table library.
 */
#include "hashtable.h"

/*
 * Include the header file.
 */
#include "philphix.h"

/*
 * Standard IO and file routines.
 */
#include <stdio.h>

/*
 * General utility routines (including malloc()).
 */
#include <stdlib.h>

/*
 * Character utility routines.
 */
#include <ctype.h>

/*
 * String utility routines.
 */
#include <string.h>

/*
 * This hash table stores the dictionary.
 */
HashTable *dictionary;

/*
 * The MAIN routine.  You can safely print debugging information
 * to standard error (stderr) as shown and it will be ignored in 
 * the grading process.
 */
int main(int argc, char **argv) {
  if (argc != 2) {
    fprintf(stderr, "Specify a dictionary\n");
    return 1;
  }
  /*
   * Allocate a hash table to store the dictionary.
   */
  fprintf(stderr, "Creating hashtable\n");
  dictionary = createHashTable(0x61C, &stringHash, &stringEquals);

  fprintf(stderr, "Loading dictionary %s\n", argv[1]);
  readDictionary(argv[1]);
  fprintf(stderr, "Dictionary loaded\n");

  fprintf(stderr, "Processing stdin\n");
  processInput();

  /*
   * The MAIN function in C should always return 0 as a way of telling
   * whatever program invoked this that everything went OK.
   */
  return 0;
}

/*
 * This should hash a string to a bucket index.  void *s can be safely cast
 * to a char * (null terminated string)
 */
unsigned int stringHash(void *s) {
  unsigned int x = 0u;
  char *str = s;
  while (*str != '\0') {
    x = x * 19u + (unsigned int)(*str);
    ++str;
  }
  return x;
}

/*
 * This should return a nonzero value if the two strings are identical 
 * (case sensitive comparison) and 0 otherwise.
 */
int stringEquals(void *s1, void *s2) {
  char *str1 = s1, *str2 = s2;
  while (*str1 != '\0' && *str2 != '\0') {
    if (*str1 != *str2) {
      return 0;
    }
    ++str1;
    ++str2;
  }
  return *str1 == '\0' && *str2 == '\0';
}

char *readString(FILE *fp) {
  char ch = fgetc(fp);
  while (ch == ' ' || ch == '\n') {
    ch = fgetc(fp);
  }

  int len = 0, size = 5;
  char *s = malloc(size * sizeof(char));
  while (ch != ' ' && ch != '\n' && ch != EOF) {
    s[len++] = ch;
    ch = getc(fp);
    if (len >= size) {
      size *= 2;
      s = realloc(s, size * sizeof(char));
    }
  }
  s[len++] = '\0';
  return realloc(s, len * sizeof(char));
}

/*
 * This function should read in every word and replacement from the dictionary
 * and store it in the hash table.  You should first open the file specified,
 * then read the words one at a time and insert them into the dictionary.
 * Once the file is read in completely, return.  You will need to allocate
 * (using malloc()) space for each word.  As described in the spec, you
 * can initially assume that no word is longer than 60 characters.  However,
 * for the final bit of your grade, you cannot assumed that words have a bounded
 * length.  You CANNOT assume that the specified file exists.  If the file does
 * NOT exist, you should print some message to standard error and call exit(61)
 * to cleanly exit the program.
 */
void readDictionary(char *dictName) {
  FILE *fp = fopen(dictName, "r");

  if (fp) {
    while (!feof(fp)) {
      char *word = readString(fp), *replacement = readString(fp);
      fprintf(stderr, "w:%s r:%s\n", word, replacement);
      insertData(dictionary, word, replacement);
    }
  } else {
    fprintf(stderr, "The specified file does not exist\n");
    exit(61);
  }
}

typedef struct Str {
    char *s;
    size_t length;
    size_t size;
} Str;

Str *createStr(void) {
    Str *str = malloc(sizeof(Str));
    str->length = 0;
    str->size = 2;
    str->s = malloc(sizeof(char) * str->size);
    str->s[0] = '\0';
    return str;
}

void append(Str *str, char ch) {
    if (str->length + 2 > str->size) {
        str->size *= 2;
        str->s = realloc(str->s, str->size);
    }
    str->s[str->length++] = ch;
    str->s[str->length] = '\0';
}

void delete(Str *str) {
    free(str->s);
    free(str);
}

/*
 * This should process standard input (stdin) and perform replacements as 
 * described by the replacement set then print either the original text or 
 * the replacement to standard output (stdout) as specified in the spec (e.g., 
 * if a replacement set of `taest test\n` was used and the string "this is 
 * a taest of  this-proGram" was given to stdin, the output to stdout should be 
 * "this is a test of  this-proGram").  All words should be checked
 * against the replacement set as they are input, then with all but the first
 * letter converted to lowercase, and finally with all letters converted
 * to lowercase.  Only if all 3 cases are not in the replacement set should 
 * it report the original word.
 *
 * Since we care about preserving whitespace and pass through all non alphabet
 * characters untouched, scanf() is probably insufficent (since it only considers
 * whitespace as breaking strings), meaning you will probably have
 * to get characters from stdin one at a time.
 *
 * Do note that even under the initial assumption that no word is longer than 60
 * characters, you may still encounter strings of non-alphabetic characters (e.g.,
 * numbers and punctuation) which are longer than 60 characters. Again, for the 
 * final bit of your grade, you cannot assume words have a bounded length.
 */
void processInput() {
  char ch = fgetc(stdin);
  Str *s = createStr();
  
  while (ch != EOF) {
    append(s, ch);
    ch = fgetc(stdin);
  }

  Str *t = createStr();
  char *iter = s->s;
  ch = *(iter++);
  while (ch != '\0') {
      if (isalpha(ch)) {
          Str *word = createStr(), *original_word = createStr();
          while (isalpha(ch)) {
              append(word, ch);
              append(original_word, ch);
              ch = *(iter++);
          }
          char *replacement = findData(dictionary, word->s);
          if (replacement == NULL) {
              for (int i = 1; i < word->length; ++i) {
                  word->s[i] = tolower(word->s[i]);
              }
              replacement = findData(dictionary, word->s);
          }
          if (replacement == NULL) {
              word->s[0] = tolower(word->s[0]);
              replacement = findData(dictionary, word->s);
          }
          if (replacement == NULL) {
              replacement = original_word->s;
          }
          while (*replacement != '\0') {
            append(t, *(replacement++));
          }
          delete(word);
          delete(original_word);
      } else {
          append(t, ch);
          ch = *(iter++);
      }
  }

  delete(s);
  fprintf(stdout, "%s", t->s);
  delete(t);
}

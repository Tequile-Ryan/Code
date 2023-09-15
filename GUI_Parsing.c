#include <stdio.h>
#include <stdlib.h>
#include <cJSON.h>
  
int main() {
    // open the file
    FILE *fp = fopen("data.json", "r");
    /*if (fp == NULL) {
        printf("Error: Unable to open the file.\n");
        return 1;
    }*/
  
    // read the file contents into a string
    //char buffer[1024];
    //int len = fread(buffer, 1, sizeof(buffer), fp);
    fclose(fp);
}
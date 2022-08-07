#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef uint8_t BYTE;

const int BLOCK_SIZE = 512;

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE");
        return 1;
    }
    // Open input file
    FILE *f = fopen(argv[1], "r");
    if (f == NULL)
    {
        printf("Could not open %s.\n", argv[1]);
        return 1;
    }
    BYTE data[BLOCK_SIZE];
    int num = 0;
    FILE *img = NULL;
    fread(data, 1, BLOCK_SIZE, f);
    while (fread(data, 1, BLOCK_SIZE, f) == BLOCK_SIZE)
    {
        if (data[0] == 0xff && data[1] == 0xd8 && data[2] == 0xff && (data[3] & 0xf0) == 0xe0)
        {
            if (img != NULL)
            {
                // Close file
                fclose(img);
            }
            char filename[8];
            sprintf(filename, "%03i.jpg", num);
            // For the name of files
            num++;
            img = fopen(filename, "w");
            // Initial write
            fwrite(data, 1, BLOCK_SIZE, img);
        }
        else if (img != NULL)
        {
            // Continue writing for normal block
            fwrite(data, 1, BLOCK_SIZE, img);
        }
    }
    // Close file
    fclose(f);
    return 0;
}
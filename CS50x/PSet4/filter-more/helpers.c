#include "helpers.h"
//Rounding
#include <math.h>
// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // Loop rows
    for (int i = 0; i < height; i++)
    {
        // Loop pixels
        for (int j = 0; j < width; j++)
        {
            RGBTRIPLE original = image[i][j];
            BYTE average = round((original.rgbtBlue + original.rgbtGreen + original.rgbtRed) / 3.0);
            RGBTRIPLE new;
            new.rgbtBlue = average;
            new.rgbtGreen = average;
            new.rgbtRed = average;
            image[i][j] = new;
        }
    }
    return;
}

void swap(int *a, int *b)
{
    int temp = *a;
    *a = *b;
    *b = temp;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    // Loop rows
    for (int i = 0; i < height; i++)
    {
        RGBTRIPLE temp;
        int start = 0;
        int end = width - 1;
        // Loop pixels
        while (start < end)
        {
            temp = image[i][start];
            image[i][start] = image[i][end];
            image[i][end] = temp;
            start++;
            end--;
        }
    }
    return;
}

void boxBlur(RGBTRIPLE *point, int count, RGBTRIPLE neighbors[9])
{
    float blu = 0;
    float green = 0;
    float red = 0;
    // Loop pixels
    for (int i = 0; i < count; i++)
    {
        blu += neighbors[i].rgbtBlue;
        green += neighbors[i].rgbtGreen;
        red += neighbors[i].rgbtRed;
    }
    BYTE avgblu = round(blu / count);
    BYTE avgreen = round(green / count);
    BYTE avgred = round(red / count);
    RGBTRIPLE new;
    new.rgbtBlue = avgblu;
    new.rgbtGreen = avgreen;
    new.rgbtRed = avgred;
    *point = new;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE newImage[height][width];
    // Loop rows
    for (int i = 0; i < height; i++)
    {
        // Loop pixels
        for (int j = 0; j < width; j++)
        {
            RGBTRIPLE neighbors[9];
            int c = 0;
            // Assign neighbors
            if (j > 0)
            {
                if (i > 0)
                {
                    neighbors[c] = image[i - 1][j - 1];
                    c++;
                }

                neighbors[c] = image[i][j - 1];
                c++;

                if (i < height - 1)
                {
                    neighbors[c] = image[i + 1][j - 1];
                    c++;
                }
            }

            if (i > 0)
            {
                neighbors[c] = image[i - 1][j];
                c++;
            }

            neighbors[c] = image[i][j];
            c++;

            if (i < height - 1)
            {
                neighbors[c] = image[i + 1][j];
                c++;
            }
            if (j < width - 1)
            {
                if (i > 0)
                {
                    neighbors[c] = image[i - 1][j + 1];
                    c++;
                }

                neighbors[c] = image[i][j + 1];
                c++;

                if (i < height - 1)
                {
                    neighbors[c] = image[i + 1][j + 1];
                    c++;
                }
            }
            boxBlur(&newImage[i][j], c, neighbors);
        }
    }

    // Copy newImage to image
    // Loop rows
    for (int i = 0; i < height; i++)
    {
        // Loop pixels
        for (int j = 0; j < width; j++)
        {
            image[i][j] = newImage[i][j];
        }
    }
    return;
}

// Calculate pixel into Gx and Gy
void seperate(int *Gxr, int *Gxg, int *Gxb, int *Gyr, int *Gyg, int *Gyb, RGBTRIPLE pixel, int multiY, int multiX)
{
    *Gxb += pixel.rgbtBlue * multiX;
    *Gxg += pixel.rgbtGreen * multiX;
    *Gxr += pixel.rgbtRed * multiX;
    *Gyb += pixel.rgbtBlue * multiY;
    *Gyg += pixel.rgbtGreen * multiY;
    *Gyr += pixel.rgbtRed * multiY;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE newImage[height][width];
    // Loop rows
    for (int i = 0; i < height; i++)
    {
        // Loop pixels
        for (int j = 0; j < width; j++)
        {
            int Gxr = 0;
            int Gxg = 0;
            int Gxb = 0;
            int Gyr = 0;
            int Gyg = 0;
            int Gyb = 0;

            // Calculate Gxr Gxg Gxb...
            if (j > 0)
            {
                if (i > 0)
                {
                    seperate(&Gxr, &Gxg, &Gxb, &Gyr, &Gyg, &Gyb, image[i - 1][j - 1], -1, -1);
                }

                seperate(&Gxr, &Gxg, &Gxb, &Gyr, &Gyg, &Gyb, image[i][j - 1], 0, -2);

                if (i < height - 1)
                {
                    seperate(&Gxr, &Gxg, &Gxb, &Gyr, &Gyg, &Gyb, image[i + 1][j - 1], 1, -1);
                }
            }

            if (i > 0)
            {
                seperate(&Gxr, &Gxg, &Gxb, &Gyr, &Gyg, &Gyb, image[i - 1][j], -2, 0);
            }

            seperate(&Gxr, &Gxg, &Gxb, &Gyr, &Gyg, &Gyb, image[i][j], 0, 0);

            if (i < height - 1)
            {
                seperate(&Gxr, &Gxg, &Gxb, &Gyr, &Gyg, &Gyb, image[i + 1][j], 2, 0);
            }

            if (j < width - 1)
            {
                if (i > 0)
                {
                    seperate(&Gxr, &Gxg, &Gxb, &Gyr, &Gyg, &Gyb, image[i - 1][j + 1], -1, 1);
                }

                seperate(&Gxr, &Gxg, &Gxb, &Gyr, &Gyg, &Gyb, image[i][j + 1], 0, 2);

                if (i < height - 1)
                {
                    seperate(&Gxr, &Gxg, &Gxb, &Gyr, &Gyg, &Gyb, image[i + 1][j + 1], 1, 1);
                }
            }

            // Calculate the values of the new pixel
            RGBTRIPLE new;
            int b = round(sqrt(Gxb * Gxb + Gyb * Gyb));
            int g = round(sqrt(Gxg * Gxg + Gyg * Gyg));
            int r = round(sqrt(Gxr * Gxr + Gyr * Gyr));
            if (b > 255)
            {
                new.rgbtBlue = 255;
            }
            else
            {
                new.rgbtBlue = b;
            }
            if (g > 255)
            {
                new.rgbtGreen = 255;
            }
            else
            {
                new.rgbtGreen = g;
            }
            if (r > 255)
            {
                new.rgbtRed = 255;
            }
            else
            {
                new.rgbtRed = r;
            }
            // Add new pixel to new image
            newImage[i][j] = new;
        }
    }

    // Copy newImage to image
    // Loop rows
    for (int i = 0; i < height; i++)
    {
        // Loop pixels
        for (int j = 0; j < width; j++)
        {
            image[i][j] = newImage[i][j];
        }
    }
    return;
}
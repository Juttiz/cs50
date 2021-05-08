// Copies a BMP file

#include <stdio.h>
#include <stdlib.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    // ensure proper usage
    if (argc != 4)
    {
        fprintf(stderr, "Usage: copy infile outfile\n");
        return 1;
    }

    // remember filenames
    char *infile = argv[2];
    char *outfile = argv[3];
    int f = atoi(argv[1]);


    // open input file
    FILE *inptr = fopen(infile, "r");
    if (inptr == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", infile);
        return 2;
    }

    // open output file
    FILE *outptr = fopen(outfile, "w");
    if (outptr == NULL)
    {
        fclose(inptr);
        fprintf(stderr, "Could not create %s.\n", outfile);
        return 3;
    }

    // read infile's BITMAPFILEHEADER
    BITMAPFILEHEADER bf;
    fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

    // read infile's BITMAPINFOHEADER
    BITMAPINFOHEADER bi;
    fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

    // ensure infile is (likely) a 24-bit uncompressed BMP 4.0
    if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 ||
        bi.biBitCount != 24 || bi.biCompression != 0)
    {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
    }

    int paddingold = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;
    int a = bi.biWidth , b = abs(bi.biHeight);

    bi.biWidth = bi.biWidth * f;
    bi.biHeight = bi.biHeight * f;

    int padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

    bi.biSizeImage = ((sizeof(RGBTRIPLE)*bi.biWidth)+padding)*abs(bi.biHeight);
    bf.bfSize = bi.biSizeImage + sizeof(BITMAPFILEHEADER) + sizeof(BITMAPINFOHEADER);

    // write outfile's BITMAPFILEHEADER
    fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, outptr);

    // write outfile's BITMAPINFOHEADER
    fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, outptr);


    RGBTRIPLE scanline[bi.biWidth*sizeof(RGBTRIPLE)];
    // iterate over infile's scanlines
    for (int i = 0; i < b; i++)
    {
        // iterate over pixels in scanline
        for (int j = 0  ; j < a; j++)
        {
            // temporary storagecp
            RGBTRIPLE triple;

            // read RGB triple from infile
            fread(&triple, sizeof(RGBTRIPLE), 1, inptr);
            for(int n = 0; n < f ; n++)
            {
                scanline[(j*f)+n] = triple;
            }
        }

        // skip over padding, if any
        fseek(inptr, paddingold, SEEK_CUR);
        for(int l = 0 ; l < f ; l++)     // write RGB triple to outfile
            {
                fwrite(scanline, sizeof(RGBTRIPLE), bi.biWidth, outptr);
                // then add it back (to demonstrate how)
                for (int k = 0; k < padding; k++)
                {
                    fputc(0x00, outptr);
                }
            }
    }

    // close infile
    fclose(inptr);

    // close outfile
    fclose(outptr);

    // success
    return 0;
}

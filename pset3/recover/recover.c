#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
typedef unsigned char  BYTE;

int main(int argc, char *argv[])
{
    if(argc != 2)
    {
        fprintf(stderr,"Usage : ./recover image\n");
        return 1;
    }

    char *infile = argv[1];

    FILE *inptr = fopen(infile,"r");
    if(inptr == NULL)
    {
        fprintf(stderr,"Could not open %s\n" , infile);
        return 2;
    }

    int a = 512;
    int i = 0;
    char *outfile = malloc(8);
    FILE *outptr = malloc(8);
    BYTE buffer[512];

    while(fread(buffer,512,1,inptr))
    {


        // fread(buffer,512,1,inptr) ;
        // int l = sizeof(buffer);
        // if(l!= a)
        // {
        //     printf("%i\n",l);
        //     break;

        // }

        //else
        {
            if(buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0 )== 0xe0)
            {
                if( i != 0 )
                {
                    fclose(outptr);
                }
                sprintf(outfile , "%03d.jpg", i);
                printf("%s\n",outfile);

                outptr = fopen(outfile,"w");
                if(outptr == NULL)
                {
                    fclose(inptr);
                    fprintf(stderr,"could not creat %s\n",outfile);
                    return 3;
                }
                fwrite(buffer,512,1,outptr);
                i++;
            }
            else
            {
                if(i > 1)
                {

                    fwrite(buffer,512,1,outptr);
                }
            }
        }

    }
    fclose (inptr);
    fclose (outptr);
    free(outptr);
    free(outfile);
    return 0 ;
}

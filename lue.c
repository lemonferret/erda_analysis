#include <stdio.h>
extern FILE *stdin;
int main(int argc, char **argv)
{
  FILE *fp;
  char *filename;
  char turha[1000];
  int data, tmp, adc[8], upper, i;
  fp=stdin;
  if(argc>1){
    filename=argv[1];
    fp=fopen(filename, "r");
  }
  fread(turha, sizeof(char),512,fp);
  fread(turha, sizeof(char),512,fp);
  while(fread(&data, sizeof(char), 2, fp)){
    for(i=0;i<8;i++) adc[i]=0;
    tmp=data;
    upper=tmp&0xE000;
    upper=upper>>13;
    tmp=0;
    tmp=data&0x1fff;
    adc[upper]=tmp;
    for(i=0;i<8;i++) printf("%i ",adc[i]);
    printf("\n");
  }
  fclose(fp);
  return 0;
}

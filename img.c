#include<stdio.h>
#include<stdlib.h>

#define END_ARRAY 32469
#define X_END  375
#define Y_END  370

#define GRID   10

int cmp( const void *p, const void *q );

int main(){

  struct{
    int x;
    int y;
  }point;

  typedef struct{
    int x;
    int y;
  }point_t;

  point_t aim[10];

  FILE *fp;
  FILE *heder;
  FILE *test;

  int sample_num;

  int est[(640/GRID)*(480/GRID)] = {0};
  int tmp[(640/GRID)*(480/GRID)] = {0};

  int GKL[10] = {0}; //greatest keypoints list

  int i,j;
  int x,y;

  int aim_point[10] = {0};

  int n;

  int ImgKeypoint_Map[640][480];

  test = fopen("test.txt","w");
  if(test == NULL){
    printf("ファイルが開けません");
    exit(1);
  }

  heder = fopen("heder.txt","r");
  if(heder == NULL){
    printf("ファイルが開けません");
    exit(1);
  }

  fp = fopen("sample_point.txt","r");
  if(fp == NULL){
    printf("ファイルが開けません");
    exit(1);
  }

  /*サンプル数の読み込み*/
  fscanf(heder,"%d %d %d",&sample_num, &x, &y);

  for(i = 0; i < sample_num; i++){
    fscanf(fp,"%d %d",&point.x,&point.y);
    //printf("%d %d\n",point.x, point.y);
    ImgKeypoint_Map[point.x][point.y] = 1;
  }
/*
  for(i = 0; i < 480; i++){
    for(j = 0; j < 640; j++){
      if((ImgKeypoint_Map[i][j] == 1) && ((i < X_END) && (i > x)) && ((j < Y_END) && (j > y))) fprintf(test,"1");
      else fprintf(test,"0");
    }
    fprintf(test,"\n");
  }
*/

  /*特徴点から風船のある座標を推測する*/
  for(i = y; i < Y_END; i++){
    for(j = x; j < X_END; j++){
      if(ImgKeypoint_Map[j][i] == 1){
        est[(int)(i/GRID)*(int)(j/GRID)] += 1;
        tmp[(int)(i/GRID)*(int)(j/GRID)] += 1;
      }
    }
  }

  n = sizeof(tmp)/sizeof(int);
  qsort(tmp, n, sizeof(int), cmp);

  for(i = 0; i < (640/GRID)*(480/GRID); i++);

  for(j = 0; j < 10; j++) GKL[j] = tmp[i-j-1];

  for(i = 0; i < 10; i++){
    for(j = 0; j < (640/GRID)*(480/GRID); j++){
      if(est[j] == GKL[i]){
        aim[i].x = j%(640/GRID);
        aim[i].y = j/(640/GRID);
      }
    }
  }

  for(i = 0; i < 10; i++) printf("aim[%d:%d]\n",aim[i].x,aim[i].y);

  fclose(heder);
  fclose(fp);
  return 0;
}


int cmp( const void *p, const void *q ) {
    return *(int*)p - *(int*)q;
}

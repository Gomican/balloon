#include<stdio.h>
#include<stdlib.h>

#define END_ARRAY 32469
#define X_END  480
#define Y_END  280

//GCD 80
#define GRID   40

int cmp( const void *p, const void *q );

int main(){
  int test2[360/GRID][640/GRID];
  int k;
  struct{
    int x;
    int y;
  }point;

  typedef struct{
    int x;
    int y;
  }point_t;

  point_t aim[10];

  typedef struct{
    int val;
    int flag;
  }est_pack_t;

  est_pack_t est[(640/GRID)*(360/GRID)];
  int tmp[(640/GRID)*(360/GRID)] = {0};

  int GKL[10] = {0}; //greatest keypoints list

  FILE *fp;
  FILE *heder;
  FILE *test;
  FILE *aimp;

  int sample_num;

  int i,j;
  int x,y;
  int n;

  int ImgKeypoint_Map[640][360];

  aimp = fopen("aim.txt","w");
  if(aimp == NULL){
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

  test = fopen("test.txt","w");
  if(fp == NULL){
    printf("ファイルが開けません");
    exit(1);
  }

  /*tmpとestの初期化*/
  for(i = 0; i < (640/GRID)*(360/GRID); i++){
    est[i].val = 0;
    est[i].flag = 1;
  }

  /*サンプル数の読み込み*/
  fscanf(heder,"%d %d %d",&sample_num, &x, &y);

  for(i = 0; i < sample_num; i++){
    fscanf(fp,"%d %d",&point.x,&point.y);
    ImgKeypoint_Map[point.y][point.x] = 1;
  }

  for(i = 0; i < 360; i++){
    for(j = 0; j < 640; j++){
      if((ImgKeypoint_Map[i][j] == 1) && ((i < Y_END) && (i > y)) && ((j < X_END) && (j > x))) fprintf(test,"1");
      else fprintf(test,"0");
    }
    fprintf(test,"\n");
  }

  /*特徴点から風船のある座標を推測する*/
  for(i = y; i < Y_END; i++){
    for(j = x; j < X_END; j++){
      if(ImgKeypoint_Map[i][j] == 1){
        est[(int)(j/GRID)+((640/GRID))*(int)(i/GRID)].val += 1;
        tmp[(int)(j/GRID)+((640/GRID))*(int)(i/GRID)] += 1;
      }
    }
  }

  //for(i = 0; i < (640/GRID)*(360/GRID); i++) printf("%d",est[i].val);
  n = sizeof(tmp)/sizeof(int);
  qsort(tmp, n, sizeof(int), cmp);

  for(i = 0; i < (640/GRID)*(360/GRID); i++);
  for(j = 0; j < 10; j++) GKL[j] = tmp[i-j-1];

  for(i = 0; i < 10; i++) printf("GKL[%d]:%d\n",i,GKL[i]);

  //for(i = 0; i < 10; i++) printf("%d\n",GKL[i]);

  for(i = 0; i < 10; i++){
    for(j = 0; j < (640/GRID)*(360/GRID); j++){
      if((est[j].val == GKL[i]) && (est[j].flag)){
        aim[i].x = j%(640/GRID);
        aim[i].y = j/(640/GRID);
        est[j].flag = 0;
        break;
      }
    }
  }

  for(i = 0; i < 360/GRID; i++){
    for(j = 0; j < 640/GRID; j++){
      test2[i][j] = 0;
    }
  }


  for(i = 0; i < 10; i++) printf("aim[%d:%d]...%d\n",aim[i].x,aim[i].y,GKL[i]);
  for(k = 0; k < 10; k++){
    for(i = 0; i < 360/GRID; i++){
      for(j = 0; j < 640/GRID; j++){
        if((aim[k].x == j) && (aim[k].y == i)){
            printf("%d,%d\n",i,j);
            test2[i][j] = 1;
         }
      }
    }
  }

  for(i = 0; i < 360/GRID; i++){
    for(j = 0; j < 640/GRID; j++){
      printf("%d",test2[i][j]);
    }
    printf("\n");
  }

  for(i = 0; i < 10; i++)  fprintf(aimp,"%d %d\n",(aim[i].x*GRID)+GRID/2,(aim[i].y*GRID)+GRID/2);

  fclose(heder);
  fclose(fp);
  fclose(aimp);


  return 0;
}


int cmp( const void *p, const void *q ) {
    return *(int*)p - *(int*)q;
}

/**
SOM.c code from https://github.com/tsotne95/SOM/blob/master/som.c
(https://github.com/tsotne95/SOM)
**/

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>

#define SQR(x) ((x)*(x)) //square

struct N_config
{
  int n_in; //capter(data vector) size
  int n_l_out; // neuron map row number
  int n_c_out; // neuron map column number
  int n_out; //total neuron (n_l_out * n_c_out)
  int nb_it; // iteration number
  double minAlpha;//starting value
  int train; //training layer operation num
  int ftrain; //first layer operation num
}N_conf;

struct node //neuron (node) struct
{
  double act; //euc. dist.
  char *etiq;
  double *w; //weight (memory) vector
};

typedef struct node t_node;

struct bmu {
	double act; // euclidian distance
	int r;
	int c;
};


struct vec
	{
        double *arr;
        char *name;
        double norm;
	};

struct vec * array_vec;


typedef struct bmu t_bmu;
t_bmu *Bmu = NULL;
int Bmu_size=1;

struct net
{
  int nhd_r;  // neighbourhood radius
  t_node **map;
  double *captors; // current data vector
  double alpha; // learning coeficient
  char *etiq;
} Net;

void alloc_array_struct(int n)
{
    array_vec=malloc(n*sizeof(struct vec));
    int i;
    for(i=0;i<n;i++)
    {
        array_vec[i].arr=malloc(N_conf.n_in*sizeof(double));
        array_vec[i].name=malloc(20*sizeof(char));
    }
}

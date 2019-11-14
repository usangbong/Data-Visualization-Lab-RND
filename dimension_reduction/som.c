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


double *aver,*min,*max;

void average_vec(int n)
{
    aver=malloc(N_conf.n_in*sizeof(double));
    memset(aver,0,N_conf.n_in*sizeof(double));

    int i,j;

    for(i=0;i<N_conf.n_in;i++)
    {
        for(j=0;j<n;j++)
            aver[i]+=array_vec[j].arr[i];
        aver[i]/=n;
    }
}

void min_vec(double k)
{
    min=malloc(N_conf.n_in*sizeof(double));
    int i;
    for(i=0;i<N_conf.n_in;i++)
        min[i]=aver[i]-k;
}

void max_vec(double k)
{
    max=malloc(N_conf.n_in*sizeof(double));
    int i;
    for(i=0;i<N_conf.n_in;i++)
        max[i]=aver[i]+k;
}


void norm_array_vec(int i,int size)
{
    double sum=0.;
    int j;
    for(j=0;j<size;j++)
        sum+=SQR(array_vec[i].arr[j]);
    array_vec[i].norm=sqrt(sum);
}

void denorm_array_vec(int n)
{
    int i,j;
    for(i=0;i<n;i++)
    {
        for(j=0;j<N_conf.n_in;j++)
            array_vec[i].arr[j]/=array_vec[i].norm;
    }
}


double* init_rand_w()
{
    int i;
    double k=(double)rand()/RAND_MAX;
    double *tmp_w=malloc(N_conf.n_in*sizeof(double));

    for(i=0;i<N_conf.n_in;i++)
        {
            tmp_w[i]=k*(max[i]-min[i])+min[i];
        }

    double norm=0.;

    for(i=0;i<N_conf.n_in;i++)
    {
        norm+=SQR(tmp_w[i]);
    }

    for(i=0;i<N_conf.n_in;i++)
    {
            tmp_w[i]/=norm;
    }
    return tmp_w;
}


int * index_array;

void init_shuffle(int n)
{
    index_array=malloc(sizeof(int)*n);
    int i;
    for(i=0;i<n;i++)
        index_array[i]=i;
}

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

void array_shuffle(int n)
{
    int i,r_and,k;
    srand(time(NULL));
    for(i=0;i<n;i++)
        {
            r_and=rand()%n;
            k=index_array[i];
            index_array[i]=index_array[r_and];
            index_array[r_and]=k;
        }
}

double euc_distance(double *a1, double *a2, int n)
{
	double sum=0.;
	int i;
	for(i=0;i<n;i++)
	{
		sum+=(SQR(a1[i] - a2[i]));
	}
	return sqrt(sum);
}


void calc_alpha(int it_n, int tot_it)
{
	Net.alpha = N_conf.minAlpha * (1 - ((double)it_n/(double)tot_it));
}

void update(t_bmu* b_mu)
{
    int nr=Net.nhd_r;
    int i,j,x1,x2,y1,y2;//top and bottom

    for(;nr>=0;nr--)
    {
        if(b_mu->r-nr<0)
            x1=0;
        else
            x1=b_mu->r-nr;
        if(b_mu->c-nr<0)
            y1=0;
        else
            y1=b_mu->c-nr;

        if(b_mu->r+nr>N_conf.n_l_out-1)
            x2=N_conf.n_l_out-1;
        else
            x2=b_mu->r+nr;
        if(b_mu->c+nr>N_conf.n_c_out-1)
            y2=N_conf.n_c_out-1;
        else
            y2=b_mu->c+nr;

        for(i=x1;i<=x2;i++)
            for(j=y1;j<=y2;j++)
            {

                int k;

                for(k=0;k<N_conf.n_in;k++)
                    {

                        Net.map[i][j].w[k]+=Net.alpha*(Net.captors[k]-Net.map[i][j].w[k]);
                    }
            }
    }
}

void init_n_conf()
{
    N_conf.n_l_out=6;
	N_conf.n_c_out=10;
    N_conf.n_out=N_conf.n_l_out*N_conf.n_c_out;
    N_conf.n_in=4;
    N_conf.nb_it=30000;
    N_conf.minAlpha=0.7;
    N_conf.ftrain=N_conf.nb_it/5;
    N_conf.train=2;
}

void read_data()
{
    FILE * in;

	char *str=malloc(sizeof(char)*500);
	in=fopen("iris.data","r");

    int i,j;
	for(i=0;i<150;i++)
	{
        fscanf(in,"%s",str);
        char *tok=strtok(str,",");

        for(j=0;j<N_conf.n_in;j++)
            {
                array_vec[i].arr[j]=atof(tok);
                tok=strtok(NULL,",");
            }

        if (strcmp(tok, "Iris-setosa") == 0)
			strcpy(array_vec[i].name,"A");
        else if(strcmp(tok,"Iris-versicolor")==0)
            strcpy(array_vec[i].name,"B");
        else
            strcpy(array_vec[i].name,"C");

        norm_array_vec(i,N_conf.n_in);
	}

	fclose(in);
    free(str);
}


index = ["vgh", "vglogh", 
        "n_l1_vg_h", "n_l1_vg_logh", "n_l1_vgh", "n_l1_vglogh", 
        "n_l2_vg_h", "n_l2_vg_logh", "n_l2_vgh", "n_l2_vglogh", 
        "n_max_vg_h", "n_max_vg_logh", "n_max_vgh", "n_max_vglogh", 
        "std_vg_h", "std_vg_logh", "std_vgh", "std_vglogh", 
        "mm_vg_h", "mm_vg_logh", "mm_vgh", "mm_vglogh", 
        "pt_vg_h", "pt_vg_logh", "pt_vgh", "pt_vglogh"
        ]

w=256
h=256
size = w*h

all_val_grad_hist = []
sparse_val_grad_hist = []
#'VisMale_128x256x256','bonsai256X256X256B', 'Carp_256x256x512','XMasTree-LO_256x249x256' 
for dataset in ['VisMale_128x256x256'] :
    with open('../volumeCache/%s.raw.2DHistogram.TextureCache'%(dataset), 'rb') as fp:
        Histogram2DYMax = unpack('<f', fp.read(4))[0] #Max of Grad_mag
        for i in range(h) :
            for j in range(w):
                readdata = unpack('<L', fp.read(4))[0]
                all_val_grad_hist.append([i, j, readdata])
                if readdata>=1 and i!=0:
                    sparse_val_grad_hist.append([i, j, readdata])

        np_all_val_grad_hist = np.array(all_val_grad_hist)
        np_sparse_val_grad_hist = np.array(sparse_val_grad_hist)

        ret_all_array = transform(np_all_val_grad_hist)
        ret_sparse_array = transform(np_sparse_val_grad_hist)
        
        tsne_all_array = []
        tsne_sparse_array = []
        
        ###########################################################################################################
        
        #for i in range(len(ret_all_array)):
        #    print("%d_%s_%s"% (i, dataset, index[i]), end='\t')
        #    tsne_all_array.append(_TSNE(100,ret_all_array[i]))
        
        #for i in range(len(tsne_all_array)):
        #    save_tsne_result( tsne_all_array[i],  "tsneCache", "%d_%s_%s"% (i, dataset, index[i]) )        
        
        #for i in range(len(tsne_all_array)):
        #    for _k in [10,15,20]:
        #        kmeans(_k,  tsne_all_array[i], np_all_val_grad_hist, 256,256,  "%d_%s_%s"% (i, dataset, index[i]) )
        #    
        #    for _eps in [0.5, 1.0, 1.5, 3.0]:
        #        dbscan(_eps, tsne_all_array[i], np_all_val_grad_hist, 256,256,  "%d_%s_%s"% (i, dataset, index[i]))
        #    Hdbscan(300, 20, 1.0, tsne_all_array[i], np_all_val_grad_hist, 256,256,  "%d_%s_%s"% (i, dataset, index[i])  ) 
        
        ###########################################################################################################
        
        for tsne_cnt in range(10):
            tsne_sparse_array.append([])
            for i in range(len(ret_sparse_array)):
                print("%s_%d_sparse_%s"% ( dataset, i,index[i]), end='\t')
                tsne_sparse_array[tsne_cnt].append(_TSNE(3000,ret_sparse_array[i]))

            for i in range(len(tsne_sparse_array[tsne_cnt])):
                save_tsne_result( tsne_sparse_array[tsne_cnt][i],  "tsneCache", "%d_%s_%d_sparse_%s"% (tsne_cnt, dataset,i,  index[i]) )     



index = ["vgh", "vglogh", 
        "n_l1_vg_h", "n_l1_vg_logh", "n_l1_vgh", "n_l1_vglogh", 
        "n_l2_vg_h", "n_l2_vg_logh", "n_l2_vgh", "n_l2_vglogh", 
        "n_max_vg_h", "n_max_vg_logh", "n_max_vgh", "n_max_vglogh", 
        "std_vg_h", "std_vg_logh", "std_vgh", "std_vglogh", 
        "mm_vg_h", "mm_vg_logh", "mm_vgh", "mm_vglogh", 
        "pt_vg_h", "pt_vg_logh", "pt_vgh", "pt_vglogh"
        ]

w=256
h=256
size = w*h

all_val_grad_hist = []
sparse_val_grad_hist = []
#'VisMale_128x256x256','bonsai256X256X256B', 'Carp_256x256x512','XMasTree-LO_256x249x256' 
for dataset in ['VisMale_128x256x256'] :
    with open('../volumeCache/%s.raw.2DHistogram.TextureCache'%(dataset), 'rb') as fp:
        Histogram2DYMax = unpack('<f', fp.read(4))[0] #Max of Grad_mag
        for i in range(h) :
            for j in range(w):
                readdata = unpack('<L', fp.read(4))[0]
                all_val_grad_hist.append([i, j, readdata])
                if readdata>=1 and i!=0:
                    sparse_val_grad_hist.append([i, j, readdata])

        np_all_val_grad_hist = np.array(all_val_grad_hist)
        np_sparse_val_grad_hist = np.array(sparse_val_grad_hist)

        ret_all_array = transform(np_all_val_grad_hist)
        ret_sparse_array = transform(np_sparse_val_grad_hist)
        
        tsne_all_array = []
        tsne_sparse_array = []
        
        ###########################################################################################################
        
        #for i in range(len(ret_all_array)):
        #    print("%d_%s_%s"% (i, dataset, index[i]), end='\t')
        #    tsne_all_array.append(_TSNE(100,ret_all_array[i]))
        
        #for i in range(len(tsne_all_array)):
        #    save_tsne_result( tsne_all_array[i],  "tsneCache", "%d_%s_%s"% (i, dataset, index[i]) )        
        
        #for i in range(len(tsne_all_array)):
        #    for _k in [10,15,20]:
        #        kmeans(_k,  tsne_all_array[i], np_all_val_grad_hist, 256,256,  "%d_%s_%s"% (i, dataset, index[i]) )
        #    
        #    for _eps in [0.5, 1.0, 1.5, 3.0]:
        #        dbscan(_eps, tsne_all_array[i], np_all_val_grad_hist, 256,256,  "%d_%s_%s"% (i, dataset, index[i]))
        #    Hdbscan(300, 20, 1.0, tsne_all_array[i], np_all_val_grad_hist, 256,256,  "%d_%s_%s"% (i, dataset, index[i])  ) 
        
        ###########################################################################################################
        
        for tsne_cnt in range(10):
            tsne_sparse_array.append([])
            for i in range(len(ret_sparse_array)):
                print("%s_%d_sparse_%s"% ( dataset, i,index[i]), end='\t')
                tsne_sparse_array[tsne_cnt].append(_TSNE(3000,ret_sparse_array[i]))

            for i in range(len(tsne_sparse_array[tsne_cnt])):
                save_tsne_result( tsne_sparse_array[tsne_cnt][i],  "tsneCache", "%d_%s_%d_sparse_%s"% (tsne_cnt, dataset,i,  index[i]) )     


for tsne_cnt in range(10):
    for i in range(len(tsne_sparse_array[tsne_cnt])):
        Hdbscan_dr(80,20,1.0, tsne_sparse_array[tsne_cnt][i], np_sparse_val_grad_hist, 256,256,  "%d_%d_%s_%s"% (tsne_cnt, i, dataset, index[i]), tsne_cnt)
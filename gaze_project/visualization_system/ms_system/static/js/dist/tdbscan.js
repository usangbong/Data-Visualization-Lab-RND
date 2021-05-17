// cluster start
//clust var
var tnp = 0;
var tpoints = [];
var tset_clust = [];
var tarray_AOI = [];
var tepsilon = 15;
var tminpts = 5;
var tcluster_num = 0;
var th=-1, ta=-2, te=1, tg=0, tb=0, tz=-2, tnum=0;
var timeDimensionWeight= 1;
var clusterSize = 5;
var DBSCAN_CONFIG = {};
function tinitSimpledbscanVariables(){
    tnp = 0;
    tpoints = [];
    tset_clust = [];
    tarray_AOI = [];
    tepsilon = DBSCAN_CONFIG['ep'];
    tminpts = DBSCAN_CONFIG['mp'];
    tcluster_num = 0;
    th=-1;
    ta=-2;
    te=1;
    tg=0;
    tb=0;
    tz=-2;
    tnum=0;
    timeDimensionWeight=DBSCAN_CONFIG['tw'];
    clusterSize = DBSCAN_CONFIG['cs'];
}

trun = function(tn, tj, tq, tm, to, tset){
    var tl, tk=0;
    for(tl=0; tl<tj; ++tl){
        if(tn[tl].cluster_id===th){
            if(td(tl, tk, tn, tj, tq, tm, to, tset)===te){
                ++tk;
            }
        }
    }
};

function tf(tl, tn, tj, tr, tq){
  var tm, tk=[], to;
    for(tm=0; tm < tj; ++tm){
        if(tm===tl){
            tk.push(tm);
            continue;
        }
        to = tq(tn[tl],tn[tm]);
        if(to > tr){
            continue;
        }
        else{
            tk.push(tm)
        }
      }
    return tk;
}

function td(tk, to, tr, tm, tt, tl, tn, tset){
    var tj, ts = tg, tq = tf(tk, tr, tm, tt, tn);
    if(tq.length<tl){
        tr[tk].cluster_id = tz;
        tset[tnum].id = tr[tk].cluster_id;
        tset[tnum].x = tr[tk].x;
        tset[tnum].y = tr[tk].y;
        tset[tnum].t = tr[tk].t;
        tset[tnum].n = 1;
        tset[tnum].r = 5;
        tnum++;
    }else{
        tr[tk].cluster_id = to;
        for(tj=0;tj<tq.length;++tj){
            tr[tq[tj]].cluster_id=to
        }
        for(tj=0;tj<tq.length;++tj){
            tc(tq[tj],tq,to,tr,tm,tt,tl,tn)
        }
        tfind_center(tr,tq,tset,tr[tk],tnum);
        ts=te
      }
    return ts
}

function tc(tk,tu,ts,tv,tm,tw,tl,tr){
    var tj,tq,to,tt,tn=tf(tk,tv,tm,tw,tr);
    tq=tn.length;
    if(tq>=tl){
        for(tj=0;tj<tq;++tj){
            tt=tn[tj];to=tv[tt];
            if(to.cluster_id===ta||to.cluster_id===th){
                if(to.cluster_id===th){
                    tu.push(tt)
                }
                to.cluster_id=ts
            }
        }
    }
    return tb
}

teuclidean_dist = function(tj,ti){
    return Math.sqrt((tj.x-ti.x)*(tj.x-ti.x)+(tj.y-ti.y)*(tj.y-ti.y)+(tj.t-ti.t)*(tj.t-ti.t))
};

function tget_dist(ti,tj){
    return Math.sqrt((tj.x-ti.x)*(tj.x-ti.x)+(tj.y-ti.y)*(tj.y-ti.y)+(tj.t-ti.t)*(tj.t-ti.t))
};

function tfind_center(tr,tk,tset,ty,tz){
    var ti=0, tavg_x, tavg_y, tavg_t, tsum_x=0, tsum_y=0, tsum_t=0, tn=tk.length, tdist=0, tminspot=[], tmaxspot=[];
    tminspot.push({
        "x": tr[tk[0]].x,
        "y": tr[tk[0]].y,
        "t": tr[tk[0]].t
    });
    tmaxspot.push({
        "x": tr[tk[0]].x,
        "y": tr[tk[0]].y,
        "t": tr[tk[0]].t
    });
    for(ti=0;ti<tn;ti++){
        tsum_x += Number(tr[tk[ti]].x);
        tsum_y += Number(tr[tk[ti]].y);
        tsum_t += Number(tr[tk[ti]].t);
        tminspot[0].x = Math.min(tminspot[0].x, tr[tk[ti]].x);
        tminspot[0].y = Math.min(tminspot[0].y, tr[tk[ti]].y);
        tminspot[0].t = Math.min(tminspot[0].t, tr[tk[ti]].t);
        tmaxspot[0].x = Math.max(tminspot[0].x, tr[tk[ti]].x);
        tmaxspot[0].y = Math.max(tminspot[0].y, tr[tk[ti]].y);
        tmaxspot[0].t = Math.max(tminspot[0].t, tr[tk[ti]].t);
    }

    tavg_x = tsum_x/tn;
    tavg_y = tsum_y/tn;
    tavg_t = tsum_t/tn;
    tdist = tget_dist(tminspot[0], tmaxspot[0]);
    tdist = tdist/2;
    tset[tnum].x=tavg_x;
    tset[tnum].y=tavg_y;
    tset[tnum].t=tavg_t;
    tset[tnum].n=tk.length;
    tset[tnum].id=tr[tk[0]].cluster_id;
    tset[tnum].r=tdist;

    tnum++;
}

window.taddCluster = function(tdataX, tdataY, tdataT) {
    tinitSimpledbscanVariables();
    var tdata = [];
    var tdataDot=[];

    for (var ti = 0; ti < Math.min(Object.keys(tdataX).length, Object.keys(tdataY).length, Object.keys(tdataT)
.length); ti++) {
        tdata[ti] = {
            "x": tdataX[ti],
            "y": tdataY[ti],
            "t": tdataT[ti]
        };
        if (tdataDot[ti] == 1){
            tdataDot.push(tdata[ti]);
        }
    }

    for (var ti = 0; ti < Math.min(Object.keys(tdataX).length, Object.keys(tdataY).length, Object.keys(tdataT)
.length); ti++){
        tdata[ti] = {
            "x": tdataX[ti],
            "y": tdataY[ti],
            "t": tdataT[ti]
        };
    }

    for (ti in tdata) {
        tpoints.push({
            "x": tdata[ti].x,
            "y": tdata[ti].y,
            "t": tdata[ti].t * timeDimensionWeight,
            "cluster_id": -1
        });
        ++tnp;
    }

    for (ti in tpoints) {
        tpoints[ti].cluster_id = -1;
        tset_clust.push({
            "x": 0,
            "y": 0,
            "t": 0,
            "n": 0,
            "id": 0
         });
     }
    trun(tpoints, tnp, tepsilon, tminpts, teuclidean_dist, tset_clust);

    for (ti in tset_clust) {
        if(Number(tset_clust[ti].r)<=10){
            continue;
        }

        //tImgCtx.beginPath();
        //tImgCtx.globalAlpha = 0.5;
        //tImgCtx.arc(Number(tset_clust[ti].x),Number(tset_clust[ti].y), Number(tset_clust[ti].r/2), 0, (Math.PI / 180) * 360, true);

        //tImgCtx.fill();
        //tImgCtx.closePath();
        //tImgCtx.globalAlpha = 1.0;
    }

    for(ti in tpoints){
        for(tj in tset_clust){
            if(tpoints[ti].cluster_id==tset_clust[tj].id){
                if(tset_clust[tj].r>10){
                    //console.log("id : "+Number(points[i].cluster_id));
                    tarray_AOI.push({
                        "id":Number(tpoints[ti].cluster_id),
                        "n": tj
                    });
                }
            }
        }
    }

    //draw line
    var tAOI_number = tarray_AOI[0].id;
    var torder = 1;
    for(ti in tarray_AOI){
        if(ti==0){
            continue;
        }
        if(tAOI_number != tarray_AOI[ti].id){
            var tprev_n = tarray_AOI[ti-1].n;
            var tnext_n = tarray_AOI[ti].n;
            //tImgCtx.beginPath();
            //tImgCtx.moveTo(tset_clust[tprev_n].x, tset_clust[tprev_n].y);
            //tImgCtx.lineTo(tset_clust[tnext_n].x, tset_clust[tnext_n].y);
            //tImgCtx.fillText(torder, (tset_clust[tprev_n].x + tset_clust[tnext_n].x)/2, (tset_clust[tprev_n].y + tset_clust[tnext_n].y)/2);
            //tImgCtx.stroke();
            //tImgCtx.closePath();

            torder++;
            tAOI_number = tarray_AOI[ti].id;
        }
    }
}

window.taddClusterSpatialTemporal = function(_data) {
    tinitSimpledbscanVariables();
    var tdata = [];

    for (var ti = 0; ti<_data.length; ti++) {
        tdata[ti] = {
            "x": _data[ti].x,
            "y": _data[ti].y,
            "t": _data[ti].t
        };
    }

    for (ti in tdata) {
        tpoints.push({
            "x": tdata[i].x,
            "y": tdata[i].y,
            "t": tdata[ti].t*timeDimensionWeight,
            "cluster_id": -1
        });
        ++tnp;
    }

    for (ti in tpoints) {
        tpoints[ti].cluster_id = -1;
        tset_clust.push({
            "x": 0,
            "y": 0,
            "t": 0,
            "n": 0,
            "id": 0
         });
     }
    trun(tpoints, tnp, tepsilon, tminpts, teuclidean_dist, tset_clust);

    for (ti in tset_clust) {
        if(tset_clust[ti].r <= 10){
            continue;
        }

        //tImgCtx.beginPath();
        //tImgCtx.globalAlpha = 0.5;
        //tImgCtx.arc(tset_clust[ti].x, tset_clust[ti].y, tset_clust[ti].r/2, 0, (Math.PI/180)*360, true);
        //tImgCtx.fillStyle = tclrs[tset_clust[ti].id%12];
        //tImgCtx.fill();
        //tImgCtx.closePath();
        //tImgCtx.globalAlpha = 1.0;
    }

    for(ti in tpoints){
        for(tj in tset_clust){
            if(tpoints[ti].cluster_id==tset_clust[tj].id){
                if(tset_clust[tj].r>10){
                    tarray_AOI.push({
                        "id":Number(tpoints[ti].cluster_id),
                        "n": tj
                    });
                }
            }
        }
    }

    //draw line
    var tAOI_number = tarray_AOI[0].id;
    var torder = 1;
    for(ti in tarray_AOI){
        if(ti==0){
            continue;
        }
        if(tAOI_number != tarray_AOI[ti].id){
            var tprev_n = tarray_AOI[ti-1].n;
            var tnext_n = tarray_AOI[ti].n;
            //tImgCtx.beginPath();
            //ImgCtx.strokeStyle = "#e31a1c";
            //tImgCtx.lineWidth = 2.5;
            //tImgCtx.moveTo(tset_clust[tprev_n].x, tset_clust[tprev_n].y);
            //tImgCtx.lineTo(tset_clust[tnext_n].x, tset_clust[tnext_n].y);
            //tImgCtx.stroke();
            //tImgCtx.closePath();

            torder++;
            tAOI_number = tarray_AOI[ti].id;
        }
    }
}

window.tgetClusterSpatialTemporal = function(_data) {
    tinitSimpledbscanVariables();
    var tdata = [];

    for (var ti = 0; ti<_data.length; ti++) {
        tdata[ti] = {
            "x": _data[ti].x,
            "y": _data[ti].y,
            "t": _data[ti].t
        };
    }

    for (ti in tdata) {
        tpoints.push({
            "x": tdata[ti].x,
            "y": tdata[ti].y,
            "t": tdata[ti].t*timeDimensionWeight,
            "cluster_id": -1
        });
        ++tnp;
    }

    for (ti in tpoints) {
        tpoints[ti].cluster_id = -1;
        tset_clust.push({
            "x": 0,
            "y": 0,
            "t": 0,
            "n": 0,
            "id": 0
         });
     }
    trun(tpoints, tnp, tepsilon, tminpts, teuclidean_dist, tset_clust);

    var rArray = [];
    // temp!!!!!!!!!!!!!!!!
    //var clusterSize = 5;
    // temp!!!!!!!!!!!!!!!!
    for(var i=0; i<tset_clust.length; i++){

        if(Number(tset_clust[i].t) <= 0){
            continue;
        }

  
        rArray.push(tset_clust[i]);
    }

    return rArray;
}
// cluster end

import React, { useEffect, useRef } from 'react';

function SurfacePlot(props) {
  const { width, height, data } = props;
  const svgRef = useRef();
  const d3 = window.d3;

  useEffect(() => {
    if (typeof data !== 'object' || data.length === 0)
      return;

    var yaw=0.5,pitch=0.5,drag=false;

    /*var ul=d3.select('body')
             .append('ul');*/
    var svg = d3.select(svgRef.current)
      .attr('height',height)
      .attr('width',width);
  
    var group = svg.append("g");
  
    var md=group.data([data])
      .surface3D(width,height)
        .surfaceHeight(function(d){ 
          return d;
        }).surfaceColor(function(d){
          var c=d3.hsl((d+100), 0.6, 0.5).rgb();
          return "rgb("+parseInt(c.r)+","+parseInt(c.g)+","+parseInt(c.b)+")";
        });
  
    /*ul.selectAll('li')
      .data(surfaces)
        .enter().append('li')
          .html(function(d){
            return d.name
          }).on('mousedown',function(){
            md.data([d3.select(this).datum().data]).surface3D()
              .transition().duration(500)
              .surfaceHeight(function(d){
                return d;
              }).surfaceColor(function(d){
                var c=d3.hsl((d+100), 0.6, 0.5).rgb();
                return "rgb("+parseInt(c.r)+","+parseInt(c.g)+","+parseInt(c.b)+")";
              });
          });*/
  
    svg.on("mousedown",function(){
      drag=[d3.mouse(this),yaw,pitch];
    }).on("mouseup",function(){
      drag=false;
    }).on("mousemove",function(){
      if(drag){            
        var mouse=d3.mouse(this);
        yaw=drag[1]-(mouse[0]-drag[0][0])/50;
        pitch=drag[2]+(mouse[1]-drag[0][1])/50;
        pitch=Math.max(-Math.PI/2,Math.min(Math.PI/2,pitch));
        md.turntable(yaw,pitch);
      }
    });
  });

  return (
    <>
      {typeof data === 'object' && data.length > 0 &&
        <svg ref={svgRef}>
        </svg>
      }
    </>
  );
}

export default SurfacePlot;

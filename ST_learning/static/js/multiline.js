var myData = "date	s1	s2	s3	s4	s5\n\
20111001	1	1	1	1	1\n\
20111002	1	1	1	1	0.98\n\
20111003	0.9	0.91	0.99	0.97	0.96\n\
20111004	0.85	0.89	0.97	0.86	0.91\n\
20111005	0.8	0.8	0.76	0.86	0.87\n\
20111006	0.78	0.7	0.66	0.85	0.84\n\
20111007	0.76	0.6	0.56	0.8	0.79\n\
20111008	0.54	0.5	0.46	0.76	0.71\n\
20111009	0.43	0.4	0.36	0.72	0.69\n\
20111010	0.3	0.3	0.26	0.7	0.68\n\
20111011	0.25	0.29	0.16	0.68	0.65\n\
20111012	0.24	0.28	0.15	0.64	0.61\n\
20111013	0.23	0.26	0.14	0.6	0.5\n\
20111014	0.21	0.2	0.13	0.57	0.4\n\
20111015	0.19	0.18	0.12	0.4	0.37\n\
20111016	0.18	0.15	0.11	0.3	0.25\n\
20111017	0.17	0.14	0.1	0.2	0.22\n\
20111018	0.1	0.12	0.08	0.1	0.21\n\
20111019	0.09	0.1	0.05	0.09	0.18\n\
20111020	0.05	0.09	0.03	0.05	0.15\n\
20111021	0.03	0.05	0.03	0.04	0.1\n\
20111022	0.01	0.01	0.02	0.03	0.09\n";

var margin = {
top:20,
right:30,
bottom:20,
left:30
};

var w = 240;
var h = 80;

var parseDate = d3.timeParse("%Y%m%d"); //date parse

var scaleX = d3.scaleTime()
.range([0,w]);

var scaleY = d3.scaleLinear()
.range([h,0]);

var color = d3.scaleOrdinal(d3.schemeCategory10);

var xAxis = d3.axisBottom() //축 label 위치
.scale(scaleX);

var yAxis = d3.axisLeft()
.scale(scaleY)

var line = d3.line()
.x(function(d){
return scaleX(d.date)
})

.y(function(d){
return scaleY(d.autocorr)
})
.curve(d3.curveBasis);

var svg = d3.select("#lineplot").append("svg")
.attr("width",w + margin.left + margin.right)
.attr("height",h + margin.top + margin.bottom)
// .style("background-color","lightGreen")
.append("g")
.attr("transform","translate("+margin.left +","+margin.top+")")


var data = d3.tsvParse(myData); //tab data기준 - 추후 변경
//console.log("data :",data)

color.domain(d3.keys(data[0]).filter(function(key){
console.log("key",key)
return key!=="date";

}))


data.forEach(function(d){
d.date = parseDate(d.date);

});

var value = color.domain().map(function(name){ //변수명 추가
return {
  name:name,
  values:data.map(function(d){
    return {
      date:d.date,
      autocorr:+d[name]
    };
  })
};
});

scaleX.domain(d3.extent(data,function(d){
return d.date;
}));

scaleY.domain([d3.min(value,function(c){
return d3.min(c.values,function(v){
  return v.autocorr
})

}),d3.max(value,function(c){
return d3.max(c.values,function(v){
  return v.autocorr;
})
})])

//console.log("value",value);

var legend = svg.selectAll("g")
.data(value)
.enter()
.append("g")
.attr("class","legend");

legend.append("rect") //legend 사각형
.attr("x",w-20)
.attr("y",function(d,i){
return i * 9;
})
.attr("width",5)
.attr("height",5)
.style("fill",function(d){
return color(d.name);
});

legend.append("text")
.attr("x",w-9)
.attr("y",function(d,i){
return (i * 9) + 4;
})
.style("fill","#FFF")
.text(function(d){
return d.name;
});

svg.append("g")
.attr("class","x axis")
.attr("transform","translate(0,"+h+")")
.call(xAxis)
.selectAll("text")
.attr("dx","-1.2em")
.attr("dy",".80em")
.style("font-size","5px") //font size
.attr("transform","rotate(-75)");

svg.append("g")
.attr("class","y axis")
.call(yAxis)
.append("text")
.attr("transform","rotate(-90)")
.attr("x",-5)
.attr("y",-25)
.attr("dy",".91em")
.style("text-anchor","end")
.style("fill","white")
.text("auto-correlation coefficients"); //y축

var value = svg.selectAll(".value")
.data(value)
.enter().append("g")
.attr("class","value");

value.append("path")
.attr("class","line")
.attr("d",function(d){
return line(d.values);
})
.style("stroke",function(d){
return color(d.name)
}); //line

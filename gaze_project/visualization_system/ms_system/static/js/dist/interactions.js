$('#experimental').change(function(){
      change_pati(this.value);
    });

    function change_pati(s){
      
      console.log(data_res);
      if(s!='-'){
        $.ajax({
          type : 'POST',
          url : data_res,
          dataType : "json",
          data : {'name':s},
          success: function(data) { 
            draw_data=data;
          },
          error: function(jqXHR) {
              alert("error: " + jqXHR.status);
              console.log(jqXHR);
          }
        }); 

        $.ajax({
          type : 'POST',
          url : clusted_data,
          dataType : "json",
          data : {'name':s},
          success: function(data) { 
            temp=Object.values(data[0]);
            console.log(temp.length);
            for(var q = 0; q< temp.length;q++)
            {
              draw_clusted_data[q]=temp[q].split("/").map(function(item) {return parseInt(item, 10);});
              var tempsumx=0;
              var tempsumy=0;
              for(var w=0;w<draw_clusted_data[q].length;w+=3)
              {
                tempsumx+=draw_clusted_data[q][w+1];
                tempsumy+=draw_clusted_data[q][w+2];
              }
              tempsumx=parseInt(tempsumx/(draw_clusted_data[q].length/3));
              tempsumy=parseInt(tempsumy/(draw_clusted_data[q].length/3));
              draw_clusted_center[q]=[tempsumx,tempsumy];
              draw_clusted_std[q]=parseFloat(data[1][q], 10);
            }
          },
          error: function(jqXHR) {
              alert("error: " + jqXHR.status);
              console.log(jqXHR);
          }
        }); 

      }
      else
        draw_data=undefined;
        draw_clusted_data=[];
        draw_clusted_center=[];

    }


$('#imageselector').change(function(){
      change_exp(this.value);
    });

    function change_exp(s){
      console.log(s);
      if(!patient_list[s])
        return;
    /*
      $.ajax({
        type : 'POST',
        url : vs_intensity_data,
        dataType : "json",
        data : {'name':s},
        success: function(data) { 
          //console.log("intensity");
          _trow=Object.values(data);
          _tcol=Object.values(data[0]);
          _rowLen = _trow.length;
          _colLen = _tcol.length;
          if(vs_width < _colLen){
            vs_width = _colLen;
          }
          if(vs_height < _rowLen){
            vs_height = _rowLen;
          }
          
          for(var q=0; q<_rowLen; q++){
            var _rowArr = []
            for(var r=0; r<_colLen; r++){
              _rowArr.push(parseFloat(data[q][r]))

            }
            vs_intensity_feature.push(Object.values(_rowArr))
          }
          //console.log(vs_intensity_feature)
        },
        error: function(jqXHR) {
            alert("error: " + jqXHR.status);
            console.log(jqXHR);
        }   
      });

      $.ajax({
        type : 'POST',
        url : vs_color_data,
        dataType : "json",
        data : {'name':s},
        success: function(data) { 
          //console.log("color");
          _trow=Object.values(data);
          _tcol=Object.values(data[0]);
          _rowLen = _trow.length;
          _colLen = _tcol.length;
          if(vs_width < _colLen){
            vs_width = _colLen;
          }
          if(vs_height < _rowLen){
            vs_height = _rowLen;
          }

          for(var q=0; q<_rowLen; q++){
            var _rowArr = []
            for(var r=0; r<_colLen; r++){
              _rowArr.push(parseFloat(data[q][r]))

            }
            vs_color_feature.push(Object.values(_rowArr))
          }
          //console.log(vs_color_feature)
        },
        error: function(jqXHR) {
            alert("error: " + jqXHR.status);
            console.log(jqXHR);
        }
      });

      $.ajax({
        type : 'POST',
        url : vs_orientation_data,
        dataType : "json",
        data : {'name':s},
        success: function(data) { 
          //console.log("orientation");
          _trow=Object.values(data);
          _tcol=Object.values(data[0]);
          _rowLen = _trow.length;
          _colLen = _tcol.length;
          if(vs_width < _colLen){
            vs_width = _colLen;
          }
          if(vs_height < _rowLen){
            vs_height = _rowLen;
          }

          for(var q=0; q<_rowLen; q++){
            var _rowArr = []
            for(var r=0; r<_colLen; r++){
              _rowArr.push(parseFloat(data[q][r]))

            }
            vs_orientation_feature.push(Object.values(_rowArr))
          }
          //console.log(vs_orientation_feature)
        },
        error: function(jqXHR) {
            alert("error: " + jqXHR.status);
            console.log(jqXHR);
        }
      });

      $.ajax({
        type : 'POST',
        url : vs_saliency_data,
        dataType : "json",
        data : {'name':s},
        success: function(data) { 
          //console.log("orientation");
          _trow=Object.values(data);
          _tcol=Object.values(data[0]);
          _rowLen = _trow.length;
          _colLen = _tcol.length;
          if(vs_width < _colLen){
            vs_width = _colLen;
          }
          if(vs_height < _rowLen){
            vs_height = _rowLen;
          }

          for(var q=0; q<_rowLen; q++){
            var _rowArr = []
            for(var r=0; r<_colLen; r++){
              _rowArr.push(parseFloat(data[q][r]))

            }
            vs_saliency_feature.push(Object.values(_rowArr))
          }
          //console.log(vs_orientation_feature)
        },
        error: function(jqXHR) {
            alert("error: " + jqXHR.status);
            console.log(jqXHR);
        }
      });
    */

      $('#experimental').html("<option>-</option>");

      for(var i=0;i<patient_list[s]['id'].length;i++)
      {
        var temptag = patient_list[s]['id'][i];
        
          $('#experimental').append('<option>'+temptag+'\
                                  </option>');  
      }

    }



$('#visualization').change(function(){
      change_vis(this.value);
    });

    function change_vis(s){
      console.log(s);
      

      if(!params_list[s])
        return;



      $('#parameters').html("");

      for(var i=0;i<params_list[s]['tag'].length;i++)
      {
        var temptag = params_list[s]['tag'][i];
        var tempval = params_list[s]['val'][i];
        if(params_list[s]['tag'][i]=="text")
        {
          $('#parameters').append('<div class="form-group row mt-2">\
                                  <label class="f10 col-8 col-form-label" for="'+tempval+'">'+tempval+'</label>\
                                  <input type="'+temptag+'" class="form-control f10 col-3 mx-auto" id="'+tempval+'" >\
                                  </div>');  
        }
        else if(params_list[s]['tag'][i]=="checkbox")
        {
          $('#parameters').append('<div class="form-group row mt-2">\
                                  <label class="f10 col-8 col-form-label" for="'+tempval+'">'+tempval+'</label>\
                                  <input type="'+temptag+'" class="form-control f10 col-3 mx-auto" id="'+tempval+'" >\
                                  </div>');  
        }
      }

    }


$('#imageselector').change(function(){
    if(this.value=="-")
      clear_canvas();
    else
      draw_image();
    });

$('#drawbutton').click(function(){

  draw_vis($('#visualization option:selected').val());
  
});

$('#imgbutton').click(function(){

  imageC();
  console.log(sb_back)
  
});


download_img = function(el) {
  var image = c.toDataURL("image/jpg");
  el.href = image;
};

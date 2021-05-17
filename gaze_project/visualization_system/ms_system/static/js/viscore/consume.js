function consume(){
	var tempobj={};
	var temptags = $('#parameters').find('input');
	
	for(var i =0;i<temptags.length;i++)
		tempobj[temptags[i].id]=Number(temptags[i].value);

	console.log(tempobj);
	return tempobj;
}
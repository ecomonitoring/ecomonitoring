var inp_id='';

window.onload = function(){
	var search_items=document.getElementById("Elements");
	var string='';
	for (var i = 0; i < 856; i++)
	{
		string += '<a onclick="ChooseClose(\'' + substance[i]+'\');">' + substance[i] +'</a>';
	}
	search_items.innerHTML = string;
	return;
}

function Opener(table_id, elem_id)
{
	inp_id=elem_id;
	console.log(inp_id);

	console.log(document.getElementById('Elements'));
	console.log(document.getElementById(table_id));
	document.getElementById(table_id).appendChild( document.getElementById('Elements') );

	document.getElementById("Elements").classList.toggle("show");
}


function openEnviroment(evt, enviromentName) {
  var i, tabcontent, tablinks;
  tabcontent = document.getElementsByClassName("tabcontent");
  for (i = 0; i < tabcontent.length; i++) {
    tabcontent[i].style.display = "none";
  }
  tablinks = document.getElementsByClassName("tablinks");
  for (i = 0; i < tablinks.length; i++) {
    tablinks[i].className = tablinks[i].className.replace(" active", "");
  }
  document.getElementById(enviromentName).style.display = "block";
  evt.currentTarget.className += " active";
  }

function data_sender(id, url) {
	var data=data_former(id);
	sender(data,url);
	return;
}

function sender(data, url) {
    var x=new XMLHttpRequest();
    x.onreadystatechange=function(){
        if(this.readystate==4 && this.status==200)
		{
			alert('Отправлено');
		}
	}
	x.open('PUT',url,true);
	x.send(data);
	}

function data_former(form_id){
	var form=document.getElementById(form_id);
	var formData=new FormData(form);
	var output={};
	formData.forEach(function(k,v){
		output[k]=v;
		});
	return output;
}

function ChooseClose(name){
	console.log(name);
	document.getElementById(inp_id).value=name;
	document.getElementById('Elements').classList.toggle("show");
}

function filterFunction() {
  var input, filter, ul, li, a, i;
  input = document.getElementById(inp_id);
  filter = input.value.toUpperCase();
  div = document.getElementById("Elements");
  a = div.getElementsByTagName("a");
  for (i = 0; i < a.length; i++) {
    txtValue = a[i].textContent || a[i].innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      a[i].style.display = "";
    } else {
      a[i].style.display = "none";
    }
  }
}

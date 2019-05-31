var inp_id='';

window.onload = function(){

	document.getElementById("request_table").style.visibility = "hidden";

	var search_items=document.getElementById("Elements");
	var string='';
	for (var i = 0; i < 856; i++)
	{
		string += '<a onclick="ChooseClose(\'' + substance[i]+ '\','+ i +');">' + substance[i] +'</a>';
	}
	search_items.innerHTML = string;
	return;
}

function Opener(table_id, elem_id)
{
	inp_id=elem_id;
	//console.log(inp_id);

	//console.log(document.getElementById('Elements'));
	//console.log(document.getElementById(table_id));
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
	var sdata=JSON.stringify(data);
	//console.log(sdata);
	sender(sdata,url);
	form_clear(id);

	return;
}

function form_clear(id) {
	var form=document.getElementById(id);
	form.reset();
	return;
}

function sender(data, url) {
    var x=new XMLHttpRequest();

    x.onreadystatechange=function(){
	if(this.readyState==4 && this.status==200)
		{
			//alert("ok");
			//console.log(this.responseText);
			var recv_data = JSON.parse(this.responseText);
			console.log(recv_data)
			document.getElementById("request_table").style.visibility = "visible";
			document.getElementById(recv_data['pid']).appendChild(document.getElementById("request_table"));
			//document.getElementById("request_table").style.visibility = "visible";
			//console.log(recv_data);
			document.getElementById("p_adult").innerHTML = recv_data["p_adult"];
			document.getElementById("p_child").innerHTML = recv_data["p_child"];
			document.getElementById("c_necan").innerHTML = recv_data["c_necan"];
			document.getElementById("a_necan").innerHTML = recv_data["a_necan"];
			document.getElementById("p_c_can").innerHTML = recv_data["p_c_can"];
			document.getElementById("p_a_can").innerHTML = recv_data["p_a_can"];
			document.getElementById("pop_can").innerHTML = recv_data["pop_can"];
			as_can = document.getElementById("assessment_can");
			if (recv_data["assessment_can"] == 1) {
				as_can.innerHTML='<font color=#4cbb17>Допустимо</font>';
			}
			if (recv_data["assessment_can"] == 2) {
				as_can.innerHTML='<font color=#808000>Низкий</font>';
			}
			if (recv_data["assessment_can"] == 3) {
				as_can.innerHTML='<font color=#ffff00>Средний</font>';
			}

			if (recv_data["assessment_can"] == 4) {
				as_can.innerHTML='<font color=#ff6600>Высокий</font>';
			}

			if (recv_data["assessment_can"] == 5) {
				as_can.innerHTML='<font color=#ff0000>Чрезвычайно опасный</font>';
		        }
		}
	}
    x.open('PUT',url,true);
    x.send(data);

    //console.log(recv_data);
}

function data_former(form_id){
	var form=document.getElementById(form_id);
	var formData=new FormData(form);
	var output={};
	formData.forEach(function(v,k){
		output[k]=v;
		});
	if (1)  return output;
	else 
	{
		alert("Неправильный ввод данных");
		return output;
	}
}

function ChooseClose(name, key){
	var elem_id="Id"+inp_id;
	//console.log(name);
	document.getElementById(elem_id).value=key;
	document.getElementById(inp_id).value=name;
	document.getElementById("req_elem").innerHTML = name;
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

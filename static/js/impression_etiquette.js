
function retour_impression(data, status)
	{
	if (status != "success")
		{
		alert("Echec d'impression");
		}
	else
		{
		if (data["status"] == "ok")
			{
			document.getElementById(data["cellule_id"]).style.background = "lightgreen";
			}
		else
			{
			document.getElementById(data["cellule_id"]).style.background = "red";
			}
		}
	}
function retour_impression_etiquette(data, status)
	{
	retour_impression(data, status);
	document.getElementById(data["cellule_id"]).children[0].src = "/static/svg/document-print.svg";
	}
function etiquette(cellule, id, type_etiquette)
	{
	cellule.style.background = "orange";
	url = "/django/stock_labo/ajax_etiquette/";
	param = "?type_etiquette=" + type_etiquette;
	param += "&id=" + id;
	param += "&cellule_id=" + cellule.id;
	$.get(url + param, retour_impression_etiquette);
	}



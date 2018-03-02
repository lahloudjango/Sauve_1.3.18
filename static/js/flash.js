


function select_onchange_mode(cellule)
    { // Onchange element
	form = document.getElementById("id_mode_form");
	form.submit()
    }   

function text_onkeypress_vue(cellule)
	{ // OnPressKey event
	if (cellule.id == "id_machine")
		{
		form = document.getElementById("id_mode_form");
		form.submit()
		}
	}
	
function text_onkeypress_charge(cellule)
	{ // OnPressKey event
	if (cellule.id == "id_contenant")
		{
		document.getElementById("id_empl_flash").focus();
		}
	if (cellule.id == "id_empl_flash")
		{
		form = document.getElementById("id_mode_form");
		form.submit()
		}
	}

function text_onkeypress_enregistrement(cellule)
	{ // OnPressKey event
	if (cellule.id == "id_contenant")
		{
		document.getElementById("id_flash_point").focus();
		}
	if (cellule.id == "id_flash_point")
		{
		document.getElementById("id_empl_sortie").focus();
		}
	if (cellule.id == "id_empl_sortie")
		{
		form = document.getElementById("id_mode_form");
		form.submit()
		}
	}




// Projet input ajax 
	function id_projet_input_ajax_receipt(data, status)
	{
		if (projet_ajax_val === $("#id_projet").val())
		{
			if (data.length === 1)
			{
				$("#id_projet_list").empty();
				$("#id_projet").val(data[0]["PROJET"]);
				$("#id_client").val(data[0]["CLIENT"]);
				$("#id_client_ka").val(data[0]["CLIENT_KA"]);
				$("#id_nbr_echantillon").focus();
			}
			else
			{
				$("#id_projet_list").empty();
				for (i = 0; i < data.length; i++)
				{
					$("#id_projet_list").append("<option>" + data[i]["PROJET"] + "</option>");
				}
			}
		}
	}
	function id_projet_input_ajax()
	{
		projet_ajax_val = $("#id_projet").val();
		$("#id_projet_list").empty();
		url = "/django/stock_labo/ajax_sample_lab_projet/";
		param = "?projet=" + $("#id_projet").val();
		$.get(url + param, id_projet_input_ajax_receipt);
	}
	function id_projet_input()
	{
		window.clearTimeout(window.id_projet_input_timeout);
		window.id_projet_input_timeout = setTimeout(id_projet_input_ajax, 800);
	}
	$(document).ready(function()
	{
		$("#id_projet").bind("input", id_projet_input );
	});

// Client input ajax 
	function id_client_input_ajax_receipt(data, status)
	{
		if (client_ajax_val === $("#id_client").val())
		{
			if (data.length === 1)
			{
				$("#id_client_list").empty();
				$("#id_client").val(data[0]["CLIENT"]);
				$("#id_client_ka").focus();
			}
			else
			{
				$("#id_client_list").empty();
				for (i = 0; i < data.length; i++)
				{
					$("#id_client_list").append("<option>" + data[i]["CLIENT"] + "</option>");
				}
			}
		}
	}
	function id_client_input_ajax()
	{
		client_ajax_val = $("#id_client").val();
		$("#id_client_list").empty();
		url = "/django/stock_labo/ajax_sample_lab_client/";
		param = "?projet=" + $("#id_projet").val();
		param += "&client=" + $("#id_client").val();
		$.get(url + param, id_client_input_ajax_receipt);
	}
	function id_client_input()
	{
		window.clearTimeout(window.id_client_input_timeout);
		window.id_client_input_timeout = setTimeout(id_client_input_ajax, 800);
	}
	$(document).ready(function()
	{
		$("#id_client").bind("input", id_client_input );
	});
// Client focus ajax 
	function id_client_focus()
	{
		window.clearTimeout(window.id_client_focus_timeout)
		window.id_client_focus_timeout = setTimeout(id_client_input_ajax, 500);
	}
	$(document).ready(function()
	{
		$("#id_client").bind("focus", id_client_focus );
	});

// Client KA input ajax 
	function id_client_ka_input_ajax_receipt(data, status)
	{
		if (client_ka_ajax_val === $("#id_client_ka").val())
		{
			if (data.length === 1)
			{
				$("#id_client_ka_list").empty();
				$("#id_client_ka").val(data[0]["CLIENT_KA"]);
				$("#id_nbr_echantillon").focus();
			}
			else
			{
				$("#id_client_ka_list").empty();
				for (i = 0; i < data.length; i++)
				{
					$("#id_client_ka_list").append("<option>" + data[i]["CLIENT_KA"] + "</option>");
				}
			}
		}
	}
	function id_client_ka_input_ajax()
	{
		client_ka_ajax_val = $("#id_client_ka").val();
		$("#id_client_ka_list").empty();
		url = "/django/stock_labo/ajax_sample_lab_client_ka/";
		param = "?projet=" + $("#id_projet").val();
		param += "&client=" + $("#id_client").val();
		param += "&client_ka=" + $("#id_client_ka").val();
		$.get(url + param, id_client_ka_input_ajax_receipt);
	}
	function id_client_ka_input()
	{
		window.clearTimeout(window.id_client_ka_input_timeout);
		window.id_client_ka_input_timeout = setTimeout(id_client_ka_input_ajax, 800);
	}
	$(document).ready(function()
	{
		$("#id_client_ka").bind("input", id_client_ka_input );
	});
// Client KA focus ajax 
	function id_client_ka_focus()
	{
		window.clearTimeout(window.id_client_ka_focus_timeout)
		window.id_client_ka_focus_timeout = setTimeout(id_client_ka_input_ajax, 500);
	}
	$(document).ready(function()
	{
		$("#id_client_ka").bind("focus", id_client_ka_focus );
	});








#!/usr/bin/bash



PY=`find $1 -iname "*.py" | grep -v "__"`
HTML=`find $1 -iname "*.html"`
CSS=`find $1 -iname "*.css"`

case "$2" in
	geany)
		geany &
		sleep 1
		for f in $PY $HTML $CSS
		do
			geany $f
		done
		;;
	wc)
		echo "Nonbre de fichiers"
		for f in $PY $HTML $CSS
			do echo "$f"
		done | wc -l
		echo "Nombre de lignes"
		for f in $PY $HTML $CSS
			do cat $f | grep -v -e "^$"
		done | wc -l
		;;
	*)
		echo "Option 1 : dossier de recherche\n"
		echo "Option 2 : action\n"
		echo "	wc : compter les lignes\n"
		echo "	geany : edition des fichier\n"
esac

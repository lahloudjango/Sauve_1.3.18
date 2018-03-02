#!/bin/sh
### BEGIN INIT INFO
# Provides:          django_io
# Required-Start:    $local_fs $remote_fs $network $syslog $named
# Required-Stop:     $local_fs $remote_fs $network $syslog $named
# Default-Start:     5
# Default-Stop:      0 1 2 3 4 6
# X-Interactive:     false
# Short-Description: Le deamon gère l'import automatique des fichier envoyé a l'application stock labo
# Description:
### END INIT INFO

DESC="Le deamon gère l'import automatique des fichier envoyé a l'application stock labo"

DAEMON="/var/www/django/prod/daemon/django_io.py"		#ligne de commande du programme
daemon_OPT=""											#argument à utiliser par le programme
DAEMONUSER="root"										#utilisateur du programme
daemon_NAME=`basename $DAEMON`							#Nom du programme (doit être identique à l'exécutable)
PIDFILE="/var/run/django.pid"

if [ ! -x $DAEMON ]
then
	echo "!!!!!  Le deamon n'existe pas  !!!!!"
	exit 0
fi

d_check ()
{
	PROSS=`ps -ef | grep "$DAEMON" | grep -v "grep"`
	echo $PROSS
	if [ -n "$PROSS" ]
	then
		if [ -f $PIDFILE ]
		then
			return 1 #Le deamon fonctionne
		else
			return 2 #Le deamon fonctionne mais sans fichier PID
		fi
	else
		if [ -f $PIDFILE ]
		then
			return 3 #Le deamon est arrêté mais le fichier PID est toujours présent
		else
			return 0 #Le deamon est arrêté
		fi
	fi
}

d_start ()
{
	echo "Démarrage du deamon $daemon_NAME"
		d_check
		case $? in
		0)
			/sbin/start-stop-daemon --make-pidfile --pidfile $PIDFILE --background --name $daemon_NAME --start --quiet --chuid $DAEMONUSER --exec $DAEMON -- $daemon_OPT
		;;
		1)
			echo "Le deamon fonctionne déjà"
		;;
		2)
			echo "Le deamon fonctionne mais sans fichier PID"
		;;
		3)
			echo "Le deamon est arrêté mais le fichier PID est toujours présent"
		;;
		*)
			echo "Statut inconnu"
		;;
		esac
}

d_stop ()
{
	echo "Arrêt du deamon $daemon_NAME"
	d_check
	case $? in
		0)
			echo "Le deamon est déjà arrêté"
		;;
		1)
			/sbin/start-stop-daemon --pidfile $PIDFILE --name $daemon_NAME --stop --signal 2 --retry 5 --quiet --name $daemon_NAME
			/bin/rm $PIDFILE
			echo "Le deamon est arrêté"
		;;
		2)
			echo "Le deamon fonctionne mais sans fichier PID"
			echo "Deamon arrêt impossible"
			echo "Utilisé le paramêtre force-stop pour arrêter/méttoyer le daemon"
		;;
		3)
			echo "Le deamon est arrêté mais le fichier PID est toujours présent"
			echo "Erreur commande status"
			echo "Utilisé le paramêtre force-stop pour arrêter/méttoyer le daemon"
		;;
		*)
			echo "Erreur inconnu"
		;;
	esac
}

case "$1" in
	start)
		d_start
	;;

	stop)
		d_stop
	;;

	restart)
		d_stop
		d_start
	;;

	force-stop)
		d_stop
		killall -q $daemon_NAME || true
		/bin/rm $PIDFILE
		sleep 2
		killall -q -9 $daemon_NAME || true
	;;

	status)
		d_check
		case $? in
		0)
			echo "Le deamon est arrêté"
		;;
		1)
			echo "Le deamon fonctionne"
		;;
		2)
			echo "Le deamon fonctionne mais sans fichier PID"
		;;
		3)
			echo "Le deamon est arrêté mais le fichier PID est toujours présent"
		;;
		*)
			echo "Statut inconnu"
		;;
		esac
	;;

	*)
		echo "Usage: /etc/init.d/$daemon_NAME {start|stop|force-stop|restart|status}"
		exit 1
	;;

esac

exit 0

#!/bin/sh

### BEGIN INIT INFO
# Provides:          server TCP<=>RS232
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: Server de pont TCP <=> RS232
# Description:       Ce server permet d'accéder à un port serie 
#                    de la machine hote via un port TCP
### END INIT INFO

# Author: Charly GONTERO <charly.gontero@linautom.fr>

DESC="Server TCP<=>RS232"
#DAEMON=/usr/sbin/daemon


case "$1" in
  start)
	/usr/bin/python /etc/init.d/server_tcp-rs232.py &
	;;

  stop)
	echo "Pas de stop"
	;;

  restart)
	echo "Pas de restart"
	;;


  status)
	/sbin/ifconfig eth0
	;;

  *)
	echo "Usage: /etc/init.d/ssh {start|stop|restart|status}"
	exit 1
esac

exit 0





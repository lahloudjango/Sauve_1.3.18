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
PYTHON="/usr/bin/python"
SERVICE="/etc/init.d/server_tcp_rs232.py"

case "$1" in
	start)
		$PYTHON $SERVICE &
		;;

	stop)
		kill -s TERM `ps -ef | grep "server_tcp_rs232.py" | grep -v grep | cut --delimiter=" " -f3`
		;;

	kill)
		kill -s KILL `ps -ef | grep "server_tcp_rs232.py" | grep -v grep | cut --delimiter=" " -f3`
		;;

	restart)
		kill -s TERM `ps -ef | grep "server_tcp_rs232.py" | grep -v grep | cut --delimiter=" " -f3`
		sleep 2
		$PYTHON $SERVICE &
		echo "Pas de restart"
		;;

	status)
		netstat -laputn | grep python
		;;

  *)
	echo "Usage: /etc/init.d/ssh {start|stop|restart|status|kill}"
	exit 1
esac

exit 0





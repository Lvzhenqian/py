#!/bin/bash
start(){
	nohup jupyter-notebook &> /tmp/jupyter.log &
}
id=$(ps aux|grep [j]upyter-notebook|awk '{print $2}')
stop(){
	[ -z "${id}" ] && echo "Not start The Jupyter." && exit 0;
	kill -9 ${id}
}

status(){
	ps aux|grep [j]upyter-notebook
}
main(){
	case $1 in 
	    start)
	        start;;
	    stop)
		stop;;
	    status)
		status;;
	    *)
		echo "Use:[start|stop|status]"
	esac
}
main "$*"

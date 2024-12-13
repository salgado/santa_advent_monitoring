#!/bin/bash

# Configurar diretório de logs (mudando para caminho relativo)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
LOG_DIR="$SCRIPT_DIR/var/log/workshop/production"

# Criar diretório de logs se não existir
mkdir -p $LOG_DIR
chmod 755 $LOG_DIR

# Função para iniciar a geração de logs
start_generation() {
    echo "Starting toy production simulation..."
    python3 $SCRIPT_DIR/toy_workshop_simulator.py >> "$LOG_DIR/toys.log" 2>&1 &
    echo $! > $SCRIPT_DIR/simulator.pid
    echo "Simulation started! PID saved in simulator.pid"
    echo "Logs will be written to: $LOG_DIR/toys.log"
}

# Função para parar a geração de logs
stop_generation() {
    if [ -f "$SCRIPT_DIR/simulator.pid" ]; then
        echo "Stopping toy production simulation..."
        kill $(cat "$SCRIPT_DIR/simulator.pid") 2>/dev/null || echo "Process already stopped"
        rm "$SCRIPT_DIR/simulator.pid"
        echo "Simulation stopped!"
    else
        echo "No running simulation found!"
    fi
}

# Função para mostrar status
show_status() {
    if [ -f "$SCRIPT_DIR/simulator.pid" ]; then
        PID=$(cat "$SCRIPT_DIR/simulator.pid")
        if ps -p $PID > /dev/null; then
            echo "Simulation is running with PID: $PID"
            echo "Log file location: $LOG_DIR/toys.log"
            echo "Last 5 log entries:"
            tail -n 5 "$LOG_DIR/toys.log"
        else
            echo "PID file exists but process is not running. Cleaning up..."
            rm "$SCRIPT_DIR/simulator.pid"
            echo "No simulation is currently running"
        fi
    else
        echo "No simulation is currently running"
    fi
    
    # Mostrar tamanho do arquivo de log
    if [ -f "$LOG_DIR/toys.log" ]; then
        echo -e "\nLog file size:"
        ls -lh "$LOG_DIR/toys.log"
    fi
}

# Função para limpar logs antigos
clean_logs() {
    echo "Cleaning old logs..."
    if [ -f "$LOG_DIR/toys.log" ]; then
        mv "$LOG_DIR/toys.log" "$LOG_DIR/toys.log.$(date +%Y%m%d-%H%M%S).bak"
        echo "Old logs backed up"
    fi
    echo "Log cleaning completed"
}

# Processar argumentos
case "$1" in
    start)
        start_generation
        ;;
    stop)
        stop_generation
        ;;
    status)
        show_status
        ;;
    clean)
        clean_logs
        ;;
    restart)
        stop_generation
        sleep 2
        start_generation
        ;;
    *)
        echo "Usage: $0 {start|stop|status|clean|restart}"
        exit 1
        ;;
esac

exit 0
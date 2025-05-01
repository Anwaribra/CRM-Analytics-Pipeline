#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to check if PostgreSQL is running
check_postgres() {
    echo -e "${GREEN}Checking PostgreSQL status...${NC}"
    if systemctl is-active --quiet postgresql; then
        echo -e "${GREEN}PostgreSQL is running${NC}"
    else
        echo -e "${RED}PostgreSQL is not running. Starting PostgreSQL...${NC}"
        sudo systemctl start postgresql
        sleep 5
    fi
}

# Function to start services
start_services() {
    echo -e "${GREEN}Starting Airflow services...${NC}"
    docker-compose up -d
    echo -e "${GREEN}Waiting for services to initialize...${NC}"
    sleep 30
    echo -e "${GREEN}Airflow services started successfully!${NC}"
    echo -e "${GREEN}Access Airflow UI at: http://localhost:8080${NC}"
    echo -e "${GREEN}Default credentials: airflow/airflow${NC}"
}

# Function to stop services
stop_services() {
    echo -e "${GREEN}Stopping Airflow services...${NC}"
    docker-compose down
    echo -e "${GREEN}Airflow services stopped successfully!${NC}"
}

# Function to show logs
show_logs() {
    echo -e "${GREEN}Showing Airflow logs...${NC}"
    docker-compose logs -f
}

# Function to restart services
restart_services() {
    stop_services
    start_services
}

# Main script
case "$1" in
    start)
        check_postgres
        start_services
        ;;
    stop)
        stop_services
        ;;
    restart)
        check_postgres
        restart_services
        ;;
    logs)
        show_logs
        ;;
    status)
        docker-compose ps
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|logs|status}"
        exit 1
        ;;
esac

exit 0 
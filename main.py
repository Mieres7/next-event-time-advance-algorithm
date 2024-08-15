import getopt
import sys
import numpy
from FEL import FEL
from Event import Event
from Server import Server


def exponentialVariate(a):
    u = numpy.random.uniform(low=0.0, high=1.0)
    return -(1/a)*numpy.log(1-u)



def main():
    # Definir los valores por defecto
    arrival_rate = None
    service_rate = None
    end_time = None

    # Definir las opciones cortas y largas
    opts, args = getopt.getopt(sys.argv[1:], "a:d:t:", ["arrival-rate=", "service-rate=", "end-time="])

    for opt, arg in opts:
        if opt in ("-a", "--arrival-rate"):
            arrival_rate = int(arg)
        elif opt in ("-d", "--service-rate"):
            service_rate = int(arg)
        elif opt in ("-t", "--end-time"):
            end_time = int(arg)


    print(arrival_rate)

    server = Server()
    fel = FEL()

    # inital state 
    arrival_0 = Event("A", arrival_rate)
    arrival_0.arrivalTime = exponentialVariate(arrival_rate)
    arrival_0.serviceTime = exponentialVariate(service_rate)
    fel.pushEvent(arrival_0)
    endEvent = Event("E", end_time)
    fel.pushEvent(endEvent)

    while(server.time <= endEvent.arrivalTime):
        
        event = fel.popEvent()
        if(event.eType == "A"):
            server.arrivals += 1
            if(server.busy):



        elif(event.eType == "D"):
            server.departures += 1
            print(4)


    '''
    stats que necesito:
    jobs arrived -> server
    jobs departured -> server
    tiempo total de la cola vacia ->
    largo maximo de la cola -> stat de la fel
    tiempo total de la cola con largo maixmo -> suma de todos los tiempos de la cola creo
    '''

    
    





    


if __name__ == "__main__":
    main()
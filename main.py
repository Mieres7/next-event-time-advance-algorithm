import getopt
import sys
import numpy
from FEL import FEL
from Event import Event
from Server import Server


def exponentialVariate(a):
    u = numpy.random.uniform()
    return -numpy.log(1-u)/a

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

    server = Server()
    fel = FEL()

    # inital state 
    arrival_0 = Event("A", arrival_rate)
    arrival_0.arrivalTime = exponentialVariate(arrival_rate)
    # arrival_0.serviceTime = exponentialVariate(service_rate)
    fel.pushEvent(arrival_0)

    endEvent = Event("E", end_time)
    

    while(server.time < endEvent.arrivalTime):
        
        event = fel.popEvent()
        print(event)
        # print(server.time)
        
        if(event.eType == "A"):
            
            
            server.arrivals += 1
            if(server.busy):
                
                # fel.pushEvent(event)
                if len(fel.eventList) > fel.maxLength : fel.maxLength = len(fel.eventList)
            else: 
                server.busy = True
                serviceTime = exponentialVariate(service_rate)
                departure = Event("D", server.time + serviceTime)
                fel.pushEvent(departure)
                if len(fel.eventList) > fel.maxLength : fel.maxLength = len(fel.eventList)

            interArrivalTime = exponentialVariate(arrival_rate)
            arrival = Event("A", server.time + interArrivalTime)
            fel.pushEvent(arrival)
            if len(fel.eventList) > fel.maxLength : fel.maxLength = len(fel.eventList)

        elif(event.eType == "D"):
            # server.time += event.arrivalTime
            server.departures += 1
            if(len(fel.eventList) > 0):
                serviceTime = exponentialVariate(service_rate)
                departure = Event("D", server.time + serviceTime)
            else: 
                server.busy = False
        
        server.time += event.arrivalTime
                
    # print(server.arrivals)
    # print(server.departures)
    print("olamklefur")
    print(server.time)
    # print(fel.maxLength)



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
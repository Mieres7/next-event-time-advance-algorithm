import getopt
import sys
import numpy as np
from FEL import FEL
from Event import Event
from Server import Server

def exponentialVariate(a):
    return -np.log(1.0 - np.random.uniform()) / a

def theoricalAverageLenght(arrivalRate, serviceRate):
    if serviceRate > arrivalRate:
        return (arrivalRate ** 2) / (serviceRate * (serviceRate - arrivalRate))
    else:
        return float('inf')  

def main():

    # generates random seed for testing
    # np.random.seed(0) 

    arrival_rate = None
    service_rate = None
    end_time = None

    opts, args = getopt.getopt(sys.argv[1:], "a:d:t:", ["arrival-rate=", "service-rate=", "end-time="])

    for opt, arg in opts:
        if opt in ("-a", "--arrival-rate"):
            arrival_rate = float(arg)
        elif opt in ("-d", "--service-rate"):
            service_rate = float(arg)
        elif opt in ("-t", "--end-time"):
            end_time = float(arg)

    server = Server()
    fel = FEL()

    # Initial state
    firstEvent = Event("A", 0, 0)
    fel.pushEvent(firstEvent)
    endEvent = Event("E", end_time, 0)
    fel.pushEvent(endEvent)

    # Metrics
    timeQueueEmpty = 0.0
    lasEventTime = 0.0
    Q_k = {}
    arrivalTimes = {}
    totalResidenceTime = 0.0


    while server.time < endEvent.arrivalTime:

        currentEvent = fel.popEvent()
        server.time = currentEvent.arrivalTime

        
        # Computes time where tail was empty before that event
        if fel.length == 0:
            timeQueueEmpty += server.time - lasEventTime

        # Save times at their respective lenght k 
        if fel.length in Q_k:
            Q_k[fel.length] += server.time - lasEventTime
        else:
            Q_k[fel.length] = server.time - lasEventTime

        if currentEvent.eType == "A":
            server.arrivals += 1
            arrivalTimes[server.arrivals] = server.time

            if not server.busy:
                server.busy = True
                serviceTime = exponentialVariate(service_rate)
                departureTime = server.time + serviceTime
                departure = Event("D", departureTime, serviceTime)
                departure.job_id = server.arrivals # saves job id to identificate them later on Q_k
                fel.pushEvent(departure)
            else:
                fel.length += 1
                
            interArrivalTime = exponentialVariate(arrival_rate)
            nextArrivalEvent = Event("A", server.time + interArrivalTime, 0)
            nextArrivalEvent.job_id = server.arrivals
            fel.pushEvent(nextArrivalEvent)

        elif currentEvent.eType == "D":
            server.departures += 1


            # Calculate the residence time
            job_id = currentEvent.job_id
            if job_id in arrivalTimes:
                residenceTime = server.time - arrivalTimes[job_id]
                totalResidenceTime += residenceTime

            if fel.length > 0:
                fel.length -= 1
                serviceTime = exponentialVariate(service_rate)
                departureEvent = Event("D", server.time + serviceTime, serviceTime)
                departureEvent.job_id = currentEvent.job_id # saves job id to identificate them later on Q_k
                fel.pushEvent(departureEvent)
            else:
                server.busy = False

        elif currentEvent.eType == "E":
            break

        lasEventTime = server.time # updates last event time

    # Cálculo del largo promedio de la cola
    QT = sum(Q_k.values()) 
    avergeQueueLength = sum(k * Q_k[k] for k in Q_k) / QT
    # Cálculo del largo teórico de la cola
    theoAvgLenght = theoricalAverageLenght(arrival_rate, service_rate)

    # Cálculo del tiempo promedio de residencia
    averegaResidenceTime = totalResidenceTime / server.departures

    # Metrics calculation
    print(f"\nNúmero de jobs que llegaron: {server.arrivals}")
    print(f"Número de jobs que salieron: {server.departures}")
    print(f"Tiempo total de la cola vacía: {timeQueueEmpty}")
    print(f"Largo máximo de la cola: {fel.maxLength}")
    print(f"Tiempo total de la cola con largo máximo: {Q_k[fel.maxLength]}")
    print(f"Utilización computada: {1-(timeQueueEmpty/end_time)}")
    print(f"Utilización teórica: {(1/service_rate) / (1 /arrival_rate) }")
    print(f"Largo promedio computado de la cola: {avergeQueueLength}")
    print(f"Largo primedio teorico de la cola: {theoAvgLenght}")
    print(f"Tiempo promedio computado de residencia: {averegaResidenceTime}")   ## failing for now
    print(f"Tiempo promedio teórico de residencia: {1 / (service_rate - arrival_rate) if service_rate > arrival_rate else float('inf')}")

if __name__ == "__main__":
    main()

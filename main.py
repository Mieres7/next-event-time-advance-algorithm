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
    lastEventTime = 0.0
    Q_k = {}
    arrivalTimes = {}
    totalResidenceTime = 0.0
    serviceStartTime = {}

    while server.time < endEvent.arrivalTime:

        currentEvent = fel.popEvent()
        server.time = currentEvent.arrivalTime

        # Computes time where tail was empty before that event
        if fel.length == 0:
            timeQueueEmpty += server.time - lastEventTime

        # Save times at their respective length k 
        if fel.length in Q_k:
            Q_k[fel.length] += server.time - lastEventTime
        else:
            Q_k[fel.length] = server.time - lastEventTime

        if currentEvent.eType == "A":
            server.arrivals += 1
            job_id = server.arrivals
            arrivalTimes[job_id] = server.time

            if not server.busy:
                server.busy = True
                serviceTime = exponentialVariate(service_rate)
                departureTime = server.time + serviceTime
                departure = Event("D", departureTime, serviceTime)
                departure.job_id = job_id
                fel.pushEvent(departure)
                serviceStartTime[job_id] = server.time
            else:
                fel.length += 1
                
            interArrivalTime = exponentialVariate(arrival_rate)
            nextArrivalEvent = Event("A", server.time + interArrivalTime, 0)
            nextArrivalEvent.job_id = job_id
            fel.pushEvent(nextArrivalEvent)

        elif currentEvent.eType == "D":
            server.departures += 1
            job_id = currentEvent.job_id

            # Calculate the residence time
            if job_id in arrivalTimes and job_id in serviceStartTime:
                arrivalTime = arrivalTimes[job_id]
                startServiceTime = serviceStartTime[job_id]
                serviceTime = currentEvent.serviceTime
                
                waitTime = startServiceTime - arrivalTime  # d_i
                residenceTime = waitTime + serviceTime  # w_i = d_i + s_i
                totalResidenceTime += residenceTime

            if fel.length > 0:
                fel.length -= 1
                serviceTime = exponentialVariate(service_rate)
                nextJob_id = server.arrivals - fel.length
                departureEvent = Event("D", server.time + serviceTime, serviceTime)
                departureEvent.job_id = nextJob_id
                fel.pushEvent(departureEvent)
                serviceStartTime[nextJob_id] = server.time
            else:
                server.busy = False

        elif currentEvent.eType == "E":
            break

        lastEventTime = server.time  # updates last event time

    # Compute average tail length
    QT = sum(Q_k.values()) 
    averageQueueLength = sum(k * Q_k[k] for k in Q_k) / QT
    # Compute theorical tail length 
    theoAvgLenght = theoricalAverageLenght(arrival_rate, service_rate)

    # Compute average residence time
    averegaResidenceTime = totalResidenceTime / server.departures if server.departures > 0 else float('inf')

    # Metrics calculation
    print(f"\nNúmero de jobs que llegaron: {server.arrivals}")
    print(f"Número de jobs que salieron: {server.departures}")
    print(f"Tiempo total de la cola vacía: {timeQueueEmpty}")
    print(f"Largo máximo de la cola: {fel.maxLength}")
    print(f"Tiempo total de la cola con largo máximo: {Q_k[fel.maxLength]}")
    print(f"Utilización computada: {1-(timeQueueEmpty/end_time)}")
    print(f"Utilización teórica: {(1/service_rate) / (1 /arrival_rate) }")
    print(f"Largo promedio computado de la cola: {averageQueueLength}")
    print(f"Largo promedio teórico de la cola: {theoAvgLenght}")
    print(f"Tiempo promedio computado de residencia: {averegaResidenceTime}") 
    print(f"Tiempo promedio teórico de residencia: {1 / (service_rate - arrival_rate) if service_rate > arrival_rate else float('inf')}")

if __name__ == "__main__":
    main()

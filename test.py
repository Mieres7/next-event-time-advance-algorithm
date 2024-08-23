import getopt
import sys
import numpy as np
from FEL import FEL
from Event import Event
from Server import Server

def Q_T(Q_k, N):
    return sum(Q_k.get(q, 0) for q in range(N + 1))

def felPromLenght(Q_t, Q_k):
    return sum(k * Q_k.get(k, 0) for k in Q_k) / Q_t

def residencePromTime(S_k, departures):
    return sum(S_k[k] for k in S_k) / departures

def exponentialVariate(rate):
    return -np.log(np.random.uniform()) * 1/ rate

def main():
    np.random.seed(0)

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
    firstArrivalTime = exponentialVariate(arrival_rate)
    firstEvent = Event("A", firstArrivalTime, 0)
    fel.pushEvent(firstEvent)

    endEvent = Event("E", end_time, 0)
    fel.pushEvent(endEvent)

    # Metrics
    lastEventTime = 0
    Q_k = {}
    arrivalTimes = {}
    S_k = {}
    job_id = 0

    while server.time < endEvent.arrivalTime:

        currentEvent = fel.popEvent()
        server.time = currentEvent.arrivalTime

        if fel.lenght in Q_k:
            Q_k[fel.lenght] += server.time - lastEventTime
        else:
            Q_k[fel.lenght] = server.time - lastEventTime

        if currentEvent.eType == "A":
            server.arrivals += 1
            arrivalTimes[job_id] = server.time

            if not server.busy:
                server.busy = True
                serviceTime = exponentialVariate(service_rate)
                departureTime = server.time + serviceTime
                departure = Event("D", departureTime, serviceTime)
                fel.pushEvent(departure)
            else:
                fel.lenght += 1

            interArrivalTime = exponentialVariate(arrival_rate)
            nextArrivalEvent = Event("A", server.time + interArrivalTime, 0)
            nextArrivalEvent.job_id = job_id
            fel.pushEvent(nextArrivalEvent)
            job_id += 1

        elif currentEvent.eType == "D":
            server.departures += 1

            job_id = currentEvent.job_id
            S_k[job_id] = server.time - arrivalTimes[job_id]

            if fel.lenght > 0:
                fel.lenght -= 1
                serviceTime = exponentialVariate(service_rate)
                departureTime = server.time + serviceTime
                departureEvent = Event("D", departureTime, serviceTime)
                fel.pushEvent(departureEvent)
            else: 
                server.busy = False

        lastEventTime = server.time

    Q_t = Q_T(Q_k, fel.maxLength)
    promLenght = felPromLenght(Q_t, Q_k)
    promResidenceTime = residencePromTime(S_k, server.departures)

    print(f"Simulación terminada en el tiempo {server.time}")
    print(f"Número de jobs que llegaron: {server.arrivals}")
    print(f"Número de jobs que salieron: {server.departures}")
    print(f"Tiempo total de la cola vacia: {Q_k[0]}")
    print(f"Largo máximo de la cola: {fel.maxLength}")
    print(f"Tiempo total de la cola con largo máximo: {Q_k.get(fel.maxLength - 1, 0)}")
    print(f"Utilización computada: {1 - Q_k.get(0, 0)/Q_t}")
    print(f"Largo promedio computado de la cola: {promLenght}")
    print(f"Tiempo promedio computado de residencia: {promResidenceTime}")

if __name__ == "__main__":
    main()

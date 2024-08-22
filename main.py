
import getopt
import sys
import numpy as np
from FEL import FEL
from Event import Event
from Server import Server


def Q_T(Q_k, N):
    sum = 0
    for q in range(N+1):
        sum += Q_k.get(q,0)
    return sum

def felPromLenght(Q_t, Q_k):
    sum = 0
    for k in Q_k:
        sum += k * Q_k.get(k,0)
    return 1/Q_t * sum

def residencePromTime(S_k, departures):
    sum = 0
    for k in S_k:
        sum += S_k[k]
    return 1/departures * sum

def exponentialVariate(a):
    u = np.random.uniform()
    return -np.log(1-u)/a

def main():
    np.random.seed(0)

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
    firstArrivalTime = exponentialVariate(arrival_rate)
    firstServiceTime = exponentialVariate(service_rate)
    firstEvent = Event("A", firstArrivalTime, firstServiceTime)
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
            serviceTime = exponentialVariate(arrival_rate)
            nextArrivalEvent = Event("A", server.time + interArrivalTime, serviceTime)
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
            

        elif currentEvent.eType == "E": 
            break
            
    Q_t = Q_T(Q_k, fel.maxLength)
    promLenght = felPromLenght(Q_t, Q_k)
    promResidenceTime = residencePromTime(S_k, server.departures)
                
    print(f"Simulación terminada en el tiempo {server.time}")
   

    print(f"Número de jobs que llegaron: {server.arrivals}")
    print(f"Número de jobs que salieron: {server.departures}")
    print(f"Tiempo total de la cola vacia: {Q_k[0]}")
    print(f"Largo máximo de la cola: {fel.maxLength}")
    print(f"Tiempo total de la cola con largo máximo: {Q_k[fel.maxLength - 1]}")
    print(f"Utilización computada: {1 - Q_k[0]/Q_t}")
    print(f"Utilización teórica: ")
    print(f"Largo promedio computado de la cola: {promLenght}")
    print(f"Largo promedio teórico de la cola: ")
    print(f"Tiempo promedio computado de residencia: {promResidenceTime}")
    print(f"Tiempo promedio teórico de residencia: ")
    

if __name__ == "__main__":
    main()
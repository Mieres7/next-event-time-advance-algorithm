
import heapq

class FEL:
    def __init__(self):
        self.eventList = []
        self.maxLength = 0
        self.emptyTime = 0  # este nose si está bien aqui
        self.lenght = 0

    def pushEvent(self, event):
        self.lenght += 1
        heapq.heappush(self.eventList, event)

    def popEvent(self):
        self.lenght -= 1
        return heapq.heappop(self.eventList)  

    def __repr__(self):
        return str(self.eventList)  
            
        
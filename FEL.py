
import heapq

class FEL:
    def __init__(self):
        self.eventList = []
        self.maxLength = 0
        self.emptyTime = 0  # este nose si está bien aqui

    def pushEvent(self, event):
        heapq.heappush(self.eventList, event)

    def popEvent(self):
        return heapq.heappop(self.eventList)  

    def __repr__(self):
        return str(self.eventList)  
            
        
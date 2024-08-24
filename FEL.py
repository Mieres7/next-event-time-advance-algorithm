import heapq

class FEL:
    def __init__(self):
        self.eventList = []
        self.maxLength = 0
        self.length = 0  # initialize in 0 even when the end event is in it

    def pushEvent(self, event):
        # self.length += 1
        heapq.heappush(self.eventList, event)
        if self.length > self.maxLength: self.maxLength = self.length
            

    def popEvent(self):
        # self.length -= 1
        return heapq.heappop(self.eventList)

    def __repr__(self): 
        return str(self.eventList.arrivalTime)  
            
        
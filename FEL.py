
import heapq

class FEL:
    def __init__(self):
        self.eventList = []
        self.maxLength = 0
        self.lenght = 0 # initialize in 0 even when the end event is in it

    def pushEvent(self, event):
        self.lenght += 1
        heapq.heappush(self.eventList, event)
        # self.eventList.insert(len(self.eventList),event)
        # self.eventList.sort()
        if self.lenght > self.maxLength: self.maxLength = self.lenght
            

    def popEvent(self):
        self.lenght -= 1
        return heapq.heappop(self.eventList)
        # return self.eventList.pop()  

    def __repr__(self): 
        return str(self.eventList.arrivalTime)  
            
        
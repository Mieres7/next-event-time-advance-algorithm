class Event:
    def __init__(self, eType, arrivalTime):
        self.arrivalTime = arrivalTime
        self.eType = eType
        self.serviceTime = 0
   
    def __lt__(self, other):
        return self.arrivalTime < other.arrivalTime
   
    def __repr__(self):
        return f'Event(Arrival Time={self.arrivalTime}, Event Type="{self.eType}")'
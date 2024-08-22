class Event:
    def __init__(self, eType, arrivalTime, serviceTime):
        self.arrivalTime = arrivalTime
        self.eType = eType
        self.job_id = 0
        self.serviceTime = serviceTime  
   
    def __lt__(self, other):
        return self.arrivalTime < other.arrivalTime
   
    def __repr__(self):
        return f'Event(Arrival Time={self.arrivalTime}, Event Type="{self.eType}")'
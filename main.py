import argparse
import numpy

# Global variables
fel = []
arrivedJobs = 0
departuredJobs = 0
serverBusy = 0

def exponentialVariate(a):
    u = numpy.random.uniform(low=0.0, high=1.0)
    return -(1/a)*numpy.log(1-u)

def arrival(): 
    return 2


def main(): 
    parser = argparse.ArgumentParser(description="Initial values")
    parser.add_argument('-a', type= int, required=True, help="Arrival rate")
    parser.add_argument('-d', type= int, required=True, help="Service rate")
    parser.add_argument('-t', type= int, required=True, help="End time")

    args = parser.parse_args()  # args.a/d/t para acceder a los valores

    print(exponentialVariate(3))

    
    





    


if __name__ == "__main__":
    main()
from time import sleep as wait
from random import randrange

class Elevator:

    def __init__(self,carname,minflr,maxflr,currentfloor=1,speed=1,doortime=3,lights=False):      
        self.current_floor = int(currentfloor)
        self.car_name = str(carname)
        self.minimum_floor = int(minflr)
        self.maximum_floor = int(maxflr)
        self.car_speed = speed
        self.direction = 1 # 0 = down; 1 = idle; 2 = up
        self.door_timer = doortime
        self.moving = False
        self.total_floors = self.maximum_floor - self.minimum_floor
        self.lights_enabled = lights
        self.queue = []

    def __str__(self):
        return "Elevator {} on floor {}".format(self.car_name, self.current_floor)

    def __repr__(self):
        return "<Elevator object {} currently on floor {}>".format(self.car_name, self.current_floor)

    def print_(self,st):
        print("CAR {}: {}".format(self.car_name,st))

    def add_call(self,floor,dire):
        if not floor > self.maximum_floor and not floor < self.minimum_floor:
            self.queue.append((floor,dire))
            # 0 = down; 1 = idle; 2 = up
            if not self.moving:
                self.check_calls()   
        else:
            raise Exception("Desired floor ({}) is higher/lower than the maximum/minimum ({}/{})".format(floor,self.maximum_floor,self.minimum_floor))

    def check_calls(self):
        self.print_("queue: {}".format(self.queue))
        options = []
        # i[0] = floor, i[1] = dir, i[2] = distancetofloor
        for i in self.queue: 
            if (i[0] > self.current_floor and ((self.direction == 0 or self.direction == 1) and i[1] == 1 or i[1] == 0)) or (i[0] == self.current_floor):
                options.append((i[0],i[1],i[0]-self.current_floor))
            elif (i[0] < self.current_floor and ((self.direction == 0 or self.direction == -1) and i[1] == -1 or i[1] == 0)) or (i[0] == self.current_floor):
                options.append((i[0],i[1],self.current_floor-i[0]))
        if len(options) != 0:
            lowestdist = 999999999999999
            best = []
            for i in options:
                if i[0] == self.current_floor and self.direction == 0:
                    self.run(i[0],i[1])
                elif i[2] < lowestdist:
                    lowestdist = i[2]
                    best = i       
            self.queue.remove((best[0],best[1]))
            self.run(best[0],best[1])      
        elif len(options) == 0 and len(self.queue) != 0:
            newoptions = []
            for i in self.queue:
                if i[0] > self.current_floor:
                    newoptions.append((i[0],i[1],i[0]-self.current_floor))               
                elif i[0] < self.current_floor:
                    newoptions.append((i[0],i[1],self.current_floor-i[0]))
            lowestdist = 99999999999999999
            best = []
            for i in newoptions:
                if i[0] == self.current_floor and self.direction == 0:
                    self.run(i[0],i[1]) 
                elif i[2] < lowestdist:
                    lowestdist = i[2]
                    best = i          
            if best:
                self.queue.remove((best[0],best[1]))
                self.run(best[0],best[1])

    def run_doors(self):
        wait(.5)
        self.print_("doors open @ floor {}".format(self.current_floor))
        wait(self.door_timer)
        self.print_("doors closed @ floor {}".format(self.current_floor))
        wait(.5)

    def run(self,floor,dir):
        if not self.moving:
            if floor == self.current_floor:
                self.print_("arrived @ floor {}".format(self.current_floor))
                self.run_doors()
                self.check_calls()
            else:
                if floor > self.current_floor:
                    self.direction = 1
                elif floor < self.current_floor:
                    self.direction = -1
                self.print_("running to floor {} in direction {}".format(floor,self.direction))
                self.moving = True
                for _ in (range(self.current_floor,floor,1)) if floor > self.current_floor else range(self.current_floor,floor,-1):              
                    wait(self.car_speed)
                    self.current_floor += self.direction
                    self.print_("@ floor {}".format(self.current_floor))
                wait(.5)
                self.print_("arrived @ floor {}".format(self.current_floor))
                self.run_doors()
                self.moving = False
                self.check_calls()
            

class Human:

    def __init__(self,id):
        self.name = str(id)         
        self.elev = elevators[randrange(0,len(elevators),1)]
        self.start = randrange(self.elev.minimum_floor,self.elev.maximum_floor,1)
        self.goal = randrange(self.elev.minimum_floor,self.elev.maximum_floor,1)
        #print("{}: Created with start floor of {} and a goal floor of {}".format(self.name,self.start,self.goal))
        self.run()

    async def run(self):
        if self.start > self.goal:
            self.elev.add_call(self.start,-1)
        elif self.start < self.goal:
            self.elev.add_call(self.start,1)
        self.elev.add_call(self.goal,0)

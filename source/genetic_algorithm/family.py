from transit_network.trips import SimpleTrip

class Family:
    def __init__(self, child_A: SimpleTrip, child_B: SimpleTrip, parent_A: SimpleTrip, parent_B: SimpleTrip):
        self.child_A = child_A 
        self.child_B = child_B

        self.parent_A = parent_A 
        self.parent_B = parent_B

    @property
    def children(self):
        return [self.child_A, self.child_B]
    
    @property
    def parents(self):
        return [self.parent_A, self.parent_B]
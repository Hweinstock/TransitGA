
class Chromosome:

    def __init__(self, obj: object, parent_A_id: str = None, parent_B_id: str = None):
        self.obj = obj 
        self.original_id = obj.id

        self.parent_A_id = parent_A_id 
        self.parent_B_id = parent_B_id 
        self.unique_id = None # This value changes based on iteration. 
        self.num_times_parent = 0
        self.FitnessObj = None 

    def get_family_history(self):
        # Removed for performance reasons. 
        return ''
        # if self.parent_A_id is None or self.parent_B_id is None:
        #     return self.original_id 
        # else:
        #     return f"({self.parent_A_id}):({self.parent_B_id})"
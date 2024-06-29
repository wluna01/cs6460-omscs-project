'''
Defines the story class that will hold the story data and manage the story's state.
'''

#defines story class
class Story:
    def __init__(self):
        self.num_segments_displayed = 0
        self.total_number_of_segments = 0
        self.segments = []

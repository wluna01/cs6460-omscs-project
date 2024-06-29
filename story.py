'''
Defines the story class that will hold the story data and manage the story's state.
'''
from helper_functions import get_data, get_credentials
#defines story class
class Story:
    def __init__(self):
        self.segments = get_data("select * from educational_technology.stories.la_tortuga_gigante limit 10")
        self.num_segments_displayed = 1
        self.total_number_of_segments = len(self.segments)

import datetime
import time

class Repetition(object):
    repetition_timestamp = None

class RepeatableItem(object):

    next_repetition_timestamp = None
    repetitions = []
    
    def get_priority(self, repetition_time=None):
        if repetition_time is None:
            repetition_time = time.time()

        # non-scheduled items have no priority
        if self.next_repetition_timestamp is None:
            return None
        
        time_delta = repetition_time - self.next_repetition_timestamp
        # before the scheduled repetition date, the item will have no priority (None)
        if time_delta < 0:
            return None
        
        # if no repetitions made yet, the item will have priority 10
        if len(self.repetitions) == 0:
            return 1.0

        if len(self.repetitions) == 1:
            return 10

        # if the item has no age, the item will have priority 0
        age = self.get_age()
        if age == 0:
            return 0
        
        waiting = time_delta / float(86400)
        
        priority = float(1.0 / age * 86400 + 1.0 / len(self.repetitions)) + waiting * 86400
        return priority

    def get_age(self):
        if len(self.repetitions) == 0:
            return None
        elif len(self.repetitions) == 1:
            last_repetition_timestamp = time.time()
        else:
            last_repetition_timestamp = self.repetitions[-1].repetition_timestamp
        age = last_repetition_timestamp - self.repetitions[0].repetition_timestamp
        return age
            

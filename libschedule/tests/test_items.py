import libschedule
import time
import datetime

class TestRepeatableItem(object):

    def test_priority_simple(self):
        
        # non-scheduled item has no priority
        ri = libschedule.RepeatableItem()
        assert ri.get_priority() is None

        # a scheduled item with no repetitions has priority 1.0
        ri.next_repetition_timestamp = time.time()
        assert ri.get_priority() == 100

        # a scheduled item with one repetition has priority 10.0
        repetition = libschedule.Repetition()
        repetition.repetition_timestamp = time.time() - 86400 * 3
        ri.repetitions.append(repetition)
        assert ri.get_priority() == 75

        # an item with two repetitions (3 and 1 days ago) will have a priority of ca 1.0
        repetition = libschedule.Repetition()
        repetition.repetition_timestamp = time.time() - 86400
        ri.repetitions.append(repetition)
        assert 14.95 < ri.get_priority() < 15.05

    def create_item(self, age, reps, wait):
        ri = libschedule.RepeatableItem()
        now = time.time()
        last_due = now - wait * 86400
        ri.next_repetition_timestamp = last_due

        from_time = last_due - age * 86400
        first_rep = libschedule.Repetition()
        first_rep.repetition_timestamp = from_time
        ri.repetitions.append(first_rep)

        if reps > 2:
            for rep in range(reps-2):
                r = libschedule.Repetition()
                ri.repetitions.append(r)

        if reps > 1:
            last_rep = libschedule.Repetition()
            last_rep.repetition_timestamp = last_due
            ri.repetitions.append(last_rep)
            
        return ri

    def test_priority_complex(self):
        #           Age, Reps, Wait, Priority
        matrix = [
                    (3,  1,    1,    75),
                    (3,  2,    2,    82),
                    (3,  3,    2,    76),
                    (5,  2,    1,    35),
                    (5,  2,    2,    55),
                    (5,  2,    3,    75),
                    (12,  3,    20,  175),
                    (1000,  35, 100, 11),

                 ]
        print "Age\tReps\tWait\tPrio"
        for item in matrix:
            current_item = self.create_item(item[0], item[1], item[2])
            actual_priority = current_item.get_priority()
            expected_priority = item[3]
            allowed_inaccuracy = 0.02
            lower_bound = expected_priority - expected_priority * allowed_inaccuracy
            upper_bound = expected_priority + expected_priority * allowed_inaccuracy

            print "%d\t%d\t%d\t%.2f" % (item[0], item[1], item[2], actual_priority)
            #print "%.2f\t%.2f\t%.2f" % (lower_bound, actual_priority, upper_bound)
            assert lower_bound <= actual_priority <= upper_bound
            

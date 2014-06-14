import libschedule
import time


class TestRepeatableItem(object):
    def test_age(self):
        
        # non-scheduled item has no priority
        ri = libschedule.RepeatableItem()
        assert ri.get_priority() is None

        # a scheduled item with no repetitions has priority 1.0
        ri.next_repetition_timestamp = time.time()
        assert ri.get_priority() == 1.0

        # a scheduled item with one repetition has priority 10.0
        repetition = libschedule.Repetition()
        repetition.repetition_timestamp = time.time() - 86400 * 3
        ri.repetitions.append(repetition)

        assert ri.get_priority() == 10.0

        repetition = libschedule.Repetition()
        repetition.repetition_timestamp = time.time() - 86400
        ri.repetitions.append(repetition)

        print ri.get_priority()
        assert 0.99 < ri.get_priority() < 1.01

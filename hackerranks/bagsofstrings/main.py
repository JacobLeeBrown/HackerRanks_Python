import logging as lg
import random
import time
import bags_of_strings

lg.basicConfig(
    format='%(asctime)s - %(name)10s - %(levelname)7s - %(message)s', level=lg.DEBUG
)


def small_demo():
    lg.debug("### Small Demo")

    demo_bags = [
        ["aaa", "abc", "def", "bbb", "1234"],
        ["hello", "world", "HeLlO", "wOrLd", "Hello World!"],
        ["hello", "there", "!", "General", "Kenobi"],
        ["apple", "banana", "cucumber", "death star", "ewok"],
        ["foo", "bar", "1234", "deadbeef", "rotflol"]
    ]

    lg.debug("~~~ Demo Bags ~~~")
    _log_bags(demo_bags)
    lg.debug("")

    # Demo low false positive rate -> Slower, but more accurate
    target = "hello"
    fp_prob = 0.1
    bloom_filters = bags_of_strings.get_bloom_filters_for_bags(demo_bags, fp_prob)
    potential_bags = bags_of_strings.get_bags_that_might_contain(demo_bags, bloom_filters, target)

    lg.debug("~~~ Potential Bags: target={}, fp_prob={} ~~~".format(target, fp_prob))
    _log_bags(potential_bags)
    lg.debug("")

    target = "1234"
    fp_prob = 0.1
    bloom_filters = bags_of_strings.get_bloom_filters_for_bags(demo_bags, fp_prob)
    potential_bags = bags_of_strings.get_bags_that_might_contain(demo_bags, bloom_filters, target)

    lg.debug("~~~ Potential Bags: target={}, fp_prob={} ~~~".format(target, fp_prob))
    _log_bags(potential_bags)
    lg.debug("")

    # Demo high false positive rate -> Faster, but less accurate
    target = "hello"
    fp_prob = 0.5
    bloom_filters = bags_of_strings.get_bloom_filters_for_bags(demo_bags, fp_prob)
    potential_bags = bags_of_strings.get_bags_that_might_contain(demo_bags, bloom_filters, target)

    lg.debug("~~~ Potential Bags: target={}, fp_prob={} ~~~".format(target, fp_prob))
    _log_bags(potential_bags)
    lg.debug("")

    lg.debug("### End Small Demo")
    lg.debug("")


def large_demo():
    lg.debug("### Large Demo")
    start_time = _current_time_ms()

    demo_bags = bags_of_strings.generate_random_bags()
    lg.debug("demo_bags_count={}, time_taken={} ms".format(
        len(demo_bags), _current_time_ms() - start_time))

    # Get random target we know exists in at least 1 bag
    rand_bag = demo_bags[random.randrange(len(demo_bags))]
    rand_target = rand_bag[random.randrange(len(rand_bag))]

    # Demo the effect of fp_prob on accuracy and time
    for i in [0.50, 0.25, 0.2, 0.1, 0.05]:
        _large_demo(demo_bags, i, rand_target)
    lg.debug("Total time_taken={} ms".format(_current_time_ms() - start_time))

    lg.debug("### End Large Demo")


def _large_demo(demo_bags, fp_prob, target):
    start_time = _current_time_ms()
    bloom_filters = bags_of_strings.get_bloom_filters_for_bags(demo_bags, fp_prob)
    potential_bags = bags_of_strings.get_bags_that_might_contain(demo_bags, bloom_filters, target)
    lg.debug("~~~ target={}, fp_prob={}, potential_bag_count={}, time_taken={} ms ~~~".format(
        target, fp_prob, len(potential_bags), _current_time_ms() - start_time))


def _log_bags(bags):
    for bag in bags:
        lg.debug("{}".format(str(bag)))


def _current_time_ms():
    return round(time.time() * 1000)


if __name__ == "__main__":
    # Demo bags of strings interface
    small_demo()
    for _ in range(3):
        large_demo()

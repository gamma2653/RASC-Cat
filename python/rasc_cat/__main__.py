import argparse

from rasc_cat import config, scheduler

parser = argparse.ArgumentParser()

parser.add_argument('-m', '--modules', nargs='+', default=config.DEFAULT_MODULES)
parser.add_argument('-c', '--chaos', action='store', type=float, default=config.DEFAULT_CHAOS)

args, unknown_args = parser.parse_known_args()

system = scheduler.System()




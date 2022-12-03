import argparse

from rasc_cat import config

parser = argparse.ArgumentParser()

parser.add_argument('-c', '--chaos', type=float, default=config.PERSONALITY['chaos'])
parser.add_argument('-d', '--debug', action='store_true', type=bool, default=False)
parser.add_argument('-mods', '--modules', nargs='+', action='extend', type=str)

args, unknowns = parser.parse_known_args()

# TODO: pass along to submodules?
print(f'Ignoring args: {unknowns}')

print(f'chaos={args.chaos}\nmods={args.modules}')
import argparse
from cowsay import cowsay, list_cows

parser = argparse.ArgumentParser()

parser.add_argument('message', type=str)
parser.add_argument('-e', default='oo', type=str)
parser.add_argument('-f', default='default', type=str)
parser.add_argument('-l', action='store_true')
parser.add_argument('-n', action='store_true')
parser.add_argument('-T', default='  ', type=str)
parser.add_argument('-W', default=40, type=int)

parser.add_argument('-b', action='store_true')
parser.add_argument('-d', action='store_true')
parser.add_argument('-g', action='store_true')
parser.add_argument('-p', action='store_true')
parser.add_argument('-s', action='store_true')
parser.add_argument('-t', action='store_true')
parser.add_argument('-w', action='store_true')
parser.add_argument('-y', action='store_true')

args = parser.parse_args()

if args.l:
    print(list_cows())
else:
    preset = [p for p in "bdgpstwy" if args.__dict__[p]]
    print(
        cowsay(
            message=args.message,
            cow=args.f,
            preset=preset[0] if preset else None,
            eyes=args.e,
            tongue=args.T,
            width=args.W,
            wrap_text=args.n,
        )
    )

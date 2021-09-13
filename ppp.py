import sys
import os.path

err = False
paths = []

# check arguments
argc = len(sys.argv)
if argc < 3:
    print_usage()
    sys.exit(1)

# figure out src dir from root argument
sep="/"
src_dir = sep.join(sys.argv[1].split(sep)[:-1])

def print_usage():
    print("\nusage: python ppp.py ROOT TEMPLATES [...]")

def preprocess_file(path):
    lines=0

    with open(path) as f:
        content = f.readlines()
        content = [x.strip() for x in content]
        lines=len(content)

        for l in content:

            if l.startswith("#include"):
                include_path = l.split(" ")[1]

                # prepend directory
                include_path = "/".join([src_dir, include_path])

                preprocess_file(include_path)
                continue

            print(l)


for i in range(1,argc):
    path = sys.argv[i]

    if not os.path.isfile(path):

        print(path + " is not a file")
        err = True
        continue

    if path in paths:
        # ignore duplicates
        continue

    paths.append(path)

if err:
    print_usage()
    sys.exit(1)

preprocess_file(sys.argv[1])

sys.exit(0)

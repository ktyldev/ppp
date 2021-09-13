import sys
import os.path
import re

err = False
paths = []

# check arguments
argc = len(sys.argv)
if argc < 3:
    print_usage()
    sys.exit(1)

# figure out src dir from root argument
sep="/"
src_dir = sep.join(sys.argv[2].split(sep)[:-1])

# regex patterns
p_var = re.compile(r'(#.+?\.css)')

def print_usage():
    print("\nusage: python ppp.py ROOT TEMPLATES [...]")

def preprocess_file(path):
    lines=0

    with open(path) as f:
        content = f.readlines()
        content = [x.strip() for x in content]
        lines=len(content)

        for l in content:

            # replace lines that start with #include with the contents of a file
            if l.startswith("#include"):
                include_path = l.split(" ")[1]

                # prepend directory
                include_path = "/".join([src_dir, include_path])

                preprocess_file(include_path)
                continue

            # inline replace any occurrence of #filename with the contents of that file
            match = re.search(p_var, l)
            if match:
                path = "/".join([src_dir, match.group(0)[1:]])

                with open(path) as var_file:
                    var_content = var_file.read().strip()
                    l = re.sub(p_var, var_content, l)

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

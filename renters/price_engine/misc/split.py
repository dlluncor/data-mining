import json
from collections import OrderedDict

def split_file(path, filename, outputname, filecount, ext="dat"):
    with open("%s/%s" % (path, filename), 'rb') as reader:
        lines = reader.readlines()

        samples = [json.dumps(OrderedDict([('id', idx), ('data', item.strip())])) for idx, item in enumerate(lines)]
        # Drop the header
        samples = samples[1:]
        for i in range(0, filecount):
            items = samples[i::filecount]
            with open("%s/%s_%s.%s" % (path, outputname, i, ext), 'w') as writer:
                for item in items:
                    writer.write(item + "\n")

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input", help="input file")
    parser.add_argument("-o", "--output", help="outputname")
    parser.add_argument("-c", "--count", help="file count")
    parser.add_argument("-p", "--path", help="file path")
    parser.add_argument("-e", "--ext", help="file extention")
    args = parser.parse_args()

    split_file(args.path, args.input, args.output, int(args.count))

import sys
import simplejson

if __name__ == "__main__":
    count = 0
    with open("wikipedia_text_files.json", "r") as original:
        data = simplejson.load(original)

    with open("wikipedia_data_lines.json", "w") as output:
        for entry in data:
            simplejson.dump(entry, output)
            output.write('\n')
            sys.stdout.write(f"Entries written: {count} \r")
            sys.stdout.flush()
            count += 1

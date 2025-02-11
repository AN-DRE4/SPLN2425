def main(input_file, output_file=None, keep_whitespace=False):
    final = []
    finalDict = {}
    with open(input_file, 'r', encoding='utf-8') as file:
        text = []
        for line in file:
            try:
                text.append(line.encode('utf-8').decode('utf-8'))
            except UnicodeError:
                continue
    for line in text:
        line_key = line if keep_whitespace else line.strip()
        if line_key not in finalDict:
            final.append(line_key)
            finalDict[line_key] = 0
        else:
            finalDict[line_key] += 1

    if output_file:
        with open(output_file, 'w') as f:
            for item in final:
                f.write(f"{item}\n")
    else:
        for item in final:
            print(item)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', help='Input file path')
    parser.add_argument('output_file', nargs='?', help='Output file path')
    parser.add_argument('--keep-whitespace', '-w', action='store_true', 
                      help='Keep trailing whitespaces')
    
    args = parser.parse_args()
    main(args.input_file, args.output_file, args.keep_whitespace)

# Function to parse input and output
def parse_example(example):
    input_start = example.find("Input") + 5
    output_start = example.find("Output") + 6
    comment = example.find("#") + 1
    if comment == 0:
        comment = "None"
    else:
        comment = example[comment:example.find("Input")-1].strip()
    input_text = example[input_start:output_start-6].strip()
    output_text = example[output_start:].strip()
    return (input_text, output_text, comment)

# Usage:
# 1. Split the text by examples
#    examples = text.strip().split('Example ')[1:]
# 2. Create tuples for each example
#    tuples = [parse_example(example) for example in examples]
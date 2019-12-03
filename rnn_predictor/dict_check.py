from spellchecker import SpellChecker
import sys
import ast
import logging
import string

# Args
if len(sys.argv) < 2:
    print("Please select a dataset.")
    print("Usage: python dict_check.py <dataset> [LOG_LEVEL]")
    print("Available datasets: dylan, spinetta, drexler")
    print("Log level ERROR by default")
    exit(1)
else:
    dataset = sys.argv[1]
    log_level = sys.argv[2] if len(sys.argv) > 2 else 'ERROR'

log_levels = {'DEBUG': logging.DEBUG, 'INFO': logging.INFO, 'WARNING': logging.WARNING, 'ERROR': logging.ERROR}

logging.basicConfig(level=log_levels[log_level])
# I/O
data_dir = "./data/" + dataset
input_file = data_dir + "/input.txt" if dataset != 'drexler' else data_dir + "/input_bkp.txt"
output_file = data_dir + "/output.txt"
corrected_file = data_dir + '/output_checked.txt'
with open(data_dir + "/smooth_losses.txt") as f:
    smooth_loses = ast.literal_eval(f.read())

# turn off loading a built language dictionary, case sensitive on (if desired)
sp = SpellChecker(language='es', case_sensitive=False)
sp.word_frequency.load_text_file(input_file)

with open(output_file) as input:
    with open(corrected_file, 'w') as output:
        input_lines = input.readlines()
        input_lines = input_lines[input_lines.index('Iteration: 100000\n'):]
        total_lines = len(input_lines)
        for i, a_line in enumerate(input_lines):
            if not a_line.startswith('Iteration') and a_line != '\n':
                #do magic
                words = a_line.split()
                for a_word in words:
                    a_word = a_word.translate(str.maketrans('', '', string.punctuation))
                    if a_word not in sp:
                        correction = sp.correction(a_word)
                        a_line = a_line.replace(a_word, correction)
                        logging.debug(f"Corrected {a_word} for {correction}")
            output.write(a_line)
            print(f"Wrote {i + 1}/{total_lines} lines...")
print("Done!")
import numpy as np

# get lines
with open('input.txt', 'r') as f:
    lines = f.readlines()

# calculate mean length for song
lengths = []
a_length = 0
previous_new_line = False
for a_line in lines:
    if a_line != '\n':
        a_length += 1
    elif not previous_new_line:
        previous_new_line = True
    else:
        lengths.append(a_length)
        a_length = 0
        previous_new_line = False
mean_lines = np.mean(lengths)
std_lines = np.std(lengths)

#trim newlines and write mock data.
lines = [x for x in lines if x != '\n']
MOCK_SONGS = 900
with open('input.txt', 'a') as f:
    for _ in range(MOCK_SONGS):
        song_size = int(np.abs(np.random.normal(mean_lines, std_lines, 1)))
        for _ in range(song_size):
            f.write(np.random.choice(lines))
        f.write('\n\n')

print("")
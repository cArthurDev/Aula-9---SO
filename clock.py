import random

SWAP_ROWS = 100
RAM_ROWS = 10
INSTRUCTIONS = 1000

random.seed()

swap = []
for i in range(SWAP_ROWS):
    swap.append([i, i + 1, random.randint(1, 50), 0, 0, random.randint(100, 9999)])

ram = []
for _ in range(RAM_ROWS):
    idx = random.randint(0, SWAP_ROWS - 1)
    row = swap[idx]
    ram.append([row[0], row[1], row[2], row[3], row[4], row[5]])


def print_matrix(title, mat):
    print(title)
    print('N\tI\tD\tR\tM\tT')
    for r in mat:
        print('{}\t{}\t{}\t{}\t{}\t{}'.format(r[0], r[1], r[2], r[3], r[4], r[5]))
    print()


def save_to_swap(page):
    n = page[0]
    swap[n][0] = page[0]
    swap[n][1] = page[1]
    swap[n][2] = page[2]
    swap[n][3] = 0
    swap[n][4] = 0
    swap[n][5] = page[5]


def find_swap_by_I(i_value):
    for s in swap:
        if s[1] == i_value:
            return s
    return None


hand = 0
page_faults = 0
writes_to_swap = 0


def clock_replace(requested_I):
    global hand, page_faults, writes_to_swap
    page_faults += 1
    n = RAM_ROWS

    while True:
        frame = ram[hand]
        if frame[3] == 0:
            if frame[4] == 1:
                save_to_swap(frame)
                writes_to_swap += 1
            swap_row = find_swap_by_I(requested_I)
            if swap_row:
                ram[hand][0] = swap_row[0]
                ram[hand][1] = swap_row[1]
                ram[hand][2] = swap_row[2]
                ram[hand][3] = 1
                ram[hand][4] = 0
                ram[hand][5] = swap_row[5]
                if random.random() < 0.5:
                    ram[hand][2] += 1
                    ram[hand][4] = 1
            else:
                ram[hand] = [requested_I - 1, requested_I, random.randint(1, 50), 1, 0, random.randint(100, 9999)]
            hand = (hand + 1) % n
            return
        else:
            ram[hand][3] = 0
            hand = (hand + 1) % n

print_matrix('MATRIZ SWAP - INICIAL', swap)
print_matrix('MATRIZ RAM - INICIAL', ram)

for instr_count in range(1, INSTRUCTIONS + 1):
    req_I = random.randint(1, 100)
    hit = False
    for j in range(RAM_ROWS):
        if ram[j][1] == req_I:
            hit = True
            ram[j][3] = 1

            if random.random() < 0.5:
                ram[j][2] += 1
                ram[j][4] = 1
            break
    if not hit:
        clock_replace(req_I)

    if instr_count % 10 == 0:
        for j in range(RAM_ROWS):
            ram[j][3] = 0

print_matrix('MATRIZ SWAP - FINAL', swap)
print_matrix('MATRIZ RAM - FINAL', ram)

print('Page faults:', page_faults)
print('Writes to swap:', writes_to_swap)

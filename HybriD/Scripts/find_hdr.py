import numpy as np

WINDOW = 40


def find_hdr():
    with open("in/depth") as file:
        s = [i.split() for i in file.readlines()]
        s.remove([])
    s3 = [int(i[2]) for i in s]
    arr = np.array([np.array(s3[i-WINDOW:i]).mean() for i in range(WINDOW, len(s3), WINDOW)])
    last = arr[0]
    for x, i in enumerate(arr):
        if last + last/2 < i:
            print(f"{x}: {i} {last}")
        last = i
    print("done")


if __name__ == "__main__":
    find_hdr()

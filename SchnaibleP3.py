# Kyler Schnaible Project 3 11/29/2021

from PIL import Image
import numpy as np
import queue


def checkBounds(vertex, size):
    if(vertex[0] > size[0]-1 or vertex[1] > size[1]-1 or vertex[0] < 0 or vertex[1] < 0):
        return False
    return True


def saveImage(image):
    # Image.fromarray(image,mode="RGB").save('out.bmp')
    a = np.array(image)
    im = Image.fromarray(a)
    filename = input("Please enter an image name to output as BMP: ")
    filename = filename+".bmp"
    im.save(filename)
    # plt.imshow(im)
    # plt.show()


def BreadthFirstSearch(I, s, t):
    # (Image: I, Vertices: s, t)
    # s is the start vertex, t is the destination
    print('Starting BreadthFirstSearch')
    newImg = I
    Q = queue.Queue()  # Initialize a queue Q;
    Q.put(s)
    # Set visited[v] = false all vertices;
    visited = np.zeros((I.shape[0], I.shape[1]))
    visited[s[0], s[1]] = 1
    prev = np.empty((I.shape[0], I.shape[1]), dtype=type(s))
    # Set array d to all -1 to represent infinity
    d = np.negative(np.ones((I.shape[0], I.shape[1])))
    d[s] = 0
    visited[s] = 1

    while not Q.empty() and visited[t] != 1:
        # print(visited)
        u = Q.get()                      # what is u?
        # print('u:', u)
        # for each neighbor v of u:
        for v in [(u[0]+1, u[1]), (u[0]-1, u[1]), (u[0], u[1]+1), (u[0], u[1]-1)]:
            if checkBounds(v, d.shape):
                if visited[v] == 0 and (I[v][0] > 100 or I[v][1] > 100 or I[v][2] > 100):
                    visited[v] = 1
                    newImg[v] = [0, 255, 0]     # set color of v to Green
                    d[v] = d[u] + 1
                    prev[v] = u
                    Q.put(v)
            else:
                continue

    prev[t[0], t[1]] = u

    v = t
    while (v != s):
        newImg[v] = [255, 0, 0]  # set color of v to Red
        v = prev[v]

    print('Saving Image For BreadthFirstSearch')
    saveImage(newImg)
    print('Distance for BreadthFirstSearch: ', d[t])
    return


def hFunc(index, t):
    # h[u] is an estimate of the distance from u to the goal node
    h = abs(index[0]-t[0]) + abs(index[1]-t[1])
    return (h)


def BestFirstSearch(I, s, t):
    # s is the start vertex, t is the destination
    # h is a function as described above
    print('Starting BestFirstSearch')
    newImg = I
    Q = queue.PriorityQueue()  # Initialize a queue Q;
    Q.put((1, s))
    # Set visited[v] = false all vertices;
    visited = np.zeros((I.shape[0], I.shape[1]))
    visited[s[0], s[1]] = 1
    prev = np.zeros((I.shape[0], I.shape[1]), dtype=type((0, 0)))

    # set d[s] = h[s] and d[u] = MaxInt for all other u.
    # Set array d to all -1 to represent infinity
    d = np.negative(np.ones((I.shape[0], I.shape[1])))
    d[s] = 0

    # print(prev)
    while not Q.empty() and visited[t] != 1:
        # How is deletemin different from delete? Does Q.get() work when using queue.PriorityQueue()
        u = Q.get()
        # for each neighbor v of u:
        for v in [(u[1][0]+1, u[1][1]), (u[1][0]-1, u[1][1]), (u[1][0], u[1][1]+1), (u[1][0], u[1][1]-1)]:
            if checkBounds(v, d.shape):
                if visited[v[0], v[1]] == 0 and (I[v][0] > 100 or I[v][1] > 100 or I[v][2] > 100):
                    visited[v[0], v[1]] = 1
                    # set color of v to Green
                    newImg[v[0], v[1]] = [0, 255, 0]
                    d[v[0], v[1]] = d[u[1][0], u[1][1]] + 1
                    prev[v] = u[1]
                    h = hFunc(v, t)
                    Q.put((d[v] + h, v))  # What are we inserting here?

    prev[t] = u[1]

    v = t
    while (v != s):
        newImg[v] = [255, 0, 0]  # set color of v to Red
        v = prev[v]

    # create an output image with new pixel values
    # output d[t]
    print('Saving Image For BestFirstSearch')
    saveImage(newImg)
    print('Distance for BestFirstSearch: ', d[t])
    return


def main():
    filename = input("Please enter an image (BMP or JPG): ")
    fileImage = Image.open(filename)
    img = np.array(fileImage.convert('RGB'))

    start = input(
        "Please enter the starting pixel, seperated by comma, as row,column: ").split(',')
    finish = input(
        "Please enter the terminating pixel, seperated by comma, as row,column: ").split(',')

    start = (int(start[0]), int(start[1]))
    finish = (int(finish[0]), int(finish[1]))

    BreadthFirstSearch(img, start, finish)
    BestFirstSearch(img, start, finish)
    return


main()

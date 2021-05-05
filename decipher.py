import sys

# Class for point representation
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # Check if points are the same
    def equals(self, q):
        if self.x == q.x and self.y == q.y:
            return True
        else:
            return False

# Get inverse of number 'j'
# Extended euclidian algorithm
def inverse(j, fp):
    u0, u1 = 0, 1
    s0, s1 = fp, j
    while s0 != 0:
        q = s1 // s0
        s1, s0 = s0, s1 - q * s0
        u1, u0 = u0, u1 - q * u0
    return u1


# Add 2 points together R = P + Q
# If point is None, it's point in infinite
def add(p, q, fp, a):
    # Laws of of elliptic curve
    if p is None:
        return q
    if q is None:
        return p
    if p.equals(q):
        return double(p, q, fp, a)
    if p.x - q.x == 0 and p.y - q.y == 0:
        return None
    
    s = ((q.y - p.y) * inverse(q.x - p.x, fp)) % fp
    x = (s * s - p.x - q.x) % fp
    y = (s * (p.x - x) - p.y) % fp

    return Point(x, y)


# Double point R = P + P
def double(p, q, fp, a):
    if not p.equals(q):
        return add(p, q)

    s = ((3 * (p.x * p.x) + a) * inverse(2 * p.y, fp)) % fp
    x = (s * s - 2 * p.x) % fp
    y = (s * (p.x - x) - p.y) % fp

    return Point(x, y)


def decipher():

    # Values for ECC
    # Given from project task
    fp = 0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff
    a = -0x3
    b = 0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b
    g_x = 0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296
    g_y = 0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5
    g = Point(g_x, g_y)
    
    # Parse input
    in_string = sys.argv[1]
    in_list = in_string.split(',')
    # Input in project task is formated as:
    #   make decipher publicKey="(0x477...3e, 0xaa0...dc)"
    # That means that there is a space between numbers
    pb_x = int(in_list[0][1:], 16)
    pb_y = int(in_list[1][1:-1], 16)

    pb = Point(pb_x, pb_y)

    # Iterate through all points on ECC
    subtotal = None
    for i in range(0, fp):
        subtotal = add(subtotal, g, fp, a)
        if subtotal.equals(pb):
            print(i + 1)
            return

    # If there is no number as given
    print(0)
    return
    


if __name__ == "__main__":
    decipher()

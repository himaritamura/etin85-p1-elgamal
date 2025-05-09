# finite curve over fixed finite field order > 100
class curve:
    # curve: y^2 = x^3 + 3x + 7 over F107
    p = 107
    a = 3
    b = 7

    def generate_points(self):
        points = set()

        for x in range(self.p):
            function = (x**3 + self.a*x + self.b) % self.p

            for y in range(self.p):
                if (y**2) % self.p == function:
                    points.add((x, y))
    
        return list(points)

    def mod_inverse(self, a):
        return pow(a, self.p-2, self.p)

    def additive_inverse(self, x, y):
        y_inverse = (self.p - y) % self.p
        return (x, y_inverse)

    def add_points(self, x1, y1, x2, y2):
        # infinity point
        if x1 == x2 and y1 != y2:
            return (None, None)
        
        # same point
        elif x1 == x2 and y1 == y2:
            return self.double_point(x1, y1)
        
        # adding to infinity point
        elif x1 is None and y1 is None:
            return (x2, y2)
        
        elif x2 is None and y2 is None:
            return (x1, y1)
        
        # normal case
        else:
            lamb = ((y2 - y1) * self.mod_inverse(x2 - x1)) % self.p
            x_res = (lamb**2 - x1 - x2) % self.p
            y_res = (lamb * (x1 - x_res) - y1) % self.p
            # print(x_res, y_res)
            return (x_res, y_res)

    def double_point(self, x, y):
        lamb = ((3 * (x**2) + self.a) * self.mod_inverse(2*y)) % self.p
        x_res = ((lamb**2) - (2*x)) % self.p
        y_res = ((lamb * (x - x_res)) - y) % self.p
        # print(f"DOUBLE_POINT: ({x_res}, {y_res})")
        return (x_res, y_res)

    def multiply_point(self, x, y, s):
        # infinity
        if s == 0:
            return (None, None)

        # self
        elif s == 1:
            return (x, y)
        
        # double and add method (uses bit-representation)
        else:
            # reverse bit string to iterate from right to left
            s_bits = '{0:b}'.format(s)[::-1]
            curr = None
            res = None

            for bit in s_bits:
                if curr is None:
                    curr = (x, y)
                else:
                    curr = self.double_point(curr[0], curr[1])

                # if bit is 1, add to total
                if int(bit) == 1:
                    if res is None:
                        res = curr
                    else:
                        # print(f"adding points: ({res[0]}, {res[1]}) and ({curr[0]}, {curr[1]})")
                        res = self.add_points(res[0], res[1], curr[0], curr[1])
            return res

    def order(self, x, y):
        total = (x, y)
        n = 1
        while total != (None, None):
            total = self.add_points(x, y, total[0], total[1])
            n += 1
        return n

    def test_functions(self):
        user_input = ''
        while user_input != "q":
            print("Which function would you like to test?")
            print("q to quit, l to list points, ai for additive inverse, ap for add points, dp for double point, mp for multiply point, or for order")
            user_input = input()
            
            if user_input == "q":
                print("Exiting tests")
                break

            elif user_input == "l":
                points = self.generate_points()
                print(f"Points ({len(points)}):")
                print(points)
            
            # additive inverse
            elif user_input == "ai":
                x = int(input("X-Coordinate: "))
                y = int(input("Y-Coordinate: "))
                x_inv, y_inv = self.additive_inverse(x, y)
                print(f"The additive inverse of ({x}, {y}) is ({x_inv}, {y_inv}).")
            
            # add points
            elif user_input == "ap":
                x1 = int(input("Point 1 X-Coordinate: "))
                y1 = int(input("Point 1 Y-Coordinate: "))
                x2 = int(input("Point 2 X-Coordinate: "))
                y2 = int(input("Point 2 Y-Coordinate: "))
                x_res, y_res = self.add_points(x1, y1, x2, y2)

                if x_res is None:
                    print(f"The addition of points ({x1}, {y1}) and ({x2}, {y2}) is the point at infinity.")
                else:
                    print(f"The addition of points ({x1}, {y1}) and ({x2}, {y2}) is ({x_res}, {y_res}).")

            # double point
            elif user_input == "dp":
                x = int(input("X-Coordinate: "))
                y = int(input("Y-Coordinate: "))
                x_res, y_res = self.double_point(x, y)
                if x_res is None:
                    print(f"Adding ({x}, {y}) with itself is the point at infinity.")
                else:
                    print(f"Adding ({x}, {y}) with itself is ({x_res}, {y_res}).")

            # multiply point
            elif user_input == "mp":
                x = int(input("X-Coordinate: "))
                y = int(input("Y-Coordinate: "))
                scalar = int(input("Scalar to multiply point: "))
                x_res, y_res = self.multiply_point(x, y, scalar)
                if x_res is None:
                    print(f"The point ({x}, {y}) multiplied by {scalar} is the point at infinity.")
                else:
                    print(f"The point ({x}, {y}) multiplied by {scalar} is ({x_res}, {y_res}).")

            # order of cyclic group generated by a point
            elif user_input == "or":
                x = int(input("X-Coordinate: "))
                y = int(input("Y-Coordinate: "))
                order = self.order(x, y)
                print(f"The order of the cyclic group generated by ({x}, {y}) is {order}.")

            print()
            print("---------------------------------------")
            print()
                

if __name__ == "__main__":
    c = curve()
    c.test_functions()
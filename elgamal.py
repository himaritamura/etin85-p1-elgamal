
import library
import numpy as np

class elgamal:
    # p = None
    # a = None
    # b = None

    # what is the generator g
    # choose random x from 1 to q-1
    # h = g^x
    # generator g = (86, 45)



    def __init__(self):
        self.curve = library.curve()

        self.p = self.curve.p
        self.a = self.curve.a
        self.b = self.curve.b

        self.Q_pub_key = None
        self.x_priv_key = None
        self.g = (86, 45)

        self.points = self.curve.generate_points()

    def setup(self):
        user_input = ""
        while (user_input != "q"):
            print("Would you like to setup the public key or the private key?")
            user_input = input("q to quit, pub for public, priv for private: ")

            if user_input == "q":
                break
            # elif user_input == 'g':
            #     x = int(input("X-Coordinate: "))
            #     y = int(input("Y-Coordinate: "))
            #     self.g = (x, y)
            
            elif user_input == "pub":
                print(f"The generator P is ({self.g[0]}, {self.g[1]}).")
                print("Please enter the new public key, Q = [x]P.")
                x = int(input("X-Coordinate: "))
                y = int(input("Y-Coordinate: "))
                self.Q_pub_key = (x, y)
            
            elif user_input == "priv":
                print(f"The generator P is ({self.g[0]}, {self.g[1]}).")
                x = int(input("Please enter the new private key, x: "))
                self.x_priv_key = x
                
    def map_to_point(self, m):
        return self.points[m]

    def map_from_point(self, point):
        return self.points.index(point)

    def encrypt(self):
        if self.Q_pub_key is None:
            print("Please set up the public key, Q, before encryption.")
            return None
        
        M = input("Please input your message, an integer in [0, 112]: ")

        # map point
        mapped_M = self.map_to_point(int(M))
        # print(f"DEBUG: mapped_M is {mapped_M[0]}, {mapped_M[1]}")

        # choose random k from 0 to q - 1
        k = np.random.randint(1, 114)

        # c1 = [k]P
        c1 = self.curve.multiply_point(self.g[0], self.g[1], k)

        # c2 = M + [k]Q
        kQ = self.curve.multiply_point(self.Q_pub_key[0], self.Q_pub_key[1], k)
        c2 = self.curve.add_points(mapped_M[0], mapped_M[1], kQ[0], kQ[1])

        # cipher = (c1, c2)
        print(f"c1 = ({c1[0]}, {c1[1]}), c2 = ({c2[0]}, {c2[1]})")
        return
        

    def decrypt(self):
        if self.x_priv_key is None:
            print("Please set up the private key, x, before decryption.")
            return None
        c1_x = int(input("Please enter c1 X-Coordinate: "))
        c1_y = int(input("Please enter c1 Y-Coordinate: "))

        c2_x = int(input("Please enter c2 X-Coordinate: "))
        c2_y = int(input("Please enter c2 Y-Coordinate: "))

        xc1 = self.curve.multiply_point(c1_x, c1_y, self.x_priv_key)
        neg_xc1 = self.curve.additive_inverse(xc1[0], xc1[1])

        # c2 - [x]c1
        mapped_M = self.curve.add_points(c2_x, c2_y, neg_xc1[0], neg_xc1[1])

        M = self.map_from_point(mapped_M)

        print(f"M = {M}")
        return

    def user_menu(self):
        user_input = ""

        while user_input != "q":
            print("What action would you like to take?")
            print("q to quit, s for setup, e for encrypt, d for decrypt")
            user_input = input()

            if user_input == "q":
                break
            elif user_input == "s":
                self.setup()
            elif user_input == "e":
                self.encrypt()
            elif user_input == "d":
                self.decrypt()
            
            print()
            print("---------------------------------------")
            print()


if __name__ == "__main__":
    eg = elgamal()
    eg.user_menu()
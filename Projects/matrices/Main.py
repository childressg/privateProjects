from matrix import Matrix

if __name__ == "__main__":
    m1 = Matrix.generate_matrix(3, 3, -9, 9)
    print(m1)
    print(m1 ** -2)
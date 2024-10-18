import random


class Matrix:
    @staticmethod
    def generate_data(rows, columns, min, max):
        data = [[None for _ in range(columns)] for _ in range(rows)]
        for i in range(rows):
            for j in range(columns):
                data[i][j] = random.randint(min, max)
        return data

    @staticmethod
    def generate_matrix(rows, columns, min, max):
        data = [[None for _ in range(columns)] for _ in range(rows)]
        for i in range(rows):
            for j in range(columns):
                data[i][j] = random.randint(min, max)
        return Matrix(data=data)

    @staticmethod
    def validate(data):
        l = len(data[0])
        for row in data:
            for value in row:
                if not isinstance(value, (int, float)):
                    return False
            if len(row) != l:
                return False
        return True

    @staticmethod
    def get_row_zero_count(matrix, row):
        if row > matrix.rows - 1:
            raise IndexError
        count = 0
        for i in range(matrix.columns):
            if matrix.data[row][i] == 0:
                count += 1
        return count


    @staticmethod
    def get_row_most_zeros(matrix):
        row = 0
        for r in range(matrix.rows):
            if Matrix.get_row_zero_count(matrix, r) > Matrix.get_row_zero_count(matrix, row):
                row = r
        return row

    @staticmethod
    def IDENTITY(n):
        matrix = Matrix(n, n)
        for i in range(n):
            matrix.data[i][i] = 1
        return matrix

    @staticmethod
    def get_sign(row, col):
        return (-1) ** (row + col)

    def __init__(self, rows:int=None, columns:int=None, data:list=None):
        self.rows = rows
        self.columns = columns
        self.data = data
        self.shape = (self.rows, self.columns)
        if data is None:
            self.data = self.generate_data(rows, columns, 0, 0)
        else:
            if not self.validate(data):
                raise Exception("Invalid data")
            self.rows = len(data)
            self.columns = len(data[0])
            self.shape = (self.rows, self.columns)

    def __repr__(self):
        biggest_length = -1
        for i in range(self.rows):
            for j in range(self.columns):
                num = self.data[i][j]
                if len(str(num)) > biggest_length:
                    biggest_length = len(f"{num:.2f}")

        s = ""
        for i in range(self.rows):
            if i == 0:
                s += "⎡"
            elif i == self.rows - 1:
                s += "⎣"
            else:
                s += "⎢"

            for j in range(self.columns):
                format_string = "{:>" + str(biggest_length + 1) + "}"
                if j == 0:
                    format_string = "{:>" + str(biggest_length) + "}"
                    s += format_string.format(f"{self.data[i][j]:.2f}")
                else:
                    s += format_string.format(f"{self.data[i][j]:.2f}")

            if i == 0:
                s += "⎤"
            elif i == self.rows - 1:
                s += "⎦"
            else:
                s += "⎥"
            s += "\n"
        return s

    def __add__(self, other):
        if self.rows != other.rows or self.columns != other.columns:
            raise Exception("Matrices must have the same number of rows and columns")
        matrix = Matrix(self.rows, self.columns)
        for row in range(self.rows):
            for col in range(self.columns):
                matrix.data[row][col] = self.data[row][col] + other.data[row][col]
        return matrix

    def __sub__(self, other):
        if self.rows != other.rows or self.columns != other.columns:
            raise Exception("Matrices must have the same number of rows and columns")
        matrix = Matrix(self.rows, self.columns)
        for row in range(self.rows):
            for col in range(self.columns):
                matrix.data[row][col] = self.data[row][col] - other.data[row][col]
        return matrix

    def __mul__(self, other):
        if isinstance(other, Matrix):
            if self.columns != other.rows:
                raise Exception("Matrice B must have a number of rows should be equal to the number of columns in A")
            matrix = Matrix(self.rows, other.columns)
            for col in range(other.columns):
                for row in range(self.rows):
                    sum = 0
                    for i in range(other.rows):
                        sum += self.data[row][i] * other.data[i][col]
                    matrix.data[row][col] = sum
            return matrix
        if isinstance(other, (int, float)):
            matrix = Matrix(self.rows, self.columns)
            for row in range(self.rows):
                for col in range(self.columns):
                    matrix.data[row][col] = self.data[row][col] * other
            return matrix
        else:
            raise Exception("Cannot multiply matrix by value")

    def transpose(self):
        if self.columns != self.rows:
            raise Exception("Matrix must have the same number of rows and columns")
        matrix = Matrix(self.rows, self.columns)
        for row in range(self.rows):
            for col in range(self.columns):
                matrix.data[col][row] = self.data[row][col]
        return matrix

    def remove_row_col(self, row, col):
        matrix = Matrix(self.rows - 1, self.columns - 1)
        r = 0
        for i in range(self.rows):
            c = 0
            if i != row:
                for j in range(self.columns):
                    if j != col:
                        matrix.data[r][c] = self.data[i][j]
                        c += 1
                r += 1
        return matrix

    def determinant(self):
        if self.columns != self.rows:
            raise Exception("Matrix must have the same number of rows and columns")
        if self.columns == 2:
            return self.data[0][0] * self.data[1][1] - self.data[0][1] * self.data[1][0]
        else:
            sub_determinants = []

            row = Matrix.get_row_most_zeros(self)
            for col in range(self.columns):
                if self.data[row][col] != 0:
                    sub_matrix = self.remove_row_col(row, col)
                    sub_determinant = sub_matrix.determinant()
                    sub_determinants.append(sub_determinant * self.data[row][col] * Matrix.get_sign(row, col))

            return sum(sub_determinants)

    def cofactor(self):
        if self.columns != self.rows:
            raise Exception("Matrix must have the same number of rows and columns")
        matrix = Matrix(self.rows, self.columns)
        for row in range(self.rows):
            for col in range(self.columns):
                matrix.data[row][col] = self.remove_row_col(row, col).determinant() * Matrix.get_sign(row, col)
        return matrix

    def inverse(self):
        return self.cofactor().transpose() * (1 / self.determinant())

    def __pow__(self, power, modulo=None):
        if self.columns != self.rows:
            raise Exception("Matrix must have the same number of rows and columns")
        matrix = Matrix(data=self.data)
        if power == 0:
            return Matrix.IDENTITY(self.rows)
        if power < 0:
            matrix = matrix.inverse()
            power = abs(power)
        exponentiation = matrix
        for i in range(power - 1):
            exponentiation = exponentiation * matrix
        return exponentiation
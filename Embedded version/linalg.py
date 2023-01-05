"""
LinAlg
------

A module to deal with matrices and vectors.
Implements methods for matrix multiplication, transpose, determinant, inverse and solving linear systems of equations, for example
"""

def linspace(start, stop, num=50, endIncluded=True):
    """
    Creates a vector with linear spaced values.
        :param start: first value of vector
        :param stop: last value of vector
        :param num: number of values in the vector
        :param endIncluded: whether the last value should be included in the vector or not
        :return: The vector with linear spaced values
    """
    start = float(start)
    stop = float(stop)
    num = int(num)

    step = 0
    if endIncluded:
        step = (stop - start) / (num - 1)
    else:
        step = (stop - start) / num

    vector = []
    for idx in range(num):
        vector.append(start + step*idx)

    return vector

def check_squareness(A):
    """
    Makes sure that a matrix is square.
        :param A: The matrix to be checked.
    """
    if len(A) != len(A[0]):
        raise ArithmeticError("Matrix must be square for current methods.")

def determinant(A, total=0):
    """
    Calculates the determinant of a matrix
        :param A: The matrix whose determinant we'll calculate.
        :return: The determinant of the matrix
    """
    indices = list(range(len(A)))
    
    if len(A) == 2 and len(A[0]) == 2:
        val = A[0][0] * A[1][1] - A[1][0] * A[0][1]
        return val

    for fc in indices:
        As = copy_matrix(A)
        As = As[1:]
        height = len(As)
        builder = 0

        for i in range(height):
            As[i] = As[i][0:fc] + As[i][fc+1:]

        sign = (-1) ** (fc % 2)
        sub_det = determinant(As)
        total += A[0][fc] * sign * sub_det

    return total

def check_non_singular(A):
    """
    Makes sure that a matrix is not singular.
        :param A: The matrix to be checked.
        :return: The determinant of the matrix, if it's nos singular (det = 0)
    """
    det = determinant(A)
    if det != 0:
        return det
    else:
        raise ArithmeticError("Singular Matrix!")
        
def zeros_matrix(rows, cols):
    """
    Creates a matrix filled with zeros.
        :param rows: the number of rows the matrix should have
        :param cols: the number of columns the matrix should have
        :return: list of lists that form the matrix.
    """
    M = []
    while len(M) < rows:
        M.append([])
        while len(M[-1]) < cols:
            M[-1].append(0.0)

    return M

def identity_matrix(n):
    """
    Creates and returns an identity matrix.
        :param n: the square size of the matrix
        :return: a square identity matrix
    """
    I = zeros_matrix(n, n)
    for i in range(n):
        I[i][i] = 1.0

    return I

def copy_matrix(A):
    """
    Creates and returns a copy of a matrix.
        :param M: The matrix to be copied
        :return: The copy of the given matrix
    """
    rows = len(A)
    cols = len(A[0])

    MC = zeros_matrix(rows, cols)

    for i in range(rows):
        for j in range(cols):
            MC[i][j] = A[i][j]

    return MC

def print_matrix(A):
    """
    Prints the matrix.
        :param M: The matrix to be printed
    """
    for row in A:
        print([round(x,3)+0 for x in row])

def transpose(A):
    """
    Creates and returns a transpose of a matrix.
        :param M: The matrix to be transposed
        :return: the transpose of the given matrix
    """
    rows = len(A)
    cols = len(A[0])

    MT = zeros_matrix(cols, rows)

    for i in range(rows):
        for j in range(cols):
            MT[j][i] = A[i][j]

    return MT

def inverse(A):
    """
    Creates and returns an inverse of a matrix.
        :param A: The matrix to be inversed
        :return: the inverse of the given matrix
    """
    det = determinant(A)
    #special case for 2x2 matrix:
    if len(A) == 2:
        return [[A[1][1]/det, -1*A[0][1]/det],
                [-1*A[1][0]/det, A[0][0]/det]]

    #find matrix of cofactors
    cofactors = []
    for r in range(len(A)):
        cofactorRow = []
        for c in range(len(A)):
            minor = [row[:c] + row[c+1:] for row in (A[:r]+A[r+1:])]
            cofactorRow.append(((-1)**(r+c)) * determinant(minor))
        cofactors.append(cofactorRow)
    cofactors = transpose(cofactors)
    for r in range(len(cofactors)):
        for c in range(len(cofactors)):
            cofactors[r][c] = cofactors[r][c]/det
    return cofactors

def matrix_multiply(A,B):
    """
    Returns the product of the matrix A * B.
        :param A: The first matrix - ORDER MATTERS!
        :param B: The second matrix
        :return: The product of the two matrices
    """
    rowsA = len(A)
    colsA = len(A[0])

    rowsB = len(B)
    colsB = len(B[0])

    if colsA != rowsB:
        raise ArithmeticError('Number of A columns must equal number of B rows.')

    C = zeros_matrix(rowsA, colsB)

    for i in range(rowsA):
        for j in range(colsB):
            total = 0
            for ii in range(colsA):
                total += A[i][ii] * B[ii][j]
            C[i][j] = total

    return C

def check_matrix_equality(A,B, tol=None):
    """
    Checks the equality of two matrices.
        :param A: The first matrix
        :param B: The second matrix
        :param tol: The decimal place tolerance of the check
        :return: The boolean result of the equality check
    """
    if len(A) != len(B) or len(A[0]) != len(B[0]):
        return False

    for i in range(len(A)):
        for j in range(len(A[0])):
            if tol == None:
                if A[i][j] != B[i][j]:
                    return False
            else:
                if round(A[i][j],tol) != round(B[i][j],tol):
                    return False

    return True

def solve_equations(A, B):
    """
    Returns the solution of a system of equations in matrix format.
        :param A: The system matrix
        :return: The solution X where AX = B
    """
    # Section 1: Make sure A can be inverted.
    check_squareness(A)
    check_non_singular(A)

    # Section 2: Make copies of A & I, AM & IM, to use for row operations
    n = len(A)
    AM = copy_matrix(A)
    I = identity_matrix(n)
    BM = copy_matrix(B)

    A_inv = inverse(AM)
    return matrix_multiply(A_inv, B)
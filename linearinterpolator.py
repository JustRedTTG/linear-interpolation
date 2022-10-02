def interpolate(matrix, x, y, percent):
    percent /= 100
    a, b, c, d = matrix[0][0], matrix[0][1], matrix[1][0], matrix[1][1]
    new = (
        a*x + b*y,
        c*x + d*y
    )
    change = (
        new[0]-x,
        new[1]-y
    )
    return (
        x+change[0]*percent,
        y+change[1]*percent
    )
def reverse_interpolate(matrix, x, y, percent):
    percent /= 100
    a, b, c, d = matrix[0][0], matrix[0][1], matrix[1][0], matrix[1][1]
    det = a * d - b * c
    newmatrix = [
        [d * det, b * det * -1],
        [c * det * -1, a * det]
    ]
    a, b, c, d = newmatrix[0][0], newmatrix[0][1], newmatrix[1][0], newmatrix[1][1]
    new = (
        a * x + b * y,
        c * x + d * y
    )
    change = (
        new[0] - x,
        new[1] - y
    )
    return (
        x + change[0] * percent,
        y + change[1] * percent
    )
def no_interpolation(matrix,x,y, percent):
    return (x,y)
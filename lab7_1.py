def bubble_sort_list(lst):
    n = len(lst)
    for i in range(n - 1):
        for j in range(n - i - 1):
            if lst[j] > lst[j + 1]:
                lst[j], lst[j + 1] = lst[j + 1], lst[j]


def sort_columns_quadratic(matrix):
    rows = len(matrix)
    cols = len(matrix[0])

    col_list = []
    for c in range(cols):
        for r in range(rows):
            col_list.append(matrix[r][c])
    bubble_sort_list(col_list)
    idx = 0
    for c in range(cols):
        for r in range(rows):
            matrix[r][c] = col_list[idx]
            idx += 1


def row_product_above_diagonal(matrix):
    rows = len(matrix)
    result = []

    for i in range(rows):
        product = 1
        has_val = False
        for j in range(i + 1, len(matrix[i])):
            product *= matrix[i][j]
            has_val = True
        result.append(product if has_val else 0)

    return result


def average(values):
    return sum(values) / len(values) if values else 0


def print_matrix(matrix):
    for row in matrix:
        print(" ".join(f"{x:4}" for x in row))


def main():
    matrix = [
        [50, 98, -4, 85, -8],
        [40, 73, -2, -9, -19],
        [1, 6, 73, 21, 0],
        [0, 25, 2, -5, -3],
        [99, 19, 95, 92, -7]
    ]

    print("Original matrix:")
    print_matrix(matrix)

    sort_columns_quadratic(matrix)

    print("\nSorted matrix:")
    print_matrix(matrix)

    fi_values = row_product_above_diagonal(matrix)
    print("\nfi(aij) values:", fi_values)

    print("\nF(fi(aij)) =", average(fi_values))


if __name__ == "__main__":
    main()

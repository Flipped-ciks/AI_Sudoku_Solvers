import time
import csv

class Node:
    def __init__(self, col=None):
        self.left = self
        self.right = self
        self.up = self
        self.down = self
        self.col = col
        self.row = None


class ColumnNode(Node):
    def __init__(self, name):
        super().__init__(self)
        self.name = name
        self.size = 0


class DancingLinks:
    def __init__(self, n):
        self.root = ColumnNode("root")
        self.columns = []
        for i in range(n):
            col = ColumnNode(str(i))
            self.columns.append(col)
            col.left = self.root.left
            col.right = self.root
            self.root.left.right = col
            self.root.left = col

    def add_row(self, row_index, cols):
        first = None
        last = None
        for col_index in cols:
            col = self.columns[col_index]
            node = Node(col)
            node.row = row_index
            node.up = col.up
            node.down = col
            col.up.down = node
            col.up = node
            col.size += 1
            if first is None:
                first = node
            if last is not None:
                node.left = last
                node.right = first
                last.right = node
                first.left = node
            last = node

    def cover(self, col):
        col.right.left = col.left
        col.left.right = col.right
        i = col.down
        while i != col:
            j = i.right
            while j != i:
                j.down.up = j.up
                j.up.down = j.down
                j.col.size -= 1
                j = j.right
            i = i.down

    def uncover(self, col):
        i = col.up
        while i != col:
            j = i.left
            while j != i:
                j.col.size += 1
                j.down.up = j
                j.up.down = j
                j = j.left
            i = i.up
        col.right.left = col
        col.left.right = col

    def search(self, k, solution):
        if self.root.right == self.root:
            return solution
        col = self.root.right
        min_size = col.size
        current = col.right
        while current != self.root:
            if current.size < min_size:
                col = current
                min_size = current.size
            current = current.right
        self.cover(col)
        r = col.down
        while r != col:
            solution.append(r.row)
            j = r.right
            while j != r:
                self.cover(j.col)
                j = j.right
            result = self.search(k + 1, solution)
            if result:
                return result
            j = r.left
            while j != r:
                self.uncover(j.col)
                j = j.left
            solution.pop()
            r = r.down
        self.uncover(col)
        return None


def sudoku_to_exact_cover(board):
    dlx = DancingLinks(324)
    for row in range(9):
        for col in range(9):
            for num in range(9):
                if board[row][col] == 0 or board[row][col] == num + 1:
                    cols = []
                    # 行 - 列约束
                    cols.append(row * 9 + col)
                    # 行 - 数字约束
                    cols.append(81 + row * 9 + num)
                    # 列 - 数字约束
                    cols.append(162 + col * 9 + num)
                    # 方块 - 数字约束
                    box = (row // 3) * 3 + (col // 3)
                    cols.append(243 + box * 9 + num)
                    dlx.add_row((row, col, num + 1), cols)
    return dlx


def solve_sudoku_dlx(board):
    dlx = sudoku_to_exact_cover(board)
    solution = dlx.search(0, [])
    if solution:
        for row, col, num in solution:
            board[row][col] = num
        return True
    return False


def string_to_board(s):
    """将字符串转换为数独棋盘"""
    return [
        [int(s[i*9 + j]) for j in range(9)]
        for i in range(9)
    ]


def board_to_string(board):
    """将数独棋盘转换为字符串"""
    return ''.join([str(board[i][j]) for i in range(9) for j in range(9)])


def print_board(bo):
    for i in range(len(bo)):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - - - - ")

        for j in range(len(bo[0])):
            if j % 3 == 0 and j != 0:
                print(" | ", end="")

            if j == 8:
                print(bo[i][j])
            else:
                print(str(bo[i][j]) + " ", end="")


def main():
    total_time = 0
    solved_count = 0
    total_count = 0
    max_rows = 1000  # 最多处理n行

    with open('data\\test.csv', 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            total_count += 1
            quiz = row['quizzes']
            solution = row['solutions']

            # 转换为棋盘
            quiz_board = string_to_board(quiz)
            answer_board = string_to_board(solution)

            # 复制棋盘用于求解
            board = [row[:] for row in quiz_board]

            print(f"\n求解第 {total_count} 个数独:")
            # print("求解前的数独矩阵:")
            # print_board(board)

            # 记录开始时间
            start_time = time.time()

            # 求解数独
            if solve_sudoku_dlx(board):
                end_time = time.time()
                elapsed_time = end_time - start_time
                total_time += elapsed_time
                solved_count += 1

                # 验证答案
                is_correct = True
                for i in range(9):
                    for j in range(9):
                        if board[i][j] != answer_board[i][j]:
                            is_correct = False
                            break
                    if not is_correct:
                        break

                # print("求解后的数独矩阵:")
                # print_board(board)
                print(f"结果: {'正确' if is_correct else '错误'}")
                print(f"耗时: {elapsed_time:.6f} 秒")
            else:
                end_time = time.time()
                print("无法解出数独")
                print(f"尝试耗时: {end_time - start_time:.6f} 秒")
            if total_count >= max_rows:
                break

    # 统计结果
    if total_count > 0:
        success_rate = solved_count / total_count * 100
        avg_time = total_time / solved_count if solved_count > 0 else 0
        print(f"\n===== 统计结果 =====")
        print(f"总题目数: {total_count}")
        print(f"成功求解: {solved_count}")
        print(f"成功率: {success_rate:.2f}%")
        print(f"平均耗时: {avg_time:.6f} 秒")

# # 样例，供参考
# sample  = [ [3,4,1,2,9,7,6,8,5],
#             [2,5,6,8,3,4,9,7,1],
#             [9,8,7,1,5,6,3,2,4],
#             [1,9,2,6,7,5,8,4,3],
#             [8,7,5,4,2,3,1,9,6],
#             [6,3,4,9,1,8,2,5,7],
#             [5,6,3,7,8,9,4,1,2],
#             [4,1,9,5,6,2,7,3,8],
#             [7,2,8,3,4,1,5,6,9] ]

if __name__ == "__main__":
    main()
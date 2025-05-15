import time
import csv

def solve(bo):
    find = find_empty(bo)
    if not find:
        return True
    else:
        row, col = find

    for i in range(1, 10):
        if valid(bo, i, (row, col)):
            bo[row][col] = i

            if solve(bo):
                return True

            bo[row][col] = 0

    return False


def valid(bo, num, pos):
    # Check row
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    # Check column
    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    # Check box
    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y * 3, box_y * 3 + 3):
        for j in range(box_x * 3, box_x * 3 + 3):
            if bo[i][j] == num and (i, j) != pos:
                return False

    return True


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


def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j)  # row, col

    return None


def string_to_board(s):
    """将字符串转换为数独棋盘"""
    return [
        [int(s[i * 9 + j]) for j in range(9)]
        for i in range(9)
    ]


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
            if solve(board):
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


if __name__ == "__main__":
    main()
import random, copy
import numpy as np
import csv

sample  = [ [3,4,1,2,9,7,6,8,5],
            [2,5,6,8,3,4,9,7,1],
            [9,8,7,1,5,6,3,2,4],
            [1,9,2,6,7,5,8,4,3],
            [8,7,5,4,2,3,1,9,6],
            [6,3,4,9,1,8,2,5,7],
            [5,6,3,7,8,9,4,1,2],
            [4,1,9,5,6,2,7,3,8],
            [7,2,8,3,4,1,5,6,9] ]
            
def construct_puzzle_solution():

    while True:
        try:
            puzzle  = [[0]*9 for i in range(9)]
            rows    = [set(range(1,10)) for i in range(9)]
            columns = [set(range(1,10)) for i in range(9)]
            squares = [set(range(1,10)) for i in range(9)]
            for i in range(9):
                for j in range(9):
                    choices = rows[i].intersection(columns[j]).intersection(squares[(i//3)*3 + j//3])
                    choice  = random.choice(list(choices))
        
                    puzzle[i][j] = choice
        
                    rows[i].discard(choice)
                    columns[j].discard(choice)
                    squares[(i//3)*3 + j//3].discard(choice)

            return puzzle
            
        except IndexError:
            pass

def pluck(puzzle, n=0):

    def canBeA(puz, i, j, c):
        v = puz[c//9][c%9]
        if puz[i][j] == v: return True
        if puz[i][j] in range(1,10): return False
            
        for m in range(9):
            if not (m==c//9 and j==c%9) and puz[m][j] == v: return False
            if not (i==c//9 and m==c%9) and puz[i][m] == v: return False
            if not ((i//3)*3 + m//3==c//9 and (j//3)*3 + m%3==c%9) and puz[(i//3)*3 + m//3][(j//3)*3 + m%3] == v:
                return False

        return True


    cells     = set(range(81))
    cellsleft = cells.copy()
    while len(cells) > n and len(cellsleft):
        cell = random.choice(list(cellsleft))
        cellsleft.discard(cell)

        row = col = square = False

        for i in range(9):
            if i != cell//9:
                if canBeA(puzzle, i, cell%9, cell): row = True
            if i != cell%9:
                if canBeA(puzzle, cell//9, i, cell): col = True
            if not (((cell//9)//3)*3 + i//3 == cell//9 and ((cell//9)%3)*3 + i%3 == cell%9):
                if canBeA(puzzle, ((cell//9)//3)*3 + i//3, ((cell//9)%3)*3 + i%3, cell): square = True

        if row and col and square:
            continue
        else:
            puzzle[cell//9][cell%9] = 0
            cells.discard(cell)

    return (puzzle, len(cells))
    
    
def run(n = 28, iter=100):
    all_results = {}
    a_puzzle_solution = construct_puzzle_solution()
    
    for i in range(iter):
        puzzle = copy.deepcopy(a_puzzle_solution)
        (result, number_of_cells) = pluck(puzzle, n)
        all_results.setdefault(number_of_cells, []).append(result)
        if number_of_cells <= n: break
 
    return all_results, a_puzzle_solution

def best(set_of_puzzles):
    return set_of_puzzles[min(set_of_puzzles.keys())][0]

def display(puzzle):
    for row in puzzle:
        print(' '.join([str(n or '_') for n in row]))

def main(num):
    with open('data\\sudoku.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['quizzes', 'solutions'])  # 写入表头
        
        for i in range(num):
            all_results, solution = run(n=23, iter=10)
            quiz = best(all_results)
            
            # 将9x9的二维数组展平为一维列表，并转换为字符串
            quiz_str = ''.join([str(num) for row in quiz for num in row])
            solution_str = ''.join([str(num) for row in solution for num in row])
            
            writer.writerow([quiz_str, solution_str])
            
            if (i + 1) % 1000 == 0:
                print(f"已生成 {i+1} 个数独谜题")
    
    print(f"已成功生成 {num} 个数独谜题并保存到 data\\sudoku.csv")

if __name__ == "__main__":
    main(1000000)       # 生成1000000个数独训练集
    # main(30)            # 生成30个数独测试集
    print("Done!")

import numpy as np

def canBeChanged(i, j):
	if i == 0 and (j == 0 or j == 2 or j == 4):
		return False
	if i == 1 and (j == 0 or j == 3 or j == 7):
		return False
	if i == 2 and (j == 0 or j == 4 or j == 6):
		return False
	if i == 3 and j == 1:
		return False
	if i == 4 and j == 4:
		return False
	if i == 5 and j == 7:
		return False
	if i == 6 and (j == 2 or j == 4 or j == 8):
		return False
	if i == 7 and (j == 1 or j == 5 or j == 8):
		return False
	if i == 8 and (j == 4 or j == 6 or j == 8):
		return False
	
	return True


def initialize_board(partial_board):
	"""Заполнение доски начальными значениями и случайными числами так, чтобы значения в строке были уникальны."""
	size = 9
	board = np.copy(partial_board)
	for i in range(size):
		for j in range(size):
			if board[i, j] == 0:  # если клетка пуста
				possible_values = [i for i in range(1, 10)]
				for value in possible_values:
					if is_safe_to_add(board, i, value):
						board[i, j] = value
						break
	return board

def is_safe_to_add(board, row, num):
	return not(num in board[row, :])

def is_safe(board, row, col, num):
	"""Проверка, можно ли вставить число в клетку."""
	block_row = (row // 3) * 3
	block_col = (col // 3) * 3
	return not (num in board[row, :] or
				num in board[:, col] or
				num in board[block_row:block_row+3, block_col:block_col+3])


def draw_board(board):
	for r in range(9):
		for c in range(9):
			print(board[r][c], end=" ")
		print()


def calculate_conflicts(board):
	conflicts = 0
	for i in range(9):
		conflicts += (9 - len(np.unique(board[i, :])))  # Row conflicts
		conflicts += (9 - len(np.unique(board[:, i])))  # Column conflicts
	for i in range(0, 9, 3):
		for j in range(0, 9, 3):
			sub_board = board[i:i+3, j:j+3].flatten()
			conflicts += (9 - len(np.unique(sub_board)))
	return conflicts


def generateBoards(board):
	size = 9
	new_boards = []
	indexes = []
	improved = False

	for r in range(size):
		indexes = []

		for j in range(size):
			if canBeChanged(r, j):
				indexes.append(j)

		current_conflicts = calculate_conflicts(board)

		for base_col in range(0, len(indexes) - 1):
			for col in range(base_col + 1, len(indexes)):
				board_copy = np.array(board).copy()
				c1 = indexes[base_col]
				c2 = indexes[col]

				temp = board_copy[r][c1]
				board_copy[r][c1] = board_copy[r][c2]
				board_copy[r][c2] = temp

				new_confilicts = calculate_conflicts(board_copy)
				if (new_confilicts < current_conflicts):
					improved = True
					new_boards.append((board_copy, new_confilicts))
	
	if not(improved):
		for r in range(size):
			current_conflicts = calculate_conflicts(board)

			for base_col in range(0, len(indexes) - 1):
				for col in range(base_col + 1, len(indexes)):
					board_copy = np.array(board).copy()
					c1 = indexes[base_col]
					c2 = indexes[col]

					temp = board_copy[r][c1]
					board_copy[r][c1] = board_copy[r][c2]
					board_copy[r][c2] = temp

					new_confilicts = calculate_conflicts(board_copy)
					new_boards.append((board_copy, new_confilicts))
	
	return new_boards


def guided_local_search(board, max_iterations=5000):
	"""Основной цикл Guided Local Search."""
	next_boards = [np.array(board).copy()]
	size = 9
	result_count = 100
	result_board = []

	for _ in range(max_iterations):
		print(_)
		for board_iter in next_boards:	
			next = []
			next_possible = generateBoards(board_iter)
			sorted_boards = sorted(next_possible, key=lambda x: x[1])[:4]
			for next_possible_item, value in sorted_boards:
				# print(value)
				if (value < result_count):
					result_count = value
					result_board = next_possible_item

				if value == 0:
					return result_board
				next.append(next_possible_item)
			
			next_boards = [i for i in next]
	return result_board

# Пример начального состояния доски (0 означает пустую клетку)
initial_board = np.array([
	[9, 0, 2, 0, 1, 0, 0, 0, 0],
	[8, 0, 0, 2, 0, 0, 0, 9, 0],
	[1, 0, 0, 0, 8, 0, 5, 0, 0],
	[0, 1, 0, 0, 0, 0, 0, 0, 0],
	[0, 0, 0, 0, 5, 0, 0, 0, 0],
	[0, 0, 0, 0, 0, 0, 0, 5, 0],
	[0, 0, 8, 0, 4, 0, 0, 0, 9],
	[0, 7, 0, 0, 0, 8, 0, 0, 6],
	[0, 0, 0, 0, 9, 0, 8, 0, 5]
])

board = initialize_board(initial_board)
solution = guided_local_search(board)
draw_board(board)
print(calculate_conflicts(board))
draw_board(solution)
print(calculate_conflicts(solution))
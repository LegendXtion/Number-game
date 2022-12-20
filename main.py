START_TIME = 0
END_TIME = 0
NUMBER = 4
SCORE_CHECK = []

import random
import tkinter as tk
import time
from tkinter.messagebox import showinfo
from config import SHOW_WARNING, POSSIBLE_GAMES, DESCRIPTION, SHOW_NUMBER_AFTER_CLICK

with open('levels_completed.txt') as config:
	STATUS = [i.strip().split(',') for i in config.readlines()]
	alpha = lambda x: x[0]
	beta = lambda y: y[1]
	LevelStatus = list(map(alpha, STATUS))
	ScoreStatus = list(map(beta, STATUS))
	
class GameWidget():
	def __init__(self, num, row, column, master, colour='red'):
		self.x = tk.Button(master=master, text=f'{num}X{num}', command=lambda: start(num), bg=colour, width=12, fg='orchid', font = ['Arial', 20],)
		self.x.grid(row=row, column=column)

class PlayWidget():
	def __init__(self, num, row, column, master):
		self.x = tk.Button(master=master, text=num, command=lambda: printScore(num, self.x), font=['Arial', 14], fg='cyan', bg='black', width=5)
		self.x.grid(row=row, column=column)

def showStats():
	stat_win = tk.Toplevel()
	stat_win.wm_title('Score Card')
	tk.Label(master=stat_win, text='GAME', fg='black', width = 15, font=['Arial', 16]).grid(row=0, column=0)
	tk.Label(master=stat_win, text='TIME TAKEN (in sec)', fg='black', font=['Arial', 16]).grid(row=0, column=1)
	for c,i in enumerate(POSSIBLE_GAMES.keys()):
		tk.Label(master=stat_win, text=f'{i}X{i}', fg='blue', font=['Arial', 13]).grid(row=c+1, column=0)
	for c,i in enumerate(ScoreStatus):
		tk.Label(master=stat_win, text=i, fg='blue', font=['Arial', 13]).grid(row=c+1, column=1)

	
def game_matrix_generate(iterator=4):
	num_arr = list(range(1,iterator**2+1))
	random.shuffle(num_arr)
	num_arr_matrix = []
	for i in range(0,iterator**2,iterator):
		num_arr_matrix.append(num_arr[i:i+iterator])
	return num_arr_matrix

def start(m):
	global NUMBER, DESCRIPTION, SCORE_CHECK
	NUMBER = m
	SCORE_CHECK = list(range(NUMBER**2, 0, -1))
	if SHOW_WARNING:
		showinfo('Description', DESCRIPTION)
	game_start()

def game_start():
	root.destroy()
	
	# SCREEN 2
	global START_TIME, NUMBER
	global root2
	root2 = tk.Tk()
	matrix = game_matrix_generate(iterator=NUMBER)
	START_TIME = time.time()
	for col_count, col in enumerate(matrix):
		for num_count, num in enumerate(col):
			PlayWidget(row=col_count, column=num_count, master=root2, num=num)
	root2.mainloop()

def printScore(number, game):
	global NUMBER, SCORE_CHECK
	if SCORE_CHECK.pop() == number:
		if SHOW_NUMBER_AFTER_CLICK:
			game.config(state='disabled')
		else:
			pass
	else:
		LevelStatus[NUMBER-3] = "2"
		with open('levels_completed.txt', 'w') as config:
			[config.write(i+','+j+'\n') for i, j in zip(LevelStatus, ScoreStatus)]
		showinfo('You Loose', 'Looser')
		root2.destroy()
		main()
	if len(SCORE_CHECK)==0:
		global START_TIME, END_TIME
		END_TIME = time.time()
		TimeTaken = round(END_TIME - START_TIME)
		showinfo('Winner', f'Time Taken: {TimeTaken} seconds')
		LevelStatus[NUMBER-3] = "1"
		ScoreStatus[NUMBER-3] = str(TimeTaken)
		with open('levels_completed.txt', 'w') as config:
			[config.write(i+','+j+'\n') for i, j in zip(LevelStatus, ScoreStatus)]
		root2.destroy()
		main()

def main():
	global root
	root = tk.Tk()
	root.title('Number Game')
	root.config(bg='black')

	ro=0
	temp = 1
	for game, col in POSSIBLE_GAMES.items():
		if LevelStatus[game-3]=="1":
			colour = 'chartreuse'
		elif LevelStatus[game-3]=="2":
			colour = 'gold'	
		else:
			colour = 'dark red'
		GameWidget(master=root, num=game, row=ro, column=col, colour=colour)
		ro+=1
		if ro==4:
			ro=0
			temp+=1

	#COMPLETE LABEL
	tk.Label(root, text='Completed', font = ['Arial', 20], bg = 'black', fg = 'white').grid(row=0, column=3)
	tk.Entry(root, width=4, bg='chartreuse').grid(row=0, column=4)
	#PENDING LABEL
	tk.Label(root, text='Pending', font = ['Arial', 20], bg = 'black', fg = 'white').grid(row=1, column=3)
	tk.Entry(root, width=4, bg='gold').grid(row=1, column=4)
	#NOT STARTED LABEL
	tk.Label(root, text='Not Started', font = ['Arial', 20], bg = 'black', fg = 'white').grid(row=2, column=3)
	tk.Entry(root, width=4, bg='dark red').grid(row=2, column=4)
	#Show Stats
	tk.Button(root, text = 'Score Card', font=['Arial', 20], command = showStats, bg='grey', fg='cyan').grid(row=3, column=3, columnspan=2)

	root.mainloop()




if __name__ == '__main__':
	main()

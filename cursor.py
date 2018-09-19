import curses
from curses import wrapper, textpad

# stdscr = curses.initscr()

def messages_screen(y, x, stdscr):
	# stdscr = curses.initscr()
	pad = curses.newpad(8, x/3 + x+x/2-2)
	# nlines 

	# curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_BLUE)
	# pad.bkgd(' ', curses.color_pair(1))

	x2 = (x+2)*2
	ncols = x+x/2
	ulx = x/3
	# stdscr.addstr(str(y))

	textpad.rectangle(stdscr, y+3, ulx-1, 15, ulx + ncols)

	pad.scrollok(1)
	return pad

	
def test_textpad(x, y, stdscr, insert_mode=False):
	ncols, nlines = x+x/2, 1
	uly, ulx = y, x/3

	# stdscr.addstr(uly-2, ulx, "Use Ctrl-G to send the message.")
	win = curses.newwin(nlines, ncols, uly, ulx)
	textpad.rectangle(stdscr, uly-1, ulx-1, uly + nlines, ulx + ncols)
	stdscr.refresh()

	box = textpad.Textbox(win, insert_mode)
	contents = box.edit()

	
	# stdscr.addstr('\n')
	stdscr.addstr(uly-2, ulx, 'Press any key to write again.')
	# stdscr.getch()
	stdscr.addstr(uly-2, ulx, '										')

	return contents

def main(stdscr):
	# Clear screen
	stdscr.clear()

	x, y = stdscr.getmaxyx()
	y=stdscr.getmaxyx()[0] / 7
	x=stdscr.getmaxyx()[1] / 2 - 2

	# with open('welcome_message.txt', 'r') as myfile:
	# 	data=myfile.read().replace('\n', '')

	# for msg in data:
	# 	stdscr.addstr(y, x, msg)

	stdscr.addstr(y, x, "Welcome")

	pad = messages_screen(y, x, stdscr)
	

	while True:
		# pad = messages_screen(y, x, stdscr)
		msg = test_textpad(x, y*7-2, stdscr, True)
		pad.addstr(msg + "\n")
		pad.refresh( 0,0, 7,15, 28, x/3 + x+x/2-2)
	# stdscr.textpad.Textbox

	stdscr.refresh()
	stdscr.getkey()

wrapper(main)

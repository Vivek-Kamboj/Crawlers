#python3
import os
if 'Linux' in os.uname():
	print('Linux Distro!!')
	path=os.path.expanduser('~')+'~/.config/google-chrome/Default/History'
	print(path)
	try:
		files=os.listdir(path)
	except FileNotFoundError:
		print('No such path!')

print(r'\AppData\Local\Google\Chrome\User Data\Default')
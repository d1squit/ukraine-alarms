import json
import requests

from tkinter import *
from tkinter import ttk
from PIL import Image

from pystray import MenuItem
import pystray

regions = ['Автономна Республіка Крим', 'Вінницька область', 'Волинська область', 'Дніпропетровська область', 'Донецька область', 'Житомирська область', 'Закарпатська область',
		   'Запорізька область', 'Івано-Франківська область', 'Кіровоградська область', 'Луганська область', 'Львівська область', 'Миколаївська область', 'Одеська область',
		   'Полтавська область', 'Рівненська область', 'Сумська область', 'Тернопільська область', 'Харківська область', 'Хмельницька область', 'Черкаська область',
		   'Чернівецька область', 'Чернігівська область', 'Херсонська область', 'Київська область', 'м Кривий Ріг та Криворізька територіальна громада', 'м Київ',
		   'м Нікополь та Нікопольська територіальна громада']

states = {
	'alarm': {'desc': 'There is alarm in your region', 'icon': 'icons/alarm.png'},
	'no_alarm': {'desc': 'There is alarm in your region', 'icon': 'icons/no_alarm.png'},
	'ready': {'desc': 'High chance of an alarm', 'icon': 'icons/ready.png'},
}

url = 'https://alarmmap.online/assets/json/_alarms/siren.json'
current_alarms = []
current_state = 'no_alarm'

root = Tk()
root.title("Alarms")

region = StringVar()
timeout = StringVar(value='1')
minimum = StringVar(value='10')

root.geometry("400x150")
root.resizable(False, False)
root.iconbitmap('icons/no_alarm.png')

frame1 = Frame()
frame1.pack(fill=X)

frame2 = Frame()
frame2.pack(fill=X)

frame3 = Frame()
frame3.pack(fill=X)

label_region = Label(frame1, text="Choose your region", width=26, anchor="w", justify=LEFT)
label_region.pack(side=LEFT, padx=5, pady=5)

combo_region = ttk.Combobox(frame1, values=regions, textvariable=region)
combo_region.current(0)
combo_region.pack(fill=X, padx=5, expand=True)

label_timeout = Label(frame2, text="Choose timeout (in seconds)", width=26, anchor="w", justify=LEFT)
label_timeout.pack(side=LEFT, padx=5, pady=5)

entry_timeout = Entry(frame2, textvariable=timeout)
entry_timeout.pack(fill=X, padx=5, expand=True)

label_minimum = Label(frame3, text="Choose minimum for ready state", width=26, anchor="w", justify=LEFT)
label_minimum.pack(side=LEFT, padx=5, pady=5)

entry_minimum = Entry(frame3, textvariable=minimum)
entry_minimum.pack(fill=X, padx=5, expand=True)


def quit_window(icon):
	icon.stop()
	root.destroy()


def show_window(icon):
	icon.stop()
	root.after(0, root.deiconify())


def hide_window():
	root.withdraw()
	image = Image.open(states[current_state]['icon'])
	menu = (MenuItem('Settings', show_window), MenuItem('Quit', quit_window))
	icon = pystray.Icon("Alarms", image, states[current_state]['desc'], menu)
	icon.run()


def get_alarms():
	global current_state

	html = requests.get(url).text
	alarms = []
	if html != '':
		alarms = json.loads(html)
	if type(alarms) != list:
		return False

	current_state = 'no_alarm'

	for alarm in alarms:
		if alarm not in current_alarms:
			current_alarms.append(alarm)

		if alarm['district'].replace('_', ' ') == region.get():
			current_state = 'alarm'
			break

	if minimum.get() == '' or timeout.get() == '':
		return False

	if len(current_alarms) > int(minimum.get()) and current_state == 'no_alarm':
		current_state = 'ready'
		states['ready']['desc'] += f' ({len(current_alarms)} regions)'

	print(current_state)
	root.after(int(timeout.get()) * 1000, get_alarms)


root.after(1000, get_alarms)
root.protocol('WM_DELETE_WINDOW', hide_window)
root.mainloop()

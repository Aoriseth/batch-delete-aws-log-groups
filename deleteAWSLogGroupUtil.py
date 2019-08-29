import tkinter
import subprocess
import json


def deleteSelected(listbox):
	values = [listbox.get(index) for index in listbox.curselection()]
	for entry in values:
		deleteFromAws(entry)
	refreshList(listbox)

def refreshList(listbox):
	listbox.delete(0,"end")
	updateListFromAWS(listbox)

def updateListFromAWS(listbox):
	result = subprocess.run(['aws','logs','describe-log-groups'], stdout=subprocess.PIPE, shell=True)
	logGroups = json.loads(result.stdout)
	for entry in logGroups['logGroups']:
		listbox.insert("end",entry['logGroupName'])

def deleteFromAws(entry):
	subprocess.run(['aws','logs','delete-log-group','--log-group-name',entry], shell=True)


root = tkinter.Tk()
root.title("AWS Log-group Killer")

frame = tkinter.Frame(root,bd=6)
frame.pack()

title = tkinter.Label(frame,text="Select log-groups to delete:")
title.pack()

lstbox = tkinter.Listbox(frame, selectmode="extended",width=100, height=30)
lstbox.pack()

updateListFromAWS(lstbox)

deleteButton = tkinter.Button(frame,text="Delete Selected",command=lambda: deleteSelected(lstbox))
deleteButton.pack()
root.mainloop()
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication,QWidget,QLabel,QPushButton,QListWidget,QTextEdit,QVBoxLayout,QHBoxLayout,QLineEdit,QInputDialog
import json
notes={
"About planets" : 
     	{
        		"text" : "What if water on Mars is a sign of life?",
        		"tags" : ["Mars", "hypotheses"]
    		},
"About black holes" : 
     	{
        		"text" : "There is no singularity on the event horizon",
        		"tags" : ["black holes", "facts"]
    		}
}
#with open('file1.json','w') as file:
 #json.dump(notes,file, sort_keys=True, ensure_ascii=False)

app=QApplication([])
window=QWidget()
window.setWindowTitle('smart note App')
window.setFixedSize(700,500)

lb1=QLabel('List of notes')
list_notes=QListWidget()
btn_createNote=QPushButton('create Note')
btn_delNote=QPushButton('delete note')
btn_saveNote=QPushButton('Save Note')

lb2=QLabel('List of tags')

list_tags=QListWidget()

field_tag=QLineEdit('')
field_tag.setPlaceholderText('Enter tag...')


btn_add=QPushButton('add to note')
btn_untag=QPushButton('untag from note')
btn_search=QPushButton('Search Note by tag')

Note_text=QTextEdit()

h2=QHBoxLayout()
h2.addWidget(btn_createNote)
h2.addWidget(btn_delNote)

h3=QHBoxLayout()
h3.addWidget(btn_add)
h3.addWidget(btn_untag)

v1=QVBoxLayout()

v1.addWidget(lb1)
v1.addWidget(list_notes)
v1.addLayout(h2)
v1.addWidget(btn_saveNote)
v1.addWidget(lb2)
v1.addWidget(list_tags)
v1.addWidget(field_tag)
v1.addLayout(h3)
v1.addWidget(btn_search)


main_layout=QHBoxLayout()
main_layout.addWidget(Note_text,stretch=2)
main_layout.addLayout(v1,stretch=1)

window.setLayout(main_layout)

def show_note():
	key=list_notes.selectedItems()[0].text()

	Note_text.setText(notes[key]['text'])
	list_tags.clear()
	list_tags.addItems(notes[key]['tags'])

def add_note():
	note_name, ok = QInputDialog.getText(window,'add Note','Enter Note Name:')

	if ok and note_name !='':
		notes[note_name]= {"text" : '',"tags" : []}
		list_notes.clear()
		list_notes.addItems(notes)
def save_note():
		key=list_notes.selectedItems()[0].text()
		
		if list_notes.selectedItems():
			notes[key]["text"] =Note_text.toPlainText()
			with open("file1.json", "w") as file:
				json.dump(notes, file, sort_keys=True, ensure_ascii=False)
				print('Note Saved....')

def del_note():
	if list_notes.selectedItems():
		key=list_notes.selectedItems()[0].text()
		print(key)
		del notes[key]
		list_notes.clear()
		list_tags.clear()
		Note_text.clear()
		list_notes.addItems(notes)
		with open("file1.json", "w") as file:
			json.dump(notes, file, sort_keys=True, ensure_ascii=False)

def add_tag():
	if list_notes.selectedItems():
		key=list_notes.selectedItems()[0].text()#notes[key]['text']
		tag=field_tag.text()
		print(tag)
		if not tag in notes[key]['tags']:
			notes[key]['tags'].append(tag)
			list_tags.clear()
			list_tags.addItems(notes[key]['tags'])

			with open("file1.json", "w") as file:
				json.dump(notes, file, sort_keys=True, ensure_ascii=False)
			field_tag.clear()

def del_tag():
	if list_notes.selectedItems():
		key=list_notes.selectedItems()[0].text()
		if list_tags.selectedItems():
			tag=list_tags.selectedItems()[0].text()
			notes[key]['tags'].remove(tag)
			list_tags.clear()
			list_tags.addItems(notes[key]['tags'])
			with open("file1.json", "w") as file:
					json.dump(notes, file, sort_keys=True, ensure_ascii=False)
		else:
			print('select tag...')

def search_tag():
	tag=field_tag.text()
	if btn_search.text()=='Search Note by tag':
		filterd_notes={}
		for key in notes:
			if tag in notes[key]['tags']:
				filterd_notes[key]=notes[key]
			list_notes.clear()
			list_tags.clear()
			field_tag.clear()
			list_notes.addItems(filterd_notes)
			btn_search.setText('reset search')

	elif btn_search.text()=='reset search':
			list_notes.clear()
			list_tags.clear()
			field_tag.clear()
			Note_text.clear()
			list_notes.addItems(notes)
			btn_search.setText('Search Note by tag')

	



with open ('file1.json','r') as file:
	notes=json.load(file)

list_notes.addItems(notes)


list_notes.itemClicked.connect(show_note)
btn_createNote.clicked.connect(add_note)
btn_saveNote.clicked.connect(save_note)
btn_delNote.clicked.connect(del_note)
btn_add.clicked.connect(add_tag)
btn_untag.clicked.connect(del_tag)
btn_search.clicked.connect(search_tag)
window.show()
app.exec_()
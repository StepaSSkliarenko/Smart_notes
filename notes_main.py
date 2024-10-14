#начни тут создавать приложение с умными заметками
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QListWidget, QLineEdit, QTextEdit, QInputDialog, QHBoxLayout, QVBoxLayout, QFormLayout
import json

notes = {"Добро пожаловать!":
            {"Текст": "В этом приложении можно создавать заметки с тегами",
             "Теги":["Умные заметки", "Инструкция"]}
            }

with open("notes.json","r",encoding="UTF-8") as file:
    notes = json.load(file)

app = QApplication([])
window = QWidget()
note_text = QTextEdit()
notes_list = QListWidget()
label_notes = QLabel("Спписок заметок")
create_note = QPushButton("Создать заметку")
delite_note = QPushButton("Удалить заметку")
save_note = QPushButton("Сохранить заметку")
tags_list = QListWidget()
label_tags = QLabel("Список тегов")
line_tegs = QLineEdit()
line_tegs.setPlaceholderText("Введите тег")
add_teg = QPushButton("Добавить тег")
delite_teg = QPushButton("Открепить тег")
search_teg = QPushButton("Искать заметки по тегу")
main_line = QHBoxLayout()
hl1 = QHBoxLayout()
hl2 = QHBoxLayout()
vl1 = QVBoxLayout()

hl1.addWidget(create_note)
hl1.addWidget(delite_note)

hl2.addWidget(add_teg)
hl2.addWidget(delite_teg)

vl1.addWidget(label_notes)
vl1.addWidget(notes_list)

vl1.addLayout(hl1)
vl1.addWidget(save_note)
vl1.addWidget(label_tags)
vl1.addWidget(tags_list)

vl1.addWidget(line_tegs)
vl1.addLayout(hl2)

vl1.addWidget(search_teg)
main_line.addWidget(note_text)
main_line.addLayout(vl1)

window.setLayout(main_line)
def show_note():
    name = notes_list.selectedItems()[0].text()
    note_text.setText(notes[name]["Текст"])
    tags_list.clear()
    tags_list.addItems(notes[name]["Теги"])

def add_note():
    note_name, ok = QInputDialog.getText(window,"Добавить заметку","Название заметки:")
    if ok and note_name != "":
        notes[note_name] = {"Текст": "", "Теги": []}
        notes_list.addItem(note_name)

def del_note():
    if notes_list.selectedItems():
        note = notes_list.selectedItems()[0].text()
        del notes[note]
        notes_list.clear()
        tags_list.clear()
        note_text.clear()
        notes_list.addItems(notes)
        with open("notes.json","w",encoding="UTF-8") as file:
            json.dump(notes, file, ensure_ascii=False)
    else:
        print("Заметка для удаления не выбрана!")

def save_notes():
    if notes_list.selectedItems():
        note = notes_list.selectedItems()[0].text()
        notes[note]["Текст"] = note_text.toPlainText()
        with open("notes.json","w",encoding="UTF-8") as file:
            json.dump(notes, file, ensure_ascii=False)
    else:
        print("Заметка для сохранения не выбрана!")

def add_tag():
    if notes_list.selectedItems():
        note = notes_list.selectedItems()[0].text()
        tag = line_tegs.text()
        if not tag in notes[note]["Теги"]:
            notes[note]["Теги"].append(tag)
            tags_list.addItem(tag)
            line_tegs.clear()
        with open("notes.json","w",encoding="UTF-8") as file:
            json.dump(notes, file, ensure_ascii=False)
    else:
        print("Заметка для добавления тега не выбрана!")

def del_tag():
    if tags_list.selectedItems():
        note = notes_list.selectedItems()[0].text()
        tag = tags_list.selectedItems()[0].text()
        notes[note]["Теги"].remove(tag)
        tags_list.clear()
        tags_list.addItems(notes[note]["Теги"])
        with open("notes.json","w",encoding="UTF-8") as file:
            json.dump(notes, file, ensure_ascii=False)
    else:
        print("Тег для удаления не выбран!")

def search_tag():
    tag = line_tegs.text()
    if search_teg.text() == "Искать заметки по тегу" and tag != "":
        filter_notes = {}
        for note in notes:
            if tag in notes[note]["Теги"]:
                filter_notes[note] = notes[note]
        search_teg.setText("Сбросить поиск")
        tags_list.clear()
        notes_list.clear()
        note_text.clear()
        notes_list.addItems(filter_notes)
    elif search_teg.text() == "Сбросить поиск":
        tags_list.clear()
        notes_list.clear()
        note_text.clear()
        line_tegs.clear()
        notes_list.addItems(notes)
        search_teg.setText("Искать заметки по тегу")


        
notes_list.itemClicked.connect(show_note)
notes_list.addItems(notes)
create_note.clicked.connect(add_note)
delite_note.clicked.connect(del_note)
save_note.clicked.connect(save_notes)
delite_teg.clicked.connect(del_tag)
add_teg.clicked.connect(add_tag)
search_teg.clicked.connect(search_tag)

window.show()
app.exec_()
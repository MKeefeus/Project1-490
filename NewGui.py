import sys
import sqlite3
import feedparser
import re
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


class LoadOptions(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(300, 200))
        self.setWindowTitle("Load options")

        self.refresh_button = QPushButton('Clear and reload database', self)
        self.refresh_button.clicked.connect(self.refresh)
        self.refresh_button.resize(200, 32)
        self.refresh_button.move(50, 50)

        self.load_button = QPushButton('Load database', self)
        self.load_button.clicked.connect(self.load)
        self.load_button.resize(200, 32)
        self.load_button.move(50, 90)

        self.update_button = QPushButton('Update database', self)
        self.update_button.clicked.connect(self.update_selection)
        self.update_button.resize(200, 32)
        self.update_button.move(50, 130)

    def update_selection(self):
        connection = sqlite3.connect('jobs.db')
        cursor = connection.cursor()

        self.create_db(cursor)
        self.update_db(cursor)

        connection.commit()
        cursor.close()
        connection.close()

        self.exit_options()

    def load(self):
        connection = sqlite3.connect('jobs.db')
        cursor = connection.cursor()

        self.create_db(cursor)

        connection.commit()
        cursor.close()
        connection.close()

        self.exit_options()

    def refresh(self):
        connection = sqlite3.connect('jobs.db')
        cursor = connection.cursor()

        self.clear_db(cursor)
        self.create_db(cursor)
        self.populate_db(cursor)

        connection.commit()
        cursor.close()
        connection.close()

        self.exit_options()

    def clear_db(self, cursor):
        cursor.execute("""DROP TABLE IF EXISTS jobs""")

    def create_db(self, cursor):
        cursor.execute("""CREATE TABLE IF NOT EXISTS jobs(
                                title text,
                                tags text,
                                author text,
                                date_published text,
                                description text,
                                location text,
                                links text,
                                allows_remote text
                                )""")

    def populate_db(self, cursor):
        feed = feedparser.parse("https://stackoverflow.com/jobs/feed")
        length = len(feed['entries'])
        for x in range(length):
            if 'title' in feed['entries'][x]:
                curr_title = feed['entries'][x]['title']
                if curr_title.find("allows remote") != -1:
                    curr_remote = "Yes"
                else:
                    curr_remote = "No"
            else:
                curr_title = "None"
            if 'tags' in feed['entries'][x]:
                curr_tags = ' '.join(str(e) for e in feed['entries'][x]['tags'])
            else:
                curr_tags = "None"
            if 'author' in feed['entries'][x]:
                curr_author = feed['entries'][x]['author']
            else:
                curr_author = "None"
            if 'published' in feed['entries'][x]:
                curr_date = feed['entries'][x]['published']
            else:
                curr_date = "None"
            if 'summary' in feed['entries'][x]:
                curr_description = feed['entries'][x]['summary']
            else:
                curr_description = "None"
            if 'location' in feed['entries'][x]:
                curr_location = feed['entries'][x]['location']
            else:
                curr_location = "None"
            if 'links' in feed['entries'][x]:
                curr_links = ' '.join(str(e) for e in feed['entries'][x]['links'])
            else:
                curr_links = "None"
            cursor.execute(
                "INSERT INTO jobs VALUES (:title, :tags, :author, :date_published, :description, :location, :links, :allows_remote)",
                {'title': curr_title,
                 'tags': curr_tags,
                 'author': curr_author,
                 'date_published': curr_date,
                 'description': curr_description,
                 'location': curr_location,
                 'links': curr_links,
                 'allows_remote': curr_remote
                 })

    def update_db(self, cursor):
        feed = feedparser.parse("https://stackoverflow.com/jobs/feed")
        length = len(feed['entries'])
        for x in range(length):
            if 'title' in feed['entries'][x]:
                curr_title = feed['entries'][x]['title']
                if curr_title.find("allows remote") != -1:
                    curr_remote = "Yes"
                else:
                    curr_remote = "No"
            else:
                curr_title = "None"
            if 'tags' in feed['entries'][x]:
                curr_tags = ' '.join(str(e) for e in feed['entries'][x]['tags'])
            else:
                curr_tags = "None"
            if 'author' in feed['entries'][x]:
                curr_author = feed['entries'][x]['author']
            else:
                curr_author = "None"
            if 'published' in feed['entries'][x]:
                curr_date = feed['entries'][x]['published']
            else:
                curr_date = "None"
            if 'summary' in feed['entries'][x]:
                curr_description = feed['entries'][x]['summary']
            else:
                curr_description = "None"
            if 'location' in feed['entries'][x]:
                curr_location = feed['entries'][x]['location']
            else:
                curr_location = "None"
            if 'links' in feed['entries'][x]:
                curr_links = ' '.join(str(e) for e in feed['entries'][x]['links'])
            else:
                curr_links = "None"
            cursor.execute(
                "INSERT INTO jobs (title, tags, author, date_published, description, location, links, allows_remote) "
                "SELECT :title, :tags, :author, :date_published, :description, :location, :links, :allows_remote "
                "WHERE NOT EXISTS(SELECT 1 FROM jobs WHERE title = :title AND author = :author)",
                {'title': curr_title,
                 'tags': curr_tags,
                 'author': curr_author,
                 'date_published': curr_date,
                 'description': curr_description,
                 'location': curr_location,
                 'links': curr_links,
                 'allows_remote': curr_remote
                 })

    def exit_options(self):
        app.closeAllWindows()


class MainWindow(QMainWindow):
    def __init__(self):
        connection = sqlite3.connect('jobs.db')
        cursor = connection.cursor()
        QMainWindow.__init__(self)
        self.setMinimumSize(QSize(1600, 900))
        self.setWindowTitle("DB Viewer")
        self.db_table = QTableWidget(self)
        self.db_table.setRowCount(1000)
        self.db_table.setColumnCount(8)
        self.db_table.move(0, 25)
        self.db_table.resize(1600, 900)
        self.db_table.setHorizontalHeaderLabels(["Titles", "Tags", "Author", "Date Published", "Description",
                                                "Location", "Links", "Allows Remote"])
        job_list = self.create_entries(cursor)
        self.db_table.cellDoubleClicked.connect(self.open_entry)
        self.entry_window = EntryWindow()

        self.menu_bar = self.menuBar()
        self.file_menu = self.menu_bar.addMenu('File')
        exit_button = QAction('Exit', self)
        exit_button.triggered.connect(self.exit_action)
        self.file_menu.addAction(exit_button)

        self.search_menu = self.menu_bar.addMenu('Search')
        search_button = QAction('Search', self)
        search_button.triggered.connect(self.search_action)
        self.search_window = SearchWindow(job_list)
        self.search_menu.addAction(search_button)

    def exit_action(self):
        self.close()

    def search_action(self):
        self.search_window.show()

    def open_entry(self, row, column):
        for i in reversed(range(self.entry_window.layout.count())):
            self.entry_window.layout.itemAt(i).widget().setParent(None)
        cell = self.db_table.item(row, 0)
        job_title = cell.text()
        window_title = str(job_title)
        self.entry_window.setWindowTitle(window_title)

        title_label = QLabel()
        title_label.setText("<strong> %s" % window_title)
        title_label.setAlignment(Qt.AlignLeft)
        self.entry_window.layout.addWidget(title_label)

        tag_label = QLabel()
        tag_label.setText("%s" % self.db_table.item(row, 1).text())
        self.entry_window.layout.addWidget(tag_label)

        author_label = QLabel()
        author_label.setText("%s" % self.db_table.item(row, 2).text())
        self.entry_window.layout.addWidget(author_label)

        time_label = QLabel()
        time_label.setText("%s" % self.db_table.item(row, 3).text())
        self.entry_window.layout.addWidget(time_label)

        location_label = QLabel()
        location_label.setText("%s" % self.db_table.item(row, 5).text())
        self.entry_window.layout.addWidget(location_label)

        links_label = QLabel()
        links_label.setText("%s" % self.db_table.item(row, 6).text())
        self.entry_window.layout.addWidget(links_label)

        remote_label = QLabel()
        if self.db_table.item(row, 7).text() == "Yes":
            remote_label.setText("Allows remote")
        else:
            remote_label.setText("Does not allow remote")
        self.entry_window.layout.addWidget(remote_label)

        description_label = QLabel()
        description_label.setText("%s" % self.db_table.item(row, 4).text())
        description_scroll = QScrollArea()
        description_scroll.setWidget(description_label)
        self.entry_window.layout.addWidget(description_scroll)

        self.entry_window.show()

    def create_entries(self, cursor):
        entry_list = []
        cursor.execute("""SELECT COUNT(*) FROM jobs""")
        result = cursor.fetchone()
        entries_length = int(result[0])
        titles = cursor.execute("""SELECT title FROM jobs""")
        titles_list = titles.fetchall()
        tags = cursor.execute("""SELECT tags FROM jobs""")
        tags_list = tags.fetchall()
        authors = cursor.execute("""SELECT author FROM jobs""")
        author_list = authors.fetchall()
        dates = cursor.execute("""SELECT date_published FROM jobs""")
        date_list = dates.fetchall()
        descriptions = cursor.execute("""SELECT description FROM jobs""")
        description_list = descriptions.fetchall()
        locations = cursor.execute("""SELECT location FROM jobs""")
        location_list = locations.fetchall()
        links = cursor.execute("""SELECT links FROM jobs""")
        links_list = links.fetchall()
        remotes = cursor.execute("""SELECT allows_remote FROM jobs""")
        remote_list = remotes.fetchall()
        for entry in range(entries_length):
            job_entry = JobEntry()
            entry_list.append(job_entry)

            job_entry.set_title(titles_list[entry][0])

            curr_tag = str(tags_list[entry])
            if curr_tag == "('none',)":
                job_entry.set_tags("None")
            else:
                output = re.findall(r"'term': '(.*?)'", curr_tag)
                final_string = ""
                for i in range(len(output)):
                    final_string += output[i]
                    final_string += ", "
                final_string = final_string[:-2]
                job_entry.set_tags(final_string)

            job_entry.set_author(author_list[entry][0])

            job_entry.set_date(date_list[entry][0])

            curr_description = QTextEdit()
            curr_description.setText(str(description_list[entry]))
            final_description = curr_description.toPlainText()
            final_description = final_description[3:-3]
            job_entry.set_description(final_description)

            location_string = str(location_list[entry])
            location_string = location_string[2:-3]
            if location_string == "None":
                job_entry.set_city("None")
                job_entry.set_state('')
            elif ',' in location_string:
                location_split = location_string.split(',')
                job_entry.set_city(location_split[0])
                job_entry.set_state(location_split[1])
            else:
                job_entry.set_city(location_string)
                job_entry.set_state('')

            curr_link = str(links_list[entry])
            link_text = re.findall(r"'href': '(.*?)'", curr_link)
            job_entry.set_links(link_text)

            job_entry.set_remote(remote_list[entry][0])

        self.fill_table(entry_list)
        return entry_list

    def fill_table(self, entry_list):
        self.db_table.setColumnWidth(0, 500)
        self.db_table.setColumnWidth(1, 500)
        self.db_table.setColumnWidth(4, 225)
        increment_row = 0
        for entry in entry_list:
            self.db_table.setItem(increment_row, 0, QTableWidgetItem(entry.title))
            self.db_table.setItem(increment_row, 1, QTableWidgetItem(entry.tags))
            self.db_table.setItem(increment_row, 2, QTableWidgetItem(entry.author))
            self.db_table.setItem(increment_row, 3, QTableWidgetItem(entry.date_published))
            self.db_table.setItem(increment_row, 4, QTableWidgetItem(entry.description))
            self.db_table.setItem(increment_row, 5, QTableWidgetItem(entry.city + ", " + entry.state))
            for link in entry.links:
                self.db_table.setItem(increment_row, 6, QTableWidgetItem(link))
            self.db_table.setItem(increment_row, 7, QTableWidgetItem(entry.allows_remote))
            increment_row += 1


class EntryWindow(QWidget):
    def __init__(self):
        super(EntryWindow, self).__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)


class SearchWindow(QWidget):
    def __init__(self, job_list):
        super(SearchWindow, self).__init__()
        self.job_list = job_list
        self.setWindowTitle('Search')
        self.layout = QVBoxLayout()

        self.instructions = QLabel()
        self.instructions.setText("Separate search items by commas")
        self.layout.addWidget(self.instructions)

        self.titles_to_search = QLineEdit()
        self.titles_to_search.setPlaceholderText("Titles")
        self.layout.addWidget(self.titles_to_search)

        self.tags_to_search = QLineEdit()
        self.tags_to_search.setPlaceholderText("Tags")
        self.layout.addWidget(self.tags_to_search)

        self.authors_to_search = QLineEdit()
        self.authors_to_search.setPlaceholderText("Authors")
        self.layout.addWidget(self.authors_to_search)

        self.cities_to_search = QLineEdit()
        self.cities_to_search.setPlaceholderText("Cities")
        self.layout.addWidget(self.cities_to_search)

        self.states_to_search = QLineEdit()
        self.states_to_search.setPlaceholderText("States or Country if outside of US (I.E. MA)")
        self.layout.addWidget(self.states_to_search)

        self.remote_to_search = QCheckBox()
        self.remote_to_search.setText("Allows remote? (leave unchecked for either)")
        self.layout.addWidget(self.remote_to_search)

        self.search_for_all = QCheckBox()
        self.search_for_all.setText("LEAVE UNCHECKED ran out of time")
        self.layout.addWidget(self.search_for_all)

        self.search_button = QPushButton()
        self.search_button.setText("Search")
        self.search_button.clicked.connect(self.search)
        self.layout.addWidget(self.search_button)

        self.setLayout(self.layout)

    def search(self):

        titles_string = self.titles_to_search.text().lower()
        titles_list = [title.strip() for title in titles_string.split(',')]

        tags_string = self.tags_to_search.text().lower()
        tags_list = [tag.strip() for tag in tags_string.split(',')]

        authors_string = self.authors_to_search.text().lower()
        authors_list = [authors.strip() for authors in authors_string.split(',')]

        cities_string = self.cities_to_search.text().lower()
        cities_list = [cities.strip() for cities in cities_string.split(',')]

        states_string = self.states_to_search.text().lower()
        states_list = [states.strip() for states in states_string.split(',')]

        if self.search_for_all.isChecked():
            None
        else:
            search_list = []
            for entry in self.job_list:
                if str(titles_list) != "['']":
                    for title in titles_list:
                        if title in entry.title.lower():
                            if entry not in search_list:
                                search_list.append(entry)
                if str(tags_list) != "['']":
                    for tag in tags_list:
                        if tag in entry.tags.lower():
                            if entry not in search_list:
                                search_list.append(entry)
                if str(authors_list) != "['']":
                    for author in authors_list:
                        if author in entry.author.lower():
                            if entry not in search_list:
                                search_list.append(entry)
                if str(cities_list) != "['']":
                    for city in cities_list:
                        if city in entry.city.lower():
                            if entry not in search_list:
                                search_list.append(entry)
                if str(states_list) != "['']":
                    for state in states_list:
                        if state in entry.state.lower():
                            if entry not in search_list:
                                search_list.append(entry)
                if self.remote_to_search.isChecked():
                    if entry.allows_remote:
                        if entry not in search_list:
                            search_list.append(entry)
            self.results_table = SearchTable()
            self.show_table()
            self.results_table.fill_table(search_list)

    def show_table(self):
        self.results_table.show()




class JobEntry:
    def __init__(self):
        self.title = None
        self.tags = None
        self.author = None
        self.date_published = None
        self.description = None
        self.city = None
        self.state = None
        self.links = None
        self.allows_remote = None

    def set_title(self, title):
        self.title = title

    def set_tags(self, tags):
        self.tags = tags

    def set_author(self, author):
        self.author = author

    def set_date(self, date_published):
        self.date_published = date_published

    def set_description(self, description):
        self.description = description

    def set_city(self, city):
        self.city = city

    def set_state(self, state):
        self.state = state

    def set_links(self, links):
        self.links = links

    def set_remote(self, allows_remote):
        self.allows_remote = allows_remote


class SearchTable(QWidget):
    def __init__(self):
        super(SearchTable, self).__init__()
        self.layout = QVBoxLayout()
        self.table = QTableWidget()
        self.layout.addWidget(self.table)
        self.setLayout(self.layout)
        self.setup_table()
        self.setMinimumSize(800,400)

    def setup_table(self):
        self.table.setColumnCount(8)
        self.table.setHorizontalHeaderLabels(["Titles", "Tags", "Author", "Date Published", "Description",
                                              "Location", "Links", "Allows Remote"])
        self.table.setColumnWidth(0, 500)
        self.table.setColumnWidth(1, 500)
        self.table.setColumnWidth(4, 225)

    def fill_table(self, search_list):
        self.table.setRowCount(len(search_list))
        increment_row = 0
        for entry in search_list:
            self.table.setItem(increment_row, 0, QTableWidgetItem(entry.title))
            self.table.setItem(increment_row, 1, QTableWidgetItem(entry.tags))
            self.table.setItem(increment_row, 2, QTableWidgetItem(entry.author))
            self.table.setItem(increment_row, 3, QTableWidgetItem(entry.date_published))
            self.table.setItem(increment_row, 4, QTableWidgetItem(entry.description))
            self.table.setItem(increment_row, 5, QTableWidgetItem(entry.city + ", " + entry.state))
            for link in entry.links:
                self.table.setItem(increment_row, 6, QTableWidgetItem(link))
            self.table.setItem(increment_row, 7, QTableWidgetItem(entry.allows_remote))
            increment_row += 1


if __name__ == "__main__":
    app = QApplication(sys.argv)
    start_window = LoadOptions()
    start_window.show()
    app.exec_()
    main_app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(main_app.exec_())

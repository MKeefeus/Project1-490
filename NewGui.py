import sys
import sqlite3
import feedparser
from PyQt5.QtWidgets import *
from PyQt5.QtCore import QSize


class LoadOptions(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)

        self.setMinimumSize(QSize(300, 200))
        self.setWindowTitle("Load options")

        refresh_button = QPushButton('Clear and reload database', self)
        refresh_button.clicked.connect(self.refresh)
        refresh_button.resize(200, 32)
        refresh_button.move(50, 50)

        load_button = QPushButton('Load database', self)
        load_button.clicked.connect(self.load)
        load_button.resize(200, 32)
        load_button.move(50, 90)

        update_button = QPushButton('Update database', self)
        update_button.clicked.connect(self.update)
        update_button.resize(200, 32)
        update_button.move(50, 130)

    def update(self):
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
                curr_title = "none"
            if 'tags' in feed['entries'][x]:
                curr_tags = ' '.join(str(e) for e in feed['entries'][x]['tags'])
            else:
                curr_tags = "none"
            if 'author' in feed['entries'][x]:
                curr_author = feed['entries'][x]['author']
            else:
                curr_author = "none"
            if 'published' in feed['entries'][x]:
                curr_date = feed['entries'][x]['published']
            else:
                curr_date = "none"
            if 'summary' in feed['entries'][x]:
                curr_description = feed['entries'][x]['summary']
            else:
                curr_description = "none"
            if 'location' in feed['entries'][x]:
                curr_location = feed['entries'][x]['location']
            else:
                curr_location = "none"
            if 'links' in feed['entries'][x]:
                curr_links = ' '.join(str(e) for e in feed['entries'][x]['links'])
            else:
                curr_links = "none"
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
                curr_title = "none"
            if 'tags' in feed['entries'][x]:
                curr_tags = ' '.join(str(e) for e in feed['entries'][x]['tags'])
            else:
                curr_tags = "none"
            if 'author' in feed['entries'][x]:
                curr_author = feed['entries'][x]['author']
            else:
                curr_author = "none"
            if 'published' in feed['entries'][x]:
                curr_date = feed['entries'][x]['published']
            else:
                curr_date = "none"
            if 'summary' in feed['entries'][x]:
                curr_description = feed['entries'][x]['summary']
            else:
                curr_description = "none"
            if 'location' in feed['entries'][x]:
                curr_location = feed['entries'][x]['location']
            else:
                curr_location = "none"
            if 'links' in feed['entries'][x]:
                curr_links = ' '.join(str(e) for e in feed['entries'][x]['links'])
            else:
                curr_links = "none"
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
        self.db_table.move(0, 0)
        self.db_table.resize(1600, 900)
        self.fill_table(cursor)

    def fill_table(self, cursor):
        titles = cursor.execute("""SELECT title FROM jobs""")
        increment_row = 0
        for title in titles:
            curr_title = title[0]
            self.db_table.setItem(increment_row, 0, QTableWidgetItem(curr_title))
            increment_row += 1
        self.db_table.setColumnWidth(0, 500)
        increment_row = 0
        tags = cursor.execute("""SELECT tags FROM jobs""")
        for tag in tags:
            curr_tag = tag[0]
            self.db_table.setItem(increment_row, 1, QTableWidgetItem(curr_tag))
            increment_row += 1
        self.db_table.setColumnWidth(1, 500)
        increment_row = 0
        authors = cursor.execute("""SELECT author FROM jobs""")
        for author in authors:
            curr_author = author[0]
            self.db_table.setItem(increment_row, 2, QTableWidgetItem(curr_author))
            increment_row += 1
        increment_row = 0
        dates = cursor.execute("""SELECT date_published FROM jobs""")
        for date in dates:
            curr_date = date[0]
            self.db_table.setItem(increment_row, 3, QTableWidgetItem(curr_date))
            increment_row += 1
        increment_row = 0
        descriptions = cursor.execute("""SELECT description FROM jobs""")
        for description in descriptions:
            curr_description = description[0]
            self.db_table.setItem(increment_row, 4, QTableWidgetItem(curr_description))
            increment_row += 1
        increment_row = 0
        locations = cursor.execute("""SELECT location FROM jobs""")
        for location in locations:
            curr_location = location[0]
            self.db_table.setItem(increment_row, 5, QTableWidgetItem(curr_location))
            increment_row += 1
        increment_row = 0
        links = cursor.execute("""SELECT links FROM jobs""")
        for link in links:
            curr_link = link[0]
            self.db_table.setItem(increment_row, 6, QTableWidgetItem(curr_link))
            increment_row += 1
        increment_row = 0
        remotes = cursor.execute("""SELECT allows_remote FROM jobs""")
        for remote in remotes:
            curr_remote = remote[0]
            self.db_table.setItem(increment_row, 7, QTableWidgetItem(curr_remote))
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

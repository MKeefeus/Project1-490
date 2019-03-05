import sqlite3
import feedparser


def main():
    conn = sqlite3.connect('jobs.db')
    c = conn.cursor()
    create_db(c)
    populate_db(c)
    conn.commit()
    conn.close()
    #save me


def create_db(c):
    c.execute("""DROP TABLE IF EXISTS jobs""")
    c.execute("""CREATE TABLE IF NOT EXISTS jobs(
                title text,
                tags text,
                author text,
                date_published text,
                description text,
                location text,
                links text,
                allows_remote text
                )""")


def populate_db(c):
    feed = feedparser.parse("https://stackoverflow.com/jobs/feed")
    length = len(feed['entries'])
    for x in range(length):
        if 'title' in feed['entries'][x]:
            currTitle = feed['entries'][x]['title']
            if currTitle.find("allows remote") != -1:
                currRemote = "yes"
            else:
                currRemote = "no"
        else:
            currTitle = "none"
        if 'tags' in feed['entries'][x]:
            currTags = ' '.join(str(e) for e in feed['entries'][x]['tags'])
        else:
            currTags = "none"
        if 'author' in feed['entries'][x]:
            currAuthor = feed['entries'][x]['author']
        else:
            currAuthor = "none"
        if 'published' in feed['entries'][x]:
            currDate = feed['entries'][x]['published']
        else:
            currDate = "none"
        if 'summary' in feed['entries'][x]:
            currDescription = feed['entries'][x]['summary']
        else:
            currDescription = "none"
        if 'location' in feed['entries'][x]:
            currLocation = feed['entries'][x]['location']
        else:
            currLocation = "none"
        if 'links' in feed['entries'][x]:
            currLinks = ' '.join(str(e) for e in feed['entries'][x]['links'])
        else:
            currLinks = "none"
        c.execute("INSERT INTO jobs VALUES (:title, :tags, :author, :date_published, :description, :location, :links, :allows_remote)",
                    {'title': currTitle,
                    'tags': currTags,
                    'author': currAuthor,
                    'date_published': currDate,
                    'description': currDescription,
                    'location': currLocation,
                    'links': currLinks,
                    'allows_remote': currRemote
                    })


main()

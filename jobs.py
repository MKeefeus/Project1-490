class Job:

    def __init__(self, title, tags, author, date, description, location, links):
        self.title = title
        self.tags = tags
        self.author = author
        self.date = date
        self.description = description
        self.location = location
        self.links = links

    def __reper__(self):
        return "Job('{}', '{}', '{}', '{}', '{}', '{}' '{}' '{}')".format(
            self.title, self.tags, self.author,
            self.date, self.description, self.location,
            self.links)
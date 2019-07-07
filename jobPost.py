class JobPost:
    def __init__(self, d):
        self.commitment = d["categories"]["commitment"] if "commitment" in d["categories"] else ""
        self.department = d["categories"]["department"] if "department" in d["categories"] else ""
        self.location = d["categories"]["location"] if "location" in d["categories"] else ""
        self.team = d["categories"]["team"] if "team" in d["categories"] else ""
        self.title = d["text"] if "text" in d else ""
        self.applyUrl = d["applyUrl"] if "applyUrl" in d else ""

    def __str__(self):
        return self.title
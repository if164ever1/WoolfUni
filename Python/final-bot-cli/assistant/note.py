class Note:
    def __init__(self, text, tags=None):
        self.text = text
        if tags:
            self.tags = tags
        else:
            self.tags = text.lower().split()

    def edit(self, new_text):
        self.text = new_text

    def add_tag(self, tag):
        if tag not in self.tags:
            self.tags.append(tag)

    def __str__(self):
        tags_str = ', '.join(self.tags) if self.tags else "No tags"
        return f"📝 {self.text} [{tags_str}]"

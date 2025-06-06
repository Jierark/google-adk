from pydantic import BaseModel

class news_article(BaseModel):
    title: str
    author: str
    description: str
    url: str

    def __str__(self):
        return f"""
        Title: {self.title}
        Author: {self.author}
        Description: {self.description}
        Url: {self.url}
        """
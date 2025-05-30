from pydantic import BaseModel

class news_article(BaseModel):
    title: str
    author: str
    description: str
    url: str

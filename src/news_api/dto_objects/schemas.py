from pydantic import BaseModel


class NewsDTO(BaseModel):
    id: int
    company: str
    title: str
    description: str
    url: str
    img_url: str
    published_at: str

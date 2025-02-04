from fastapi import APIRouter
from src.news_api.news_controller import NewsController

router = APIRouter(
    prefix="/news",
    tags=["News"]
)

news_controller = NewsController()


@router.get('/company')
async def get_news_by_query(query: str):
    print('query', query)
    news = await news_controller.get_news_by_query_from_db(query)
    return news


# @router.get('/')
# async def get_all_news():
#     news  = await news_controller.get_all_news()
#     return news

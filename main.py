from wsgiref.util import request_uri

import uvicorn
from fastapi import FastAPI, Request
from pydantic import BaseModel


app = FastAPI(
    title="rest api traine",
    redoc_url=None,
    docs_url="/docs",

)


class UrlRequest(BaseModel):
    url: str


@app.post("/", status_code=201)
async def shorten_url(url_request: UrlRequest, request: Request):
    request_url = url_request.url
    shortening_url = request_url[:30]

    # Получаем название метода и путь обращения
    method = request.method
    path = request.url.path
    return {'Shortening URL': method + " " + path }
    #return {'Shortening URL': shortening_url}


@app.get("/{shortened_id}", status_code=307)
async def get_original_url(shortened_id: int, request: Request):
    # Получаем схему (http или https) и хост (домен)
    scheme = request.url.scheme
    host = request.url.hostname

    # Формируем полный URL
    full_url = f"{scheme}://{host}/{shortened_id}"

    return {"Location": full_url}

if __name__ == '__main__':
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)


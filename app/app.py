import uvicorn
from fastapi import FastAPI, Request, Depends
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError
from pydantic import BaseModel

app = FastAPI()
port = 5000
host = "localhost"


class CsrfSettings(BaseModel):
  secret_key:str = 'secret_you_definitely_keep_encrypted_in_config'

@CsrfProtect.load_config
def get_csrf_config():
  return CsrfSettings()

@app.get('/', response_class=HTMLResponse)
def get(request: Request, csrf_protect:CsrfProtect = Depends()):
  """
  Return the base HTML page
  """
  csrf_token = csrf_protect.generate_csrf()
  html_content=f"""
    <!DOCTYPE html>
    <html lang="en">
    <meta name="csrf_token" value="{csrf_token}">
    <head>
        <title>FastAPI CSRF Protect Example</title>
    </head>
    <body>
        <h1>FastAPI CSRF Protect Example</h1>
        <p>Check my meta values in the page source to find my csrf token!</p>
        <p>Use this value to set the X-CSRF-Token on the header of any POST to this server</p>
    </body>
    </html>
  """
  response = HTMLResponse(content=html_content, status_code=200)
  return response


@app.post('/posts', response_class=JSONResponse)
def create_post(request: Request, csrf_protect:CsrfProtect = Depends()):
  """
  Creates a new Post
  """
  csrf_token = csrf_protect.get_csrf_from_headers(request.headers)
  csrf_protect.validate_csrf(csrf_token)
  return JSONResponse({"message":"Received request"})

@app.exception_handler(CsrfProtectError)
def csrf_protect_exception_handler(request: Request, exc: CsrfProtectError):
  return JSONResponse(
    status_code=exc.status_code,
      content={ 'detail':  exc.message
    }
  )


if __name__ == "__main__":
    uvicorn.run("app:app", host=host, port=port, log_level="info")
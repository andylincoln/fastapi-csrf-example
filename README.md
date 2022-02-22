# fastapi-csrf-example
Exploration in adding CSRF protections to APIs with FastAPI and `fastapi-csrf-protect` library


## Getting started
Using Python 3.9 and Poetry for dependency management.

```sh
poetry install && poetry shell
```
Once in the poetry shell, you can run `python` with the dependencies.
To start the server: 

```sh
python app/app.py
```

Go to `127.0.0.1:5000`

Using `View Source` or `Inspect element` you should see the CSRF token be dropped in the `<head>` of the page in a `<meta>` tag.
Use that value to POST to `/posts`. You should see a success message in JSON attached to a response with HTTP 200 status.

```json
{
    "message": "Received request"
}
```


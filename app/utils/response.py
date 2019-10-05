import json

from flask import Response


def response(content: any, status: int, headers: dict = None) -> Response:
    if not headers:
        headers = [('Content-Type', 'application/json')]

    if isinstance(content, str):
        content = json.dumps({'message': content})

    if isinstance(content, dict) or isinstance(content, list):
        content = json.dumps(content)

    if isinstance(headers, dict):
        headers = [(name, value) for (name, value) in headers.items()]

    return Response(response=content, status=status, headers=headers)

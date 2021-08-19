from common import Controller
from requests import get as http_get
from common.http_responses import Response, UnauthorizedResponse, NotFoundResponse, InternalServerErrorResponse
import config
import http

class GitHubFileController(Controller):
    
    URL_TEMPLATE = 'https://raw.githubusercontent.com/{owner}/{repo}/master/{path}'

    def __init__(self, logger, access_token):
        super().__init__(logger)
        self._access_token = access_token
    
    def get(self, repo, path):
        if repo not in config.WhitelistedRepo:
            return UnauthorizedResponse(f'{repo} is not accessible.')
        url = self.URL_TEMPLATE.format(owner=config.RepoOwner, repo=repo, path=path)
        res = http_get(url, headers={'Authorization': f'token {self._access_token}'})
        if res.status_code == http.HTTPStatus.NOT_FOUND:
            return NotFoundResponse()
        if res.status_code != http.HTTPStatus.OK:
            return InternalServerErrorResponse()
        return Response(res.content, headers={
            'Content-Type': res.headers['Content-Type'],
            'Cache-Control': 'max-age=300'
        })
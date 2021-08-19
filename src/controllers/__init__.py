from common import Controller
from common.http_responses import Response, UnauthorizedResponse, InternalServerErrorResponse, NotFoundResponse
from common.utils import decode_base64, string_to_bytes
from github import Github, UnknownObjectException
import config
import http

class GitHubFileController(Controller):
    
    def __init__(self, logger, access_token):
        super().__init__(logger)
        self.g = Github(access_token)
    
    def get(self, repo, path):
        if repo not in config.WhitelistedRepo:
            return UnauthorizedResponse(f'{repo} is not accessible.')
        user = self.g.get_user(config.RepoOwner)
        repo = user.get_repo(repo)
        try:
            f = repo.get_contents(path)
        except UnknownObjectException as e:
            if e.status == http.HTTPStatus.NOT_FOUND:
                return NotFoundResponse()
            return InternalServerErrorResponse()
        content = string_to_bytes(f.content)
        return Response(decode_base64(content))
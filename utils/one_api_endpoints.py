from .request_handler import OneApiConfig

LIMIT = 20


class OneApi(OneApiConfig):

    def get_characters(self, page: str, limit: str) -> dict:
        limit = limit if limit != None else LIMIT
        page = page if page != None else 1
        return self.handle_request("GET", self.parse_url(f"character?page={page}&limit={limit}"))

    def get_single_character(self, _id: str):
        return self.handle_request("GET", self.parse_url(f"character/{_id}"))

    def get_qoute(self, character_id: str, page: str, limit: str) -> dict:
        limit = limit if limit != None else LIMIT
        page = page if page != None else 1
        return self.handle_request("GET", self.parse_url(f"character/{character_id}/quote?page={page}&limit={limit}"))

    def get_single_quote(self, _id: str):
        return self.handle_request("GET", self.parse_url(f"quote/{_id}"))

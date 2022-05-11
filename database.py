import json
from model import OneFinalAudienceResult


class Database:
    def __init__(self, base_path: str) -> None:
        self.base_path = base_path
        self.base_init_value = '{"faculty":[],"winners":[], "audience": []}'

    def create_faculty(self, faculty: list[str]):
        data = self.base_init_value
        with open(self.base_path, "r") as f:
            data = f.read()
        data = json.loads(data)
        data['faculty'] = faculty
        with open(self.base_path, "w") as f:
            f.write(json.dumps(data))

    def get_faculty(self) -> list[str]:
        data = None
        with open(self.base_path, "r") as f:
            data = f.read()
        data = json.loads(data)
        return data['faculty']

    def create_winners(self, winners: list[str]):
        data = self.base_init_value
        with open(self.base_path, "r") as f:
            data = f.read()
        data = json.loads(data)
        data['winners'] = winners
        with open(self.base_path, "w") as f:
            f.write(json.dumps(data))

    def get_winners(self) -> list[str]:
        data = None
        with open(self.base_path, "r") as f:
            data = f.read()
        data = json.loads(data)
        return data['winners']

    def create_audience(self, audience: list[OneFinalAudienceResult]):
        data = self.base_init_value
        with open(self.base_path, "r") as f:
            data = f.read()
        data = json.loads(data)
        tmp = []
        for a in audience:
            a_json = a.dict()
            tmp.append(a_json)
        data['audience'] = tmp
        with open(self.base_path, "w") as f:
            f.write(json.dumps(data))

    def get_audience(self) -> list[OneFinalAudienceResult]:
        data = None
        with open(self.base_path, "r") as f:
            data = f.read()
        data = json.loads(data)
        print(data['audience'])
        return data['audience']

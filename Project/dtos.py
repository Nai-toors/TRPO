'''DTO (Data Transfer Object) — это простой объект, который используется для передачи данных между различными частями приложения'''

class LocationDTO:
    def __init__(self, id=None, address=None):
        self.id = id
        self.address = address

class CastingDTO:
    def __init__(self, id=None, title=None, actors=None, address=None, time=None):
        self.id = id
        self.title = title
        self.actors = actors
        self.address = address
        self.time = time

class PlanDTO:
    def __init__(self, id=None, title=None, description=None, start_date=None, end_date=None):
        self.id = id
        self.title = title
        self.description = description
        self.start_date = start_date
        self.end_date = end_date

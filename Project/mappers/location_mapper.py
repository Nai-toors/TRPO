from models import db, Location
from dtos import LocationDTO  # Подключение DTO

class LocationMapper:
    def _to_dto(self, location):
        """Преобразует ORM-объект Location в DTO."""
        if not location:
            return None
        return LocationDTO(id=location.id, address=location.address)

    def get_all(self):
        """Возвращает список всех локаций в виде DTO."""
        orm_locations = Location.query.all()
        return [self._to_dto(location) for location in orm_locations]

    def find_by_id(self, location_id):
        """Ищет локацию по ID и возвращает DTO."""
        orm_location = Location.query.get(location_id)
        return self._to_dto(orm_location)

    def insert(self, location_dto):
        """Добавляет новую локацию в базу данных, принимая DTO."""
        new_location = Location(address=location_dto.address)
        db.session.add(new_location)
        db.session.commit()
        return self._to_dto(new_location)

    def delete(self, location_dto):
        """Удаляет локацию по объекту DTO."""
        if location_dto.id is None:
            raise ValueError("ID в DTO отсутствует, невозможно удалить объект.")
        location = Location.query.get(location_dto.id)
        if location:
            db.session.delete(location)
            db.session.commit()


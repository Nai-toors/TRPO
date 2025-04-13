from models import db, Casting
from dtos import CastingDTO

class CastingMapper:
    """
    Маппер для работы с таблицей castings.
    """

    def _to_dto(self, casting):
        """Преобразует ORM-объект Casting в DTO."""
        if not casting:
            return None
        return CastingDTO(
            id=casting.id,
            title=casting.title,
            actors=casting.actors,
            address=casting.address,
            time=casting.time
        )

    def get_all(self):
        """Возвращает список всех кастингов в виде DTO."""
        orm_castings = Casting.query.all()
        return [self._to_dto(casting) for casting in orm_castings]

    def find_by_id(self, casting_id):
        """Ищет кастинг по ID и возвращает DTO."""
        orm_casting = Casting.query.get(casting_id)
        return self._to_dto(orm_casting)

    def insert(self, casting_dto):
        """Добавляет новый кастинг в базу данных."""
        new_casting = Casting(
            title=casting_dto.title,
            actors=casting_dto.actors,
            address=casting_dto.address,
            time=casting_dto.time
        )
        db.session.add(new_casting)
        db.session.commit()
        return self._to_dto(new_casting)

    def delete(self, casting_dto):
        """Удаляет кастинг по объекту DTO."""
        if casting_dto.id is None:
            raise ValueError("ID в DTO отсутствует, невозможно удалить объект.")
        casting = Casting.query.get(casting_dto.id)
        if casting:
            db.session.delete(casting)
            db.session.commit()


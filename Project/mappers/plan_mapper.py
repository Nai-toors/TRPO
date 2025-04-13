from models import db, Plan
from dtos import PlanDTO

class PlanMapper:
    """
    Маппер для работы с таблицей plans.
    """

    def _to_dto(self, plan):
        """Преобразует ORM-объект Plan в DTO."""
        if not plan:
            return None
        return PlanDTO(
            id=plan.id,
            title=plan.title,
            description=plan.description,
            start_date=plan.start_date,
            end_date=plan.end_date
        )

    def get_all(self):
        """Возвращает список всех съёмочных планов в виде DTO."""
        orm_plans = Plan.query.all()
        return [self._to_dto(plan) for plan in orm_plans]

    def find_by_id(self, plan_id):
        """Ищет съёмочный план по ID и возвращает DTO."""
        orm_plan = Plan.query.get(plan_id)
        return self._to_dto(orm_plan)

    def insert(self, plan_dto):
        """Добавляет новый съёмочный план в базу данных."""
        new_plan = Plan(
            title=plan_dto.title,
            description=plan_dto.description,
            start_date=plan_dto.start_date,
            end_date=plan_dto.end_date
        )
        db.session.add(new_plan)
        db.session.commit()
        return self._to_dto(new_plan)

    def delete(self, plan_dto):
        """Удаляет съёмочный план по объекту DTO."""
        if plan_dto.id is None:
            raise ValueError("ID в DTO отсутствует, невозможно удалить объект.")
        plan = Plan.query.get(plan_dto.id)
        if plan:
            db.session.delete(plan)
            db.session.commit()


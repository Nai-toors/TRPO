from flask import Flask, render_template, request, redirect, url_for
from models import db
from mappers.location_mapper import LocationMapper
from mappers.casting_mapper import CastingMapper
from mappers.plan_mapper import PlanMapper
from dtos import LocationDTO, CastingDTO, PlanDTO

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  # Подключение к SQLite базе данных
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False             # Отключение уведомлений об изменениях SQLAlchemy
db.init_app(app)                                                 # Инициализация базы данных

# Инициализация мапперов
location_mapper = LocationMapper()
casting_mapper = CastingMapper()
plan_mapper = PlanMapper()


@app.route('/')
def index():
    """Главная страница."""
    return render_template('plans.html')


# Обработчики для локаций
@app.route('/locations', methods=['GET', 'POST'])
def locations():
    """Страница для просмотра и добавления локаций."""
    if request.method == 'POST':
        address = request.form['address']
        location_dto = LocationDTO(address=address)
        location_mapper.insert(location_dto)
        return redirect(url_for('locations'))

    locations_dto = location_mapper.get_all()
    return render_template('locations.html', locations=locations_dto)


@app.route('/locations/<int:location_id>/delete', methods=['POST'])
def delete_location(location_id):
    """Удаляет локацию по объекту DTO."""
    location_dto = location_mapper.find_by_id(location_id)  # Получаем DTO
    if not location_dto:
        return "Локация не найдена", 404
    location_mapper.delete(location_dto)  # Удаляем через DTO
    return redirect(url_for('locations'))



@app.route('/locations/<int:location_id>/request', methods=['POST'])
def request_location(location_id):
    """Заглушка для запроса локации."""
    location_dto = location_mapper.find_by_id(location_id)
    if not location_dto:
        return "Локация не найдена", 404
    return f"Локация '{location_dto.address}' запрошена"


# Обработчики для кастингов
@app.route('/castings', methods=['GET', 'POST'])
def castings():
    """Страница для просмотра и добавления кастингов."""
    if request.method == 'POST':
        casting_dto = CastingDTO(
            title=request.form['title'],
            actors=request.form['actors'],
            address=request.form['address'],
            time=request.form['time']
        )
        casting_mapper.insert(casting_dto)
        return redirect(url_for('castings'))

    castings_dto = casting_mapper.get_all()
    return render_template('castings.html', castings=castings_dto)


@app.route('/castings/<int:casting_id>', methods=['GET'])
def casting_detail(casting_id):
    """Страница с деталями кастинга."""
    casting_dto = casting_mapper.find_by_id(casting_id)
    if not casting_dto:
        return "Кастинг не найден", 404
    return render_template('casting_detail.html', casting=casting_dto)


@app.route('/castings/<int:casting_id>/schedule', methods=['POST'])
def schedule_audition(casting_id):
    """Заглушка для назначения прослушивания."""
    casting_dto = casting_mapper.find_by_id(casting_id)
    if not casting_dto:
        return "Кастинг не найден", 404
    return f"Прослушивание для кастинга '{casting_dto.title}' назначено"


@app.route('/castings/<int:casting_id>/delete', methods=['POST'])
def delete_casting(casting_id):
    """Удаляет кастинг по объекту DTO."""
    casting_dto = casting_mapper.find_by_id(casting_id)  # Получаем DTO
    if not casting_dto:
        return "Кастинг не найден", 404
    casting_mapper.delete(casting_dto)  # Удаляем через DTO
    return redirect(url_for('castings'))



# Обработчики для съёмочных планов
@app.route('/plans', methods=['GET', 'POST'])
def plans():
    """Страница для просмотра и добавления съёмочных планов."""
    if request.method == 'POST':
        plan_dto = PlanDTO(
            title=request.form['title'],
            description=request.form['description'],
            start_date=request.form['start_date'],
            end_date=request.form['end_date']
        )
        plan_mapper.insert(plan_dto)
        return redirect(url_for('plans'))

    plans_dto = plan_mapper.get_all()
    return render_template('plans.html', plans=plans_dto)


@app.route('/plans/<int:plan_id>', methods=['GET'])
def plan_detail(plan_id):
    """Детали съёмочного плана."""
    plan_dto = plan_mapper.find_by_id(plan_id)
    if not plan_dto:
        return "План не найден", 404
    return render_template('plan_detail.html', plan=plan_dto)


@app.route('/plans/<int:plan_id>/delete', methods=['POST'])
def delete_plan(plan_id):
    """Удаляет съёмочный план по объекту DTO."""
    plan_dto = plan_mapper.find_by_id(plan_id)  # Получаем DTO
    if not plan_dto:
        return "План не найден", 404
    plan_mapper.delete(plan_dto)  # Удаляем через DTO
    return redirect(url_for('plans'))



if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Создание таблиц в базе данных при запуске приложения
    app.run(debug=True)

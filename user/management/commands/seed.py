import os
import django
from django.core.management.base import BaseCommand
from django_seed import Seed
from faker import Faker

from user.models import Employee
import random

MODE_REFRESH = 'refresh'
MODE_CLEAR = 'clear'

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website.settings")

django.setup()


class Command(BaseCommand):
    help = "Seed database for testing and development."

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        self.stdout.write('Seeding data...')
        run_seed(options['mode'])
        self.stdout.write('Done.')


def clear_data():
    """Deletes all the Employee data"""
    Employee.objects.all().delete()


def create_employee():
    """Creates an Employee object with random data and supervisor"""
    seeder = Seed.seeder()

    supervisor = None  # Начальник по умолчанию - None для корневого уровня иерархии

    if Employee.objects.exists():
        # Если уже есть сотрудники, выберите случайного начальника из них
        supervisor = Employee.objects.order_by('?').first()

    return {
        'full_name': lambda x: seeder.faker.name(),
        'position': lambda x: seeder.faker.job(),
        'hire_date': lambda x: seeder.faker.date_this_decade(),
        'email': lambda x: seeder.faker.email(),
        'supervisor': supervisor,
    }


def run_seed(mode):
    if mode == MODE_CLEAR:
        return

    fake = Faker()
    employees = []
    dct = []
    supervisors = []
    levels = [10, 500, 2500, 2500, 2500, 15000, 30000]
    # levels = [1, 2, 4, 8, 16]

    for level, num_employees in enumerate(levels, start=1):
        supervisor = None

        for i in range(num_employees):
            if level != 1:
                supervisor = random.choice(supervisors)

            # Генерация уникального имени пользователя
            username = f"{fake.user_name()}_{level}_{i}"

            employee = Employee.objects.create(
                full_name=fake.name(),
                position=fake.job(),
                hire_date=fake.date_of_birth(),
                email=fake.email(),
                supervisor=supervisor,
                level=level,
                username=username,
            )
            employees.append(employee)
            password = fake.password()
            employee.set_password(password)
            employee.save()
            print(f"Created user: {username}, Password: {password}")

        dct.append(employees)
        supervisors = employees
        employees = []
    # clear_data()

# def run_seed(mode):
#     """ Seed database based on mode
#     :param mode: refresh / clear
#     :return:
#     """
#     # Clear data from Employee table
#     clear_data()
#
#     if mode == MODE_CLEAR:
#         return
#
#     seeder = Seed.seeder()
#     # levels = [10, 500, 2500, 2500, 2500, 15000, 30000]
#     levels = [1, 2, 4, 8, 16]
#     employees = generate_hierarchy(levels)
#     seeder.add_entity(Employee, len(employees), *employees)
#     seeder.execute()
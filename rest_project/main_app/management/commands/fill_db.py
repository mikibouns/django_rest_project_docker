from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from subprocess import call
import os
import random
import re
from rest_framework.authtoken.models import Token

from product_app.models import Products
from basket_app.models import Basket, ProductList

User = get_user_model()


class Command(BaseCommand):
#---- Удаление и создание БД -------------------------------------------------------------------------------------------
    def create_db(self):
        '''создает базу данных и миграции'''
        try:
            call('python manage.py makemigrations && python manage.py migrate && python manage.py collectstatic', shell=True)
        except Exception as e:
            print(e)

    def files_searcher(self, tamplate):
        home_path = os.getcwd()
        pattern = re.compile(tamplate)
        for root, _, files in os.walk(home_path):
            depth = root.count('\\') - home_path.count('\\')
            for file in files:
                if pattern.findall(file) and depth <= 3:
                    yield os.path.join(root, file)
                else:
                    yield False

    def delete_db(self):
        '''удаляет базу данных и миграции'''
        pattern = [r'\d\d\d\d_\w+\.py', r'^\w+\.sqlite3$']
        for template in pattern:
            for file_path in self.files_searcher(template):
                if file_path:
                    print('{} is removed'.format(file_path))
                    os.remove(file_path)

#---- Заполнение БД ----------------------------------------------------------------------------------------------------

    def users_iterator(self):
        '''генератор создание пользователей'''
        FIOs = ['Иванов Иван Иванович',
                'Петров Петр Петрович',
                'Сидоров Сергей Федорович',
                'Путин Владимир Владимирович',
                'Пушкин Александр Сергеевич',
                'Пупкин Владимир Петрович']
        for i, name in enumerate(FIOs):
            username = 'email{}@mail.com'.format(i)
            user = get_user_model()(
                fio=name,
                address=username,
                username=username,
            )
            user.set_password('123')
            yield user

    def fill_products(self):
        '''заполнение таблицы Products'''
        roducts = ['Картофель', 'Капуста', 'Морковь', 'Помидоры', 'Огурцы', 'Чеснок', 'Лук', 'Свекла', 'Зелень',
                   'Яблоки']
        for prod in roducts:
            data = {'name': prod,
                    'art': random.randint(123000, 999999),
                    'price': random.uniform(10.50, 200.50),
                    'quantity': random.randint(0, 40)}

            Products.objects.create(**data)
        Products.objects.create(name='Малина', art=111111, price=325.50, quantity=100)

    def handle(self, *args, **options):
        '''Главный обработчик'''

        self.delete_db()
        self.create_db()

        User.objects.bulk_create(iter(self.users_iterator())) # создание пользователей

        # Создаем суперпользователя при помощи менеджера модели
        super_user = User.objects.create_superuser('administ', 'administ@mail.com', 'Testtest123', address='administ@mail.com')

        self.fill_products() # добавляем список продуктов

        # создаем токены для пользователей и корзины с продуктами
        for user in User.objects.all():
            Token.objects.create(user=user)
            basket = Basket.objects.create(user_id=user)
            if random.randint(0, 1):
                for prod in Products.objects.all():
                    if random.randint(0, 1):
                        ProductList.objects.create(basket=basket,
                                                   product=prod,
                                                   quantity=random.randint(1, 12))

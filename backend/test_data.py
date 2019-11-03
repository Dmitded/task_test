#!./env/bin/python

import falcon
from random import randint
from sqlalchemy.sql import func
from db.session import Session

from models.worker import *
from models.activity_log import ActivityLog


WORKERS = \
    {
        'ean13': [25, 24, 23, 22],
        'name': ['Иван', 'Андрей', 'Сергей', 'Федор'],
        'surname': ['Ванко', 'Джигаев', 'Савичев', 'Коростылев'],
        'middle_name': ['Иванович', 'Дмитриевич', 'Сергеевич', 'Артемович'],
        'type': ['INSPECTOR', 'COLLECTOR', 'COLLECTOR', 'COLLECTOR']
    }

inspector_data = ['ean13: ', '25', 'password: ']


def create_workers():

    for i in range(0, 4):
        # import pdb; pdb.set_trace()
        worker = Worker()
        worker.ean13 = WORKERS['ean13'][i]
        worker.password = Worker.generate_worker_password()
        worker.name = WORKERS['name'][i]
        worker.surname = WORKERS['surname'][i]
        worker.middle_name = WORKERS['middle_name'][i]
        worker.type = WORKERS['type'][i]

        try:
            worker.save()
            worker.db_session.commit()
        except Exception:
            falcon.HTTPUnprocessableEntity()

        if i == 0:
            inspector_data.append(str(worker.password))


def generate_box_index(box_code_index):
    rand = randint(1, 6000)

    if rand == box_code_index:
        generate_box_index(box_code_index)

    return rand


def create_activity_log():

    box_code_index = 1

    for i in range(1, 12):
        for j in range(1, 31):

            if i == 2 and j >= 28:
                continue

            for k in range(10, 19):

                activity_collector = ActivityLog()
                activity_inspector = ActivityLog()

                activity_collector.box_code = generate_box_index(box_code_index)
                box_code_index = activity_collector.box_code
                activity_collector.worker_id = randint(2, 4)
                activity_collector.payload = WORKERS['ean13'][activity_collector.worker_id - 1]
                activity_collector.type = 'COLLECT'
                activity_collector.status = 'SUCCESS'
                if i < 10 and j < 10:
                    date = '2019-0{0}-0{1}'.format(i, j)
                elif i < 10 and j > 9:
                    date = '2019-0{0}-{1}'.format(i, j)
                elif i > 9 and j < 10:
                    date = '2019-{0}-0{1}'.format(i, j)
                time = '{0}:55:'.format(k) + str(randint(10, 59))
                activity_collector.local_time = date + ' ' + time
                activity_collector.server_time = date + ' ' + '{0}:55:00'.format(k)
                try:
                    activity_collector.save()
                    activity_collector.db_session.commit()
                except Exception:
                    falcon.HTTPUnprocessableEntity()

                activity_inspector.box_code = box_code_index
                activity_inspector.worker_id = 1
                activity_inspector.payload = randint(30, 80)
                activity_inspector.type = 'REVIEW'
                activity_inspector.status = 'SUCCESS'
                activity_inspector.local_time = date + ' ' + \
                    '{0}:00:'.format(k+1) + str(randint(10, 59))
                activity_inspector.server_time = date + ' ' + '{0}:00:00'.format(k+1)
                try:
                    activity_inspector.save()
                    activity_inspector.db_session.commit()
                except Exception:
                    falcon.HTTPUnprocessableEntity()


create_workers()
create_activity_log()

f = open('inspector.txt', 'w')

for index in inspector_data:
    f.write(index + '\n')

f.close()

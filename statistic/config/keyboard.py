import json

class Keyboard:

    KEYBOARD_STEP_1 = {
        'one_time': False,
        'buttons': [[{
            'action': {
                'type': 'text',
                'payload': json.dumps({'buttons': '1'}),
                'label': 'Добавить заданиe',
            },
            'color': 'negative'
        },
            {
                'action': {
                    'type': 'text',
                    'payload': json.dumps({'buttons': '2'}),
                    'label': 'Добавить время',
                },
                'color': 'primary'
            }], [
            {
                'action': {
                    'type': 'text',
                    'payload': json.dumps({'buttons': '3'}),
                    'label': 'Посмотреть задания',
                },
                'color': 'primary'
            }, {
                'action': {
                    'type': 'text',
                    'payload': json.dumps({'buttons': '3'}),
                    'label': 'Добавить категорию',
                },
                'color': 'primary'
            }

        ], [
            {
                'action': {
                    'type': 'text',
                    'payload': json.dumps({'buttons': '3'}),
                    'label': 'Выбрать задание',
                },
                'color': 'primary'
            },
            {
                'action': {
                    'type': 'text',
                    'payload': json.dumps({'buttons': '3'}),
                    'label': 'Посмотреть статистику',
                },
                'color': 'primary'
            }

        ]]
    }
    KEYBOARD_STEP_2 = {
        'one_time': True,
        'buttons': [[{
            'action': {
                'type': 'text',
                'payload': json.dumps({'buttons': '1'}),
                'label': 'Общее',
            },
            'color': 'primary'
        },
            {
                'action': {
                    'type': 'text',
                    'payload': json.dumps({'buttons': '2'}),
                    'label': 'Учеба',
                },
                'color': 'primary'
            }], [
            {
                'action': {
                    'type': 'text',
                    'payload': json.dumps({'buttons': '3'}),
                    'label': 'Работа',
                },
                'color': 'primary'
            }, {
                'action': {
                    'type': 'text',
                    'payload': json.dumps({'buttons': '3'}),
                    'label': 'Личное',
                },
                'color': 'primary'
            }

        ]]
    }
    KEYBOARD_STEP_3 = {
        'one_time': True,
        'buttons': [[{
            'action': {
                'type': 'text',
                'payload': json.dumps({'buttons': '1'}),
                'label': 'Выполнено',
            },
            'color': 'primary'
        },
            {
                'action': {
                    'type': 'text',
                    'payload': json.dumps({'buttons': '2'}),
                    'label': 'Изменить врeмя напоминания',
                },
                'color': 'primary'
            }], [
            {
                'action': {
                    'type': 'text',
                    'payload': json.dumps({'buttons': '3'}),
                    'label': 'Изменить текст',
                },
                'color': 'primary'
            }, {
                'action': {
                    'type': 'text',
                    'payload': json.dumps({'buttons': '3'}),
                    'label': 'Изменить кaтегорию',
                },
                'color': 'primary'
            }

        ]]
    }
GROUP_ID = 193249309
TOKEN = '9eac46bc3ae9df0e2bdc3404d0f5f70ef346a39fc314f6a26575cdfe98f9a89512a000668fb05b316a524'

DB_CONFIG = dict(
    provider='postgres',
    user='postgres',
    host='localhost',
    database='vk_chat_bot'
)

INTENTS = [
    {
        'name': 'Сообщение помощи',
        'tokens': ('/help', 'помощь'),
        'scenario': None,
        'answer': 'Привет, я бот для заказа авиабилетов на самолет. Если хотите заказать у нас билет на самолет, то вам необходимо:' \
                  '\n1. Ввести город отправления.\n2. Ввести город назначения.\n3. Ввести дату перелета.\n4. Выбрать рейс из предложенных.' \
                  '\n5. Уточнить кол-во мест.\n6. Написать произвольный комментарий.\n7. Проверить введенные данные.\n8. Указать номер телефона.' \
                  '\nДля того чтобы начать сценарий заказа авиабилетов введите команду /ticket.'
    },
    {
        'name': 'Начало сценария',
        'tokens': '/ticket',
        'scenario': 'start_scenario',
        'answer': None
    },
]
SCENARIOS = {
    'start_scenario': {
        'first_step': 'step1',
        'steps': {
            'step1': {
                'text': 'Хорошо, давайте начнём. Пожалуйста, введите город отправления',
                'failure_text': 'К сожалению, мы не смогли найти рейс с городом, который вы ввели. Выберите город, из которых есть рейс: {cities_with_flight}',
                'handler': 'handle_dep_city',
                'next_step': 'step2'
            },
            'step2': {
                'text': 'Введите город назначения',
                'failure_text': 'К сожалению, между введенными городами нет рейсов',
                'handler': 'handle_dest_city',
                'next_step': 'step3'
            },
            'step3': {
                'text': 'Введите дату рейса в формате дд-мм-гггг',
                'failure_text': 'Вы ввели неправильную дату, либо на данную дату нет ни одного рейса',
                'handler': 'handle_date',
                'next_step': 'step4'
            },
            'step4': {
                'text': 'Пожалуйста, выберите из предложенных рейсов один(введите номер): {flights}',
                'failure_text': 'К сожалению для заданных городов в дате, которую вы ввели, нет ни одного рейса. Попробуйте выбрать другой город отправления или назначения. Или введите другую дату рейса',
                'handler': 'handle_flights',
                'next_step': 'step5'
            },
            'step5': {
                'text': 'Пожалуйста, скажите сколько вам нужно билетов(от 1 до 5)',
                'failure_text': 'Вы ввели неправильное количество билетов, попробуйте ещё раз',
                'handler': 'handle_tickets',
                'next_step': 'step6'
            },
            'step6': {
                'text': 'Предлагаем вам написать комментарий в произвольной форме',
                'failure_text': None,
                'handler': 'handle_commentary',
                'next_step': 'step7'
            },
            'step7': {
                'text': 'Пожалуйста, проверьте введенные вами данные. Город отправления: {dep_city}, '
                        'город назначения: {dest_city}, дата вылета: {flight}, '
                        'количество билетов: {number_of_tickets} и ваш комментарий: {commentary}. Введите да или нет',
                'failure_text': 'Не понял вас, введите да или нет',
                'handler': 'handle_check',
                'next_step': 'step8'
            },
            'step8': {
                'text': 'Введите ваш номер телефона в формате +00000000000',
                'failure_text': 'Введите телефон в правильном формате',
                'handler': 'handle_telephone',
                'next_step': 'step9'
            },
            'step9': {
                'text': 'Введите имя которое будет указано в билете',
                'failure_text': 'Введите имя правильно',
                'handler': 'handle_name',
                'next_step': 'step10'
            },
            'step10': {
                'text': 'Хорошо, мы свяжемся с вами по набранному телефону. Вот ваш билет, до свидания',
                'image': 'generate_ticket_handler',
                'failure_text': None,
                'handler': None,
                'next_step': None
            },
        }
    },
}

DEFAULT_ANSWER = 'Простите, не знаю, что ответить. Введите /help, если хотите узнать, что я делаю или /ticket,' \
                 ' если хотите начать сценарий'

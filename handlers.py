import re
from datetime import datetime

from generate_ticket import generate_ticket


def handle_dep_city(text, context, settings_dict):
    context['cities_with_flight'] = []
    for dep_city, regex_and_cities in settings_dict.items():
        match = re.search(regex_and_cities['regex'].lower(), text.lower())
        if match:
            context['dep_city'] = dep_city
            return True
        else:
            context['cities_with_flight'].append(dep_city)
    else:
        return False


def handle_dest_city(text, context, settings_dict):
    for dest_city, regex_and_date in settings_dict[context['dep_city']]['cities'].items():
        match = re.search(regex_and_date['regex'].lower(), text.lower())
        if match:
            context['dest_city'] = dest_city
            return True
    else:
        return False


def handle_date(text, context, settings_dict):
    regex = r'\d\d-\d\d-\d{4}'
    match = re.search(regex, text)
    if match:
        context['date'] = text
        dates = set()
        try:
            datetime.strptime(text, '%d-%m-%Y')
            for date in settings_dict[context['dep_city']]['cities'][context['dest_city']]['date'].split(", "):
                if datetime.strptime(date, '%d-%m-%Y') >= datetime.strptime(text, '%d-%m-%Y'):
                    if len(dates) >= 5:
                        break
                    dates.add(date)
            context['flights'] = {}
            if len(dates) == 0:
                return False
            for number, date in enumerate(sorted(dates)):
                context['flights'][number + 1] = date
        except Exception:
            return False
        else:
            return True


def handle_flights(text, context, settings_dict):
    try:
        number = int(text)
        if len(text) == 1 and 0 < number <= 5:
            context['flight'] = traffic_planes(context, settings_dict)[number - 1]
            context.pop('date')
            return True
        else:
            return False
    except Exception:
        return False


def traffic_planes(user_state, settings_dict):
    dates = set()
    for date in settings_dict[user_state['dep_city']]['cities'][user_state['dest_city']]['date'].split(", "):
        if datetime.strptime(date, '%d-%m-%Y') >= datetime.strptime(user_state['date'], '%d-%m-%Y'):
            if len(dates) >= 5:
                break
            dates.add(date)
    if len(dates) < 1:
        return False
    dates = list(dates)
    return sorted(dates)


def handle_tickets(text, context, settings_dict):
    try:
        number = int(text)
    except Exception:
        return False
    if len(text) == 1 and 0 < number <= 5:
        context['number_of_tickets'] = text
        return True
    else:
        return False


def handle_commentary(text, context, settings_dict):
    context['commentary'] = text
    return True


def handle_check(text, context, settings_dict):
    if text.lower() == 'да':
        return True
    elif text.lower() == 'нет':
        context['start_over'] = True
        return True
    else:
        return False


def handle_telephone(text, context, settings_dict):
    if len(text) == 12 and text[1:].isdigit() and text[0] == '+':
        context['telephone'] = text
        return True
    else:
        return False

def handle_name(text, context, settings_dict):
    re_name = re.compile(r'^[\w\-\s]{3,40}$')
    match = re.search(re_name, text.lower())
    if match:
        context['fio'] = text
        return True
    else:
        return False


def generate_ticket_handler(text, context, settings_dict):
    return generate_ticket(dep_city=context['dep_city'], dest_city=context['dest_city'], flight=context['flight'],
                           fio=context['fio'])

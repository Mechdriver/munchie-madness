import csv
import json
import requests
import pprint
import asyncio
import random

FIVE_MILES_IN_METERS = 8047


def get_average_score(university):
    url = 'https://api.yelp.com/v3/businesses/search'
    headers = {'Authorization': 'Bearer {secret goes here}'}
    params = {
        'term': 'Restaurants',
        'radius': FIVE_MILES_IN_METERS,
        'limit': 50,
        'sort_by': 'review_count',
        'location': university,
    }
    response = requests.get(url, params=params, headers=headers)

    data = response.json()

    business_count = 0
    sum_score = 0

    for business in data['businesses']:
        rating = business['rating']
        sum_score += rating
        business_count += 1

    return sum_score / business_count


def record_scores():
    with open('school_list', 'r') as school_file:
        school_list = list(map(lambda line : str(line).strip().replace(',', ''), school_file.readlines()))

    score_dict = {}

    for school in school_list:
        score_dict[school] = get_average_score(school)

    with open('schools_to_score_v2.csv', 'w') as score_file:
        writer = csv.writer(score_file)
        writer.writerows(score_dict.items())


def sort_scores():
    score_dict = {}
    with open('schools_to_score_v2.csv', 'r') as score_file:
        for line in score_file.readlines():
            values = line.strip().split(',')
            score_dict[values[0]] = float(values[1])

    sorted_dict =dict(sorted(score_dict.items(), key=lambda item: item[1]))

    pprint.pprint(sorted_dict.items())


def get_finals_score():
    LOW = 55
    HIGH = 95
    print(f'GCU: {random.randrange(LOW, HIGH + 1)}')
    print(f'Ohio St.: {random.randrange(LOW, HIGH + 1)}')


get_finals_score()

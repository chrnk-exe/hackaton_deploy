from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response

import random
import requests
import math


def sigmoid(x):
    return 1 / (1 + math.exp(-x))


class MainApi(APIView):
    def get(self, request, ):
        return render(request, 'index.html')

    def post(self, request):
        return Response('post')


class CapacityApi(APIView):
    def get(self, request):
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXkiOiJ2a2lkMDAwMDAwMDAwIiwiZXhwIjoxNjg1NTc4NDA2fQ.U85uW7q-wpFg38kUekL8mc1YwvxYPTKu-9AZ-R5bj2A"
        headers = {"Authorization": f"Bearer {token}"}

        latitude, longitude = request.query_params.get('x'), request.query_params.get('y')

        path = f'https://our-spb.gate.petersburg.ru/our_spb/geo/buildings/nearest?latitude={latitude}&longitude={longitude}'
        r = requests.get(path, headers=headers)

        build_json = r.json()

        build_data = build_json.get('data')
        build_id = build_data.get('id')

        path_problems = f'https://our-spb.gate.petersburg.ru/our_spb/problems/by_buildings/{build_id}?format=common&count=10'
        r = requests.get(path_problems, headers=headers)
        problems = r.json().get('data')

        capacity = {
            'problems': 0,
            'petitions': 0,
            'answers2d': 0,
            'answers': 0,
            'accepted': 0,
        }

        if problems:
            for index, problem in enumerate(problems):
                capacity['problems'] += 1
                answers2d = list(map(lambda x: x.get('answers'), problem.get('petition')))
                for answers in answers2d:
                    capacity['answers2d'] += 1
                    if answers:
                        for answer in answers:
                            capacity['answers'] += 1
                            date = answer.get('accepted_at')
                            if date is not None:
                                capacity['accepted'] += 1

        coeff_for_key = {
            'problems': -1,
            'petitions': 0.2,
            'answers2d': 0.1,
            'answers': 0.1,
            'accepted': 0.5,
        }

        coefficient = sum(capacity[key] * coeff_for_key[key] for key in capacity)
        capacity['coefficient'] = sigmoid(coefficient)

        response = {
            'build': build_json,
            'problems': problems,
            'capacity': capacity
        }

        return Response(response, headers={'Access-Control-Allow-Origin': '*'})


class AllCapacityApi(APIView):
    def get(self, request):
        token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJrZXkiOiJ2a2lkMDAwMDAwMDAwIiwiZXhwIjoxNjg1NTc4NDA2fQ.U85uW7q-wpFg38kUekL8mc1YwvxYPTKu-9AZ-R5bj2A"
        headers = {"Authorization": f"Bearer {token}"}

        response = []

        districts_count = request.query_params.get('districts_count')
        count = request.query_params.get('count_for_district')

        path = 'https://our-spb.gate.petersburg.ru/our_spb/geo/districts/all'
        r = requests.get(path, headers=headers)
        districts = r.json().get('data')

        for district in districts[:int(districts_count)]:
            district_id = district.get('id')

            path = f'https://our-spb.gate.petersburg.ru/our_spb/problems/by_districts/{district_id}?format=common&count_on_page={count}'
            r = requests.get(path, headers=headers)

            problems_data = r.json().get('data')
            if problems_data is not None:
                for problem_data in problems_data:
                    response.append({
                        'reason': problem_data.get('reason', ''),
                        'latitude': problem_data.get('latitude', ''),
                        'longitude': problem_data.get('longitude', ''),
                        'building': problem_data.get('building')
                    })

        return Response(response, headers={'Access-Control-Allow-Origin': '*'})

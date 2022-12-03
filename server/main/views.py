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
        return Response(
            [
                {
                    "success": True,
                    "data": {
                        "id": 205780,
                        "prefix_id": 100029,
                        "district": {
                            "id": 100004,
                            "name": "Кингисеппский ЛО",
                            "is_updated": 1,
                            "is_actual": 1
                        },
                        "house": "б/н",
                        "full_address": "Кингисеппский район, поселок ж/д ст.Веймарн, дом б/н",
                        "short_address": "Кингисеппский р-н, п ж/д ст.Веймарн, д. б/н",
                        "latitude": 59.713474,
                        "longitude": 28.727406
                    }
                },
                {
                    "success": True,
                    "data": {
                        "id": 221812,
                        "prefix_id": 100079,
                        "district": {
                            "id": 100009,
                            "name": "Выборгский ЛО",
                            "is_updated": 1,
                            "is_actual": 1
                        },
                        "house": "б/н",
                        "liter": "Х",
                        "full_address": "Выборгский район, Красносельская волость, п Лебедевка, дом б/н, литера Х",
                        "short_address": "Выборгский район, Красносельская волость, п Лебедевка, д. б/н, л. Х",
                        "latitude": 60.625065,
                        "longitude": 28.951023
                    }
                },
                {
                    "success": True,
                    "data": {
                        "id": 221793,
                        "prefix_id": 100079,
                        "district": {
                            "id": 100009,
                            "name": "Выборгский ЛО",
                            "is_updated": 1,
                            "is_actual": 1
                        },
                        "house": "б/н",
                        "liter": "А",
                        "full_address": "Выборгский район, Красносельская волость, п Лебедевка, дом б/н, литера А",
                        "short_address": "Выборгский район, Красносельская волость, п Лебедевка, д. б/н, л. А",
                        "latitude": 60.625072,
                        "longitude": 28.949005
                    }
                }
            ]
        , headers={'Access-Control-Allow-Origin': '*'})


def error_404_view(request, *args, **argv):
    print('123123321')
    return redirect('/')

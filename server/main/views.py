from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response


class MainApi(APIView):
    def get(self, request):
        return render(request, 'index.html')

    def post(self, request):
        return Response('post')


def handler404(request, *args, **argv):
    print('123123321')
    return redirect('/')

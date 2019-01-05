import json
from django.shortcuts import render
from django.http import JsonResponse
from .fastlooker import getMatches

# Create your views here.
def search(req):
	word = req.GET.get('word')
	words = getMatches(word)
	return JsonResponse({
		"msg":"success",
		"data":words
		})

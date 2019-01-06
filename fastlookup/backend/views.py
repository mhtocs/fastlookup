import os
import json
from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from .fastlooker import FastLooker

FILENAME = os.path.join(settings.BASE_DIR, 'word_search.tsv')
fl = FastLooker(FILENAME)

# Create your views here.
def search(req):
	word = req.GET.get('word')
	words = fl.getMatches(word)
	return JsonResponse({
		"msg":"success",
		"data":words
		})

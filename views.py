from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.template import loader
from django.urls import reverse
import pathpy as pp
import numpy as np
import math

from pathpy.classes.paths import Paths
from pathpy.classes.higher_order_network import HigherOrderNetwork
from pathpy.path_extraction.origin_destination_stats import paths_from_origin_destination, read_origin_destination

from .forms import CardForm
from .models import Card

def run(card_text):
    numFrac = 3.5

    def similarity(s1, s2):
        wList1 = []
        for i in range(0,len(s1)):
            wList1.append(s1[i])
        wList2 = []
        for i in range(0,len(s2)):
            wList2.append(s2[i])
        denom = math.log(len(s1)) + math.log(len(s2))

        count = 0

        for word in wList1:
            if word in wList2:
                count+=1
        score = count/denom
        return score

    fWriterInt = open('cardSpaced.txt','w')


    LineList = card_text.split('. ')
    for line in LineList:
        fWriterInt.write(line.strip() + "." + "\n")

    fWriterInt.close()

    fReaderSentences = open('cardSpaced.txt','r')
    fWriteNodes = open('sentenceNodes.txt','w')
    fWriteAllEdges = open('sentenceAllEdgeWeights.txt','w')


    sentences = fReaderSentences.readlines()
    length = len(sentences)
    numSentences = int(length/numFrac)

    for i in range(0,len(sentences)):
        fWriteNodes.write(str(i) + "\n")

    sentenceListLists = []

    for sent1 in sentences:
        for sent2 in sentences:
            i1 = sentences.index(sent1)
            i2 = sentences.index(sent2)
            sentenceList = []
            score = similarity(sent1,sent2)
            sentenceList.append(str(i1))
            sentenceList.append(str(i2))
            sentenceList.append(str(score))
            sentenceListLists.append(sentenceList)

    sentenceListLists.sort(key=lambda x: float(x[2]))
    sentenceListLists.reverse()
    fWriteSortEdges = open('sentenceSortedEdgeWeights.txt','w')

    for list in sentenceListLists:
        fWriteSortEdges.write(list[1] + "," + list[0] + "," + str(round(float(list[2]))) + "\n")

    fWriteSortEdges.close()

    paths = pp.Paths.read_edges('sentenceSortedEdgeWeights.txt', weight=True)
    network = pp.HigherOrderNetwork(paths, k=1)

    prDict = pp.algorithms.centralities.pagerank(network, weighted=True)
    print(prDict)

    prListTotal = []
    for tuple in prDict:
        prList = []
        prList.append(tuple)
        prList.append(prDict[tuple])
        prListTotal.append(prList)

    prListTotal.sort(key=lambda x: float(x[1]))
    prListTotal.reverse()

    fSummarizedSentences = open('keySentences.txt','w')

    newList = []
    for i in range(0,numSentences):
        newList.append(int(prListTotal[i][0]))
    newList.sort()

    return newList

def index(request):
    if request.method == 'POST':
        form = CardForm(request.POST)
        if form.is_valid():

            unformattedText = form.cleaned_data['card_text']
            listIndex = run(unformattedText)
            allSentencesOld = unformattedText.split('. ')
            allSentences = []
            for i in range(0,len(allSentencesOld)):
                newString = str(allSentencesOld[i] + ". ")
                allSentences.append(newString)
                
            listSentences = []
            for i in listIndex:
                listSentences.append(allSentences[i])

            myDict = {'listSentences': listSentences, 'allSentences' : allSentences}

            return render(request, 'debate/results.html', myDict)

        
    else:
        form = CardForm()

    return render(request, 'debate/index.html', {'form': form})

    
def results(request, listSentences):
    pass

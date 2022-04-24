from django.shortcuts import redirect, render
# from django.shortcuts import render_to_response

from .forms import ProjectModel
import pandas as pd
import numpy as np
import re, math
from collections import Counter

# Create your views here.
def project_view(request):
    form = ProjectModel()
    return render(request, 'index.html', { 'form': form })

def test_view(request):

    WORD = re.compile(r'\w+')

    #applying cosine similarity for finding similarities between user interests and places
    def get_cosine(vec1, vec2):
        #print(vec1, vec2)
        intersection = set(vec1.keys()) & set(vec2.keys())
        numerator = sum([vec1[x] * vec2[x] for x in intersection])
        sum1 = sum([vec1[x]**2 for x in vec1.keys()])
        sum2 = sum([vec2[x]**2 for x in vec2.keys()])
        denominator = math.sqrt(sum1) * math.sqrt(sum2)
        if not denominator:
            return 0.0
        else:
            return float(numerator) / denominator

    def text_to_vector(text):
        words = WORD.findall(text)
        return Counter(words)

    #remove spaces from the category column of dataset
    def clean_data(x):
        if isinstance(x, list):
            return [str.lower(i.replace(" ", "")) for i in x]
        else:
            if isinstance(x, str):
                return str.lower(x.replace(" ", ""))
            else:
                return ''

    #calulating weighted rating of places



    metadata = pd.read_csv('/home/pal/Desktop/190953194/dmpa_project/myProject/project/Book1.csv', low_memory=False)
    text1 = request.GET.get('Category')
    text2 = request.GET.get('Location')
    text3 = request.GET.get('Budget')
    vector1 = text_to_vector(text1)
    C = metadata[' p_rating'].mean()
    m = metadata[' count'].quantile(0.75)

    def weighted_rating(x, m=m, C=C):
        v = x[' count']
        R = x[' p_rating']
        # Calculation based on the Bayesian Rating 
        
        return (v/(v+m) * R) + (m/(m+v) * C)

    metadata['Category'] = metadata['Category'].apply(clean_data)
    metadata[' score'] = metadata.apply(weighted_rating, axis=1)
    print(metadata[' score'])
    cos=[]
    for i in list(metadata['Category']):
        text2 = i
        vector2 = text_to_vector(text2)
        cosine = get_cosine(vector1, vector2)
        cos.append(cosine)
    metadata['cosine']=cos
    x=metadata['cosine']>0.0
    rec=pd.DataFrame(metadata[x])
    rec = rec.sort_values('cosine', ascending=False)
    rec = rec.sort_values(' score', ascending=False)
    p1 = ""
    u1 = ""
    p2 = ""
    u2 = ""
    p3 = ""
    u3 = ""
    b1 = ""
    b2 = ""
    b3 = ""
    v1 = ""
    v2 = ""
    v3 = ""
    text1 = request.GET.get('Category')
    text2 = request.GET.get('Region')
    text2 = text2.capitalize()
    text3 = request.GET.get('Budget')

    counter = 1
    for x in range(len(rec)):
        if rec[' Region'].iloc[x].strip() == text2 and counter==1 and rec[' Budget'].iloc[x] <= int(text3):
            p1 = rec[' Title'].iloc[x]
            u1 = rec[' URL'].iloc[x]
            b1 = rec[' Budget'].iloc[x]
            v1 = rec[' Places'].iloc[x]
            counter+=1
        elif rec[' Region'].iloc[x].strip() == text2 and counter==2 and rec[' Budget'].iloc[x] <= int(text3):
            p2 = rec[' Title'].iloc[x]
            u2 = rec[' URL'].iloc[x]
            b2 = rec[' Budget'].iloc[x]
            v2 = rec[' Places'].iloc[x]
            counter+=1
        elif rec[' Region'].iloc[x].strip() == text2 and counter==3 and rec[' Budget'].iloc[x] <= int(text3):
            p3 = rec[' Title'].iloc[x]
            u3 = rec[' URL'].iloc[x]
            b3 = rec[' Budget'].iloc[x]
            v3 = rec[' Places'].iloc[x]
    
    return render(request, 'test.html', { 'text_1_data': p1, 'text_2_data': u1 , 'text_3_data': p2, 'text_4_data': u2, 'text_5_data': p3, 'text_6_data': u3, 'text_7_data': b1 , 'text_8_data': b2 , 'text_9_data': b3, 'text_10_data': v1, 'text_11_data': v2, 'text_12_data': v3  })
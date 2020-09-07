from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import *
import requests
import bs4
import nltk
from newspaper import Article
from gensim.summarization import summarize
# Create your views here.
class titleurl:
    def title(self,title):
        self.title = title
    def url(self,url):
        self.url = url
    def urlpass(self,urlpass):
        self.urlpass = urlpass
@login_required(login_url='login')
def review(request):
    res = requests.get('https://www.livemint.com/technology/tech-news')
    soup = bs4.BeautifulSoup(res.text, 'lxml')
    read = soup.select('h2 > a')
    arr = []
    for i in range(15):
        myclass = titleurl()
        myurl = 'https://www.livemint.com' + read[i].get('href')
        myclass.title = read[i].text
        myclass.url = myurl
        arr.append(myclass)
    return render(request,'home/review.html',{'newslist':arr})

    #newslist = {}
    #for i in range(10):
    #    url = read[i].get('href')
    #    title = read[i].text
    #    newslist[title] = url
    #return render(request,'home/review.html',{'newslist':newslist})
@login_required(login_url='login')
def approve(request):
    selecturl = request.POST.get('selecturl')
    url = selecturl
    article = Article(url)
    article.download()
    article.parse()
    nltk.download('punkt')
    article.nlp()
    full_article = article.text
    artilce_title = article.title
    image_url = article.top_image
    summarize_1 = summarize(full_article, word_count=50)
    summarize_2 = article.summary
    return render(request,'home/approve.html',{'full_article':full_article,'summary_1':summarize_1,'summary_2':summarize_2,'article_title':artilce_title,'article_url':url,'image_url':image_url})

def dashboard(request):
    if request.method == 'POST':
        news = News()
        news.title = request.POST.get('article_title')
        news.summary = request.POST.get('article_summary')
        news.article_url= request.POST.get('article_url')
        news.image_url = request.POST.get('image_url')
        news.save()
    news = News.objects.all().order_by('-id')
    return render(request,'home/dashboard.html',{'news':news})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('review')
    return render(request,'home/login.html')

def user_logout(request):
    logout(request)
    return redirect('login')
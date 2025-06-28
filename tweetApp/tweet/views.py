from django.shortcuts import render
from .models import Tweet
from .forms import TweetForm
from django.shortcuts import get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from .forms import userRegistrationForm
from django.contrib.auth import login
# Create your views here.

def index(request):
    return render(request,'index.html')

def tweet_list(request):
    tweets=Tweet.objects.all().order_by('-created_at')
    return render(request,'tweet_list.html',{'tweets':tweets})

@login_required
def tweet_create(request):
    if request.method=='POST':     #when form is submitted after filling
        #request.files also gives us the file while post gives us the data
        form=TweetForm(request.POST,request.FILES)
        #checking whether from is valid or not
        if form.is_valid():
            #commmit is false to not save this in database
            tweet=form.save(commit=False)
            #we did not take user from forms, but request also has an inbuilt user
            tweet.user=request.user
            #not tweet gets saved in DB
            tweet.save()
            #this redirects it to tweetlist after saving
            return redirect('tweet_list')
    else:
        #Just show the form
        form=TweetForm()
    return render(request,'tweet_form.html',{'form':form})


#tweet_id is used to recognise the tweet, this we have inbuilt in django but note in urls we have to use this also.
@login_required
def tweet_edit(request,tweet_id):
    #this tweet will be filled with earlier tweet data
    #get_object_404 gets data from the Tweet model, we also match the requested user with model user saved in tweet
    tweet=get_object_or_404(Tweet,pk=tweet_id,user=request.user)
    if request.method=="POST" :
        form=TweetForm(request.POST,request.FILES,instance=tweet)
        if form.is_valid():
            tweet=form.save(commit=False)
            tweet.user=request.user
            tweet.save()
            return redirect('tweet_list')
    else:
        #instance is used to have the earlier version of tweetform since we are editing here
        form=TweetForm(instance=tweet)
    return render(request,'tweet_form.html',{'form':form})

@login_required
def tweet_delete(request,tweet_id):
    tweet=get_object_or_404(Tweet,pk=tweet_id,user=request.user)
    if request.method=="POST":
        tweet.delete()
        return redirect('tweet_list')
    return render(request,'tweet_delete_confirmation.html',{'tweet':tweet})

#register from will be in main project folder as app should not contain it.
def register(request):
    if request.method=="POST":
        form=userRegistrationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            #this directly does the login after registration
            login(request,user)
            return redirect('tweet_list')

    else:
        form=userRegistrationForm()
    return render(request,'registration/register.html',{'form':form})



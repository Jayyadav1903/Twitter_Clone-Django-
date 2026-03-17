from django.shortcuts import render
from .models import Tweet,Follow
from .forms import TweetForm, UserRegistrationForm
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.db.models import Q
from django.contrib.auth.models import User
# Create your views here.

def home(request):
    return render(request, 'index.html')

def tweet_list(request):
    if request.user.is_authenticated:
        
        following_ids = request.user.following_relationships.values_list(
        "following_id",
        flat=True
        )

        tweets = Tweet.objects.filter(
            user__in=following_ids,
            parent__isnull=True
        ) | Tweet.objects.filter(
            user=request.user,
            parent__isnull=True
        )
    else:
        tweets = Tweet.objects.filter(
            parent__isnull=True
        )
    tweets = tweets.select_related("user").order_by("-created_at")
    
    return render(request, "tweet_list.html", {"tweets": tweets})
    

@login_required
def tweet_create(request):
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES)
        
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    
    else: 
        form = TweetForm()
        
    return render(request, 'tweet_form.html', {'form': form})    

@login_required
def tweet_edit(request, tweet_id):
    tweet = get_object_or_404(Tweet,pk=tweet_id, user=request.user)
    
    if request.method == 'POST':
        form = TweetForm(request.POST, request.FILES, instance=tweet)
        if form.is_valid():
            tweet = form.save(commit=False)
            tweet.user = request.user
            tweet.save()
            return redirect('tweet_list')
    
    else:
        form = TweetForm(instance = tweet)
    
    return render(request, 'tweet_form.html', {'form': form})    

@login_required
def tweet_delete(request, tweet_id):
    tweet = get_object_or_404(Tweet,pk=tweet_id,user = request.user)
    if request.method =='POST':
        tweet.delete()
        return redirect('tweet_list')
    return render(request, 'tweet_confirm_delete.html', {'tweet': tweet})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        
        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])   
            user.save()
            login(request, user)
            return redirect('tweet_list')
    else:
        form = UserRegistrationForm()            
    return render(request, 'registration/register.html',{"form": form})


def search(request):
    query = request.GET.get('q')
    
    tweets = Tweet.objects.none() 
     
    if query:
        tweets = Tweet.objects.select_related("user").filter(
            Q(text__icontains=query) |
            Q(user__username__icontains=query)
        ).order_by('-created_at')
    else:
        tweets = Tweet.objects.filter(
    parent__isnull=True
).order_by('-created_at')

    return render(request, 'tweet_list.html', {
        'tweets': tweets,
        'query': query
    })

@login_required
def toggle_like(request, tweet_id):
    tweet = get_object_or_404(Tweet, pk=tweet_id)
    
    if tweet.likes.filter(id=request.user.id).exists():
        tweet.likes.remove(request.user)
    else:
        tweet.likes.add(request.user)
    
    return redirect('tweet_list')

@login_required
def reply_tweet(request, tweet_id):
    parent_tweet= get_object_or_404(Tweet, pk=tweet_id)
    
    if request.method =="POST":
        text = request.POST.get('text','').strip()
        if text:
            reply = Tweet.objects.create(
                user = request.user,
                text = text,
                parent = parent_tweet
            )
    
    return redirect('tweet_list')

@login_required
def follow_user(request, user_id):
    
    if request.method == "POST":
        user_to_follow = get_object_or_404(User, pk=user_id)       
    
        if user_to_follow != request.user:
            Follow.objects.get_or_create(follower=request.user, following=user_to_follow)
    
    return redirect('profile', user_id=user_id) 

@login_required
def unfollow_user(request, user_id):
    
    if request.method == "POST":
    
        user_to_unfollow = get_object_or_404(User, pk=user_id)    
        if user_to_unfollow != request.user:   
            Follow.objects.filter(follower=request.user, following=user_to_unfollow).delete()
    
    return redirect('profile', user_id=user_id) 

@login_required
def tweet_detail(request, tweet_id):

    tweet = get_object_or_404(
        Tweet.objects.select_related("user"),
        pk=tweet_id
    )

    replies = tweet.replies.select_related("user").order_by("created_at")

    return render(
        request,
        "tweet_detail.html",
        {
            "tweet": tweet,
            "replies": replies
        }
    )
    
@login_required
def toggle_retweet(request, tweet_id):

    tweet = get_object_or_404(Tweet, pk=tweet_id)

    if tweet.retweets.filter(id=request.user.id).exists():
        tweet.retweets.remove(request.user)
    else:
        tweet.retweets.add(request.user)

    return redirect("tweet_list")


def profile(request,user_id):
    
    profile_user = get_object_or_404(User,pk=user_id)
    
    tweets = Tweet.objects.filter(
        user=profile_user,
        parent__isnull=True
    ).order_by("-created_at")
    
    is_following = False
    
    if request.user.is_authenticated:
        is_following = Follow.objects.filter(
            follower=request.user,
            following=profile_user
        ).exists()
        
    followers_count = Follow.objects.filter(
        following=profile_user
    ).count()

    following_count = Follow.objects.filter(
        follower=profile_user
    ).count()

    tweets_count = Tweet.objects.filter(
        user=profile_user,
        parent__isnull=True
    ).count()    
        
    context = {
        "profile_user": profile_user,
        "tweets": tweets,
        "is_following": is_following
    }

    return render(request, "profile.html", {
        "profile_user": profile_user,
        "tweets": tweets,
        "is_following": is_following,
        "followers_count": followers_count,
        "following_count": following_count,
        "tweets_count": tweets_count,
    })                     
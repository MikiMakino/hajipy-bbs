from django.shortcuts import render
from .models import Post
from .forms import PostForm
from django.shortcuts import redirect
import requests
import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')

def index(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'posts/index.html',{'posts': posts})

def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            # Discordに通知を送る
            post = form.instance
            data = {
                "content": f"新しい投稿がありました！\nタイトル: {post.title}\n内容: {post.body}"
            }
            requests.post(DISCORD_WEBHOOK_URL, json=data)
            return redirect('index')
    else:
        form = PostForm()
    return render(request, 'posts/create.html', {'form': form})
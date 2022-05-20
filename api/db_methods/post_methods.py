from django.contrib.auth.models import User

from social_network.models import Post


def get_feed_for_user(user: User):
    liked_posts = user.liked_posts.all()
    disliked_posts = user.disliked_posts.all()
    all_posts = Post.objects.all()
    feed = list(filter(lambda post: post not in set(liked_posts) | set(disliked_posts), all_posts))
    return feed

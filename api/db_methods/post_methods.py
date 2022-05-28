from django.contrib.auth.models import User

from social_network.models import Post


def get_feed_for_user(user: User, subscriptions=False):
    liked_posts = user.liked_posts.all()
    disliked_posts = user.disliked_posts.all()
    if subscriptions:
        all_posts = Post.objects.filter(author__in=user.profile.subscriptions.all())
    else:
        all_posts = Post.objects.all()
    feed = list(
        sorted(
            filter(
                lambda post: post not in set(liked_posts) | set(disliked_posts),
                all_posts,
            ),
            key=lambda post: -post.rating,
        )
    )
    return feed

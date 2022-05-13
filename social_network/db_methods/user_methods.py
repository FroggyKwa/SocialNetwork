from django.contrib.auth.models import User


def subscribe_to(subscriber: User, to: User):
    try:
        subscriber.profile.subscriptions.add(to)
        subscriber.save()
    except Exception as e:
        print(e)
    return {"Success": "OK"}


def unsubscribe_from(subscriber, from_s):
    try:
        from_s.profile.subscriptions.remove(subscriber)
        from_s.save()
    except Exception as e:
        print(e)
    return {"Success": "OK"}


def get_all_users():
    return list(User.objects.all())

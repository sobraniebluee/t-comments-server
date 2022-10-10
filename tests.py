import multiprocessing

import random
import string

from src import config
from src.models.post_model import PostLikes, Post
from src.models.user_model import User


def create_user():
    username = ''.join(random.choices(string.ascii_uppercase + string.digits, k=30))
    email = 'dim@'.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    new_user = User(username=username, password='Front1529!', email=email)
    new_user.save()
    return new_user.id


def create_like():
    user_id = create_user()
    new_like = PostLikes(id_post=2981556809794804, type=config.Config.LIKE, id_user=user_id)
    new_like.save()


def create_post(user_id):
    text = ''.join(random.choices(string.ascii_uppercase + string.digits, k=1000))
    new_post = Post(id_author=user_id, title="hello from", description=[{"id": "pmC7dGi4ll", "data": {"text": "Hello kak dela&nbsp;"}, "type": "paragraph"}, {"id": "uMJw1r3DPx", "data": {"text": "ddd"}, "type": "paragraph"}, {"id": "9gbYSjWVbk", "data": {"text": "dd"}, "type": "paragraph"}, {"id": "4MA6u0q7MN", "data": {"text": "dddd"}, "type": "paragraph"}, {"id": "0pr60B2ALC", "data": {"text": "dddd"}, "type": "paragraph"}, {"id": "Lxn9i26UMb", "data": {"text": "dddd"}, "type": "paragraph"}])
    new_post.save()


def thread_func(iters):
    user_id_for = create_user()
    for i in range(0, iters):
        print(i)
        create_post(user_id_for)


if __name__ == '__main__':
    processes = [multiprocessing.Process(target=thread_func, args=(10,)) for _ in range(10)]
    for p in processes:
        p.start()

    for p in processes:
        p.join()

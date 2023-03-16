from django.urls import path
from .views import PostList, MyPostList, PostCreate, PostUpdate, PostDelete, add_comment, post_detail, comment_change_kind, comment_change_kind_from_mylist

urlpatterns = [
    path("", PostList.as_view(), name='post_list'),
    path('my_post/', MyPostList.as_view(), name='my_post_list'),
    path('<int:post_id>', post_detail, name='post_detail'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/update/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
    path('<int:post_id>/comment/', add_comment, name='create_comment'),
    path('<int:post_id>/change_status/<int:comment_id>/<int:kind>', comment_change_kind, name='comment_change_status'),
    path('my_post/change_status/<int:comment_id>/<int:kind>', comment_change_kind_from_mylist, name='comment_change_status_mypost'),
]

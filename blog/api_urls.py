from django.urls import include, path

from rest_framework import routers
from blog.views import PostAPIView, PostDetailAPIView, PostViewSet, UploadView, UserListView, UserSetView, UserViewSet, posts,PostListView



router = routers.DefaultRouter()
router.register('', UserViewSet)

# post_list_view = PostViewSet.as_view({
#     "GET" :"list",
#     "POST" : "create"
# })


from rest_framework.routers import DefaultRouter, SimpleRouter


# give you a api root
router1 = DefaultRouter()
# router1 = SimpleRouter()

router1.register("post", PostViewSet)

# give you a api root
router2 = DefaultRouter()
# router1 = SimpleRouter()

router2.register("users", UserSetView)

urlpatterns = [
   
    path('user/', include(router.urls)),
    # path('posts/',posts),
    # path('post/<int:id>/',post_detail),

    path('posts/',PostAPIView.as_view()),
    path('post/<int:id>/',PostDetailAPIView.as_view()),

    path('generics/posts/',PostListView.as_view()),
    path('generics/posts/<int:id>/',PostListView.as_view()),

    path('postviewset/', include(router1.urls)),


    # path('userfilter/',UserListView.as_view()),
    path('userfilter/', include(router2.urls)),

    path('upload/',UploadView.as_view()),


        

]

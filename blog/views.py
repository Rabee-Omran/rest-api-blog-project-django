from django_filters.filters import OrderingFilter
from blog.models import Post
from rest_framework import viewsets
from django.contrib.auth.models import  User
from django.http import  HttpResponse, JsonResponse
from .serializer import LoginSerializer, ProfileSerilizer, UserSerailizer
from blog.serializer import PostSerializer
from rest_framework.parsers import  JSONParser
from django.views.decorators.csrf import csrf_exempt



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerailizer



@csrf_exempt
def posts(request):
    if request.method == 'GET':
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many = True)

        return JsonResponse(serializer.data, safe = False)
    
    elif request.method == "POST":
        json_parser = JSONParser()
        data = json_parser.parse(request)
        serializer = PostSerializer(data= data)
        if serializer.is_valid():
           serializer.save()
           return JsonResponse(serializer.data, status  = 201)
        return JsonResponse(serializer.errors, status = 400)

@csrf_exempt
def post_detail2(request, id ):
    try :
        instance = Post.objects.get(id = id)
    except Post.DoesNotExist as e:
        return JsonResponse({'error': "given post object does not found"} , status = 404)


    if request.method == 'GET':
        serializer = PostSerializer(instance)
        return JsonResponse(serializer.data)
    
    elif request.method == "PUT":
        json_parser = JSONParser()
        data = json_parser.parse(request)
        serializer = PostSerializer(instance ,data= data)
        if serializer.is_valid():
           serializer.save()
           return JsonResponse(serializer.data, status  = 200)
        return JsonResponse(serializer.errors, status = 400)
    elif request.method == "DELETE":
        instance.delete()
        return HttpResponse( status = 204)

###############################################
from rest_framework.views import APIView
from rest_framework.response import Response


class PostAPIView(APIView):
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many = True)
        return Response(serializer.data, status= 200)
    
    def post (self, request):
        data = request.data
        serializer = PostSerializer(data= data)
        if serializer.is_valid():
           serializer.save()
           return Response(serializer.data, status  = 201)
        return Response(serializer.errors, status = 400)
         

class PostDetailAPIView(APIView):

    #for get object
    def get_object(self, id):
        try:
            return Post.objects.get(id = id)
        except Post.DoesNotExist as e:
            return Response({'error': "given post object does not found"} , status = 404)


    def get(self, request, id= None):
        instance = self.get_object(id)
        serializer = PostSerializer(instance)
        return Response(serializer.data)

    
    def put(self, request, id):
        data = request.data
        instance = self.get_object(id)
        serializer = PostSerializer(instance ,data= data)
        if serializer.is_valid():
           serializer.save()
           return Response(serializer.data, status  = 200)
        return Response(serializer.errors, status = 400)


    def delete(self, request, id):
        instance = self.get_object(id)
        instance.delete()
        return Response( status = 204)


##############################
from rest_framework import generics
from rest_framework import mixins
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.authentication import TokenAuthentication

class PostListView(generics.GenericAPIView, 
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.RetrieveModelMixin,    
                    mixins.DestroyModelMixin,         
                    ):

    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = 'id'

    #SessionAuthentication for csrftoken
    #BasicAuthentication username and password
    authentication_classes = [TokenAuthentication,SessionAuthentication, BasicAuthentication]


    #check for user if login or not 0 [return boolean value]
    #[IsAuthenticated, IsAdminUser]  check if user is admin or not
    permission_classes = [IsAuthenticated]


    def get(self, request, id = None):
        if id:
            return self.retrieve(request, id)
        else:
            return self.list(request)


    def post(self, request):
        return self.create(request)
    
    #in last line in create function above this method will be called
    # here we will make the author of created post post = request.user
    def perform_create(self, serializer):
        self.serializer


    def put(self, request, id = None):
        return self.update(request,id)


    #in last line in update function above this method will be called
    # here we will make the author of updated post = request.user
    def perform_update(self, serializer):
        serializer.save(author = self.request.user)

    def delete(self, request, id = None):
        return self.destroy(request,id)


###################
from rest_framework.views import APIView
from .serializer import LoginSerializer
#for session login, logout
from django.contrib.auth import login as django_login, logout as django_logout
#for auth token
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data = request.data)

        #raise_exception : if any error happend will raise exception
        serializer.is_valid(raise_exception = True)
        #we pass user from serailizer we made it
        print(serializer.errors)
        user = serializer.validated_data["user"]
        django_login(request, user)
        #TOKEN AUTH --- created is boolean Value -> if created or not
        token, created = Token.objects.get_or_create(user = user)
        return Response({'token':token.key}, status = 200)

class LogoutView(APIView):

    authentication_classes = [TokenAuthentication]

    def post(self, request):
        #logout from client device only  [not all devices]
        django_logout(request)
        return Response( status = 204)


###############################################
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializer import  PostSerializer

class PostViewSet(viewsets.ModelViewSet):
    
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = 'id'
    
    
    #Url -> http://127.0.0.1:8000/api/v1/postviewset/post/51/choices/
    @action(detail=True, methods=['GET'])
    def choices(self, request, id = None ):
        post = self.get_object()
        user_posts = Post.objects.filter(author__id = post.author.id)
        serializer = PostSerializer(user_posts, many = True)
        return Response(serializer.data, status=200)
    #same to action   but without detail parameter
    @action(detail=True, methods=['GET'])
    def choices2(self, request, id = None ):
        post = self.get_object()
        user = User.objects.get(id = post.author.id)
        posts = user.post_set.all()
        serializer = PostSerializer(posts, many = True)
        return Response(serializer.data, status=200)

 
    #Url -> http://127.0.0.1:8000/api/v1/postviewset/post/choices/
    @action(detail=False, methods=['GET'])
    def choices3(self, request):  
        post = Post.objects.all()
        serializer = PostSerializer(post, many = True)
        return Response(serializer.data, status=200)




######################################################


from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
#for custom filter
from django_filters import FilterSet
from django_filters import rest_framework as filters

#-----CUSTOM FILTER -----


class UserFilter(FilterSet):
    is_active  = filters.CharFilter('is_active')
    profileUser   = filters.CharFilter('profile__user')

    # min_salary = filters.CharFilter(method = "filter_by_min_salary")
    # max_salary = filters.CharFilter(method = "filter_by_max_salary")

    # # Url --> http://127.0.0.1:8000/api/v1/userfilter/?min_salary=1000/
    # def filter_by_min_salary(self,queryset, name, value ):
    #     queryset = queryset.filter(salary__gt = value)  #put your own field here
    #     return queryset
        

    # def filter_by_max_salary(self,queryset, name, value ):
    #     queryset = queryset.filter(salary__lt = value)
    #     return queryset
        


    class Meta:

        model = User
        fields = ('is_active', 'profileUser','username')

class UserListView(generics.ListAPIView):
    serializer_class  = UserSerailizer
    queryset = User.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filter_class = UserFilter
    
    ##[OrderingFilter] Url       -->  http://127.0.0.1:8000/api/v1/userfilter/?ordering=username
    ##[OrderingFilter] Url          -->  http://127.0.0.1:8000/api/v1/userfilter/?ordering=-username&is_active=True
    ordering_fields = ('is_active', 'username')
    #default ordering
    ordering = ('-username')

    ##[SearchFilter]   Url          --> http://127.0.0.1:8000/api/v1/userfilter/?search=admin
    ##check in both username and first_name
    search_fields = ('username', 'first_name')




from rest_framework.parsers import  FileUploadParser  #FormParser, MultiPartParser, JSONParser,


class UserSetView(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class  = UserSerailizer
    queryset = User.objects.all()


    @action(detail=True, methods=['PUT'])
    def profile(self, request, pk = None):
        user = self.get_object()
        profile = user.profile   #One to One Field
        
        #try to update user first name
        # user_first_name = request.data.get('first_name', user.first_name)
        # user.first_name = user_first_name
        # user.save()
       
        serializer = ProfileSerilizer(profile, data= request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status= 200)

        else :
            return Response(serializer.errors, status= 400)




class UploadView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [FileUploadParser]

    def post(self, request):
        file = request.data.get('file', None)

        # import pdb ; pdb.set_trace()
        # print(file)
        if file:

            return Response({"message" :"File is recieved" }, status= 200)
        else :
            return Response({"message" :"File is missing" }, status= 400)
            





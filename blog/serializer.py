from django.contrib.auth import authenticate
from django.db.models import fields
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Comment, Post, Profile
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import ValidationError



class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get("username", "")
        password = data.get("password", "")

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    data["user"] = user
                else:
                    msg = "User is deactivated."
                    raise ValidationError(msg)
            else:
                msg = "Unable to login with given credentials."
                raise ValidationError(msg)
        else:
            msg = "Must provide username and password both."
            raise ValidationError(msg)
        return data



################3


class CommentSerializer(serializers.ModelSerializer):
    id  = serializers.IntegerField(required = False)
   
  
    class Meta :
        model =  Comment
        fields = [
            'id',
            'body',
            'comment_date', 
            'post'
             ]

        read_only_fields = ['post']
             

    # def create(self, validated_data) :
    #     pass 

#################


class PostSerializer(serializers.ModelSerializer):

    #able to change but not required
   # comments = CommentSerializer(many= True, required= False)

    #not able to change
    #comments = CommentSerializer(many= True, read_only= True)

    comments = CommentSerializer(many= True)
    class Meta :
        model =  Post
        fields = [
            'id',
            'title',
            'content', 
            'author',
            'comments'
             ]
             
        #depth = 2


#try to create post with comments
    def create(self, validated_data) :
        #pop from dict
        comments = validated_data.pop('comments')
        # print(comments)
        post =  Post.objects.create(**validated_data) 
        for comment in comments:

            #**{'year': "2020"} --> year = 2020
            Comment.objects.create(**comment, post = post)

        return post


#try to edit post with comments
    def update(self,instance, validated_data) :
  
        comments = validated_data.pop('comments')
      
        instance.content = validated_data.get("content", instance.content)
        instance.title = validated_data.get("title", instance.title)
        instance.save()  
        keep_comments = []
        for comment in comments:
            if "id" in comment.keys():
              #  print("key : ",  comment.keys())   -->  key :  odict_keys(['id', 'body'])
                if Comment.objects.filter(id = comment['id']).exists():
                    c = Comment.objects.get(id = comment['id'])
                    c.body = comment.get("body", c.body)
                    c.save()
                    keep_comments.append(c.id)
                else:
                    continue
            else:
                c = Comment.objects.create(**comment, post = instance)
                keep_comments.append(c.id)
       

        for comment in instance.comments.all():
            if comment.id  not in keep_comments:
                comment.delete()
        return instance
#################


class ProfileSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ["id",'image']

class UserSerailizer(serializers.ModelSerializer):
    profile = ProfileSerilizer(read_only = True)
    class Meta:
        model = User
        # fields = "__all__"
        fields= (
            'id',
            'username',
            'first_name',
            'last_name',
            'is_staff',
            'is_superuser',
            'is_active',
            'email',
            'profile'
        )


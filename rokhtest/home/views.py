from django.contrib.auth.decorators import user_passes_test
from django.db.models.functions import Concat
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse, FileResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from rest_framework import renderers, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, BasePermission
from rest_framework.views import APIView
from accounts.models import User
from Posts.models import Post
from home.models import *
from django.db.models import F, OuterRef, Subquery, Q
from django.db.models.functions import Concat
from django.db.models import Value, F, CharField
from accounts.models import *
from accounts.serializers import *

@api_view(["GET"])
@permission_classes([IsAuthenticated, ])
@user_passes_test(lambda u: u.is_staff)
def page_home(request,**kwargs):
    # request = kwargs.get('request')
    # if request:
    #     request.session['request_count'] = request.session.get('request_count', 0) + 1
    user_count = User.objects.filter(is_active=True).count()
    # admin_count = User.objects.filter(is_staff=True).count()
    post_count = Post.objects.count()
    request_per_day = 500
    ticket_count = ContactUs.objects.filter(is_answer=False).count()


    return Response({
        "user_count": user_count,
        "post_count": post_count,
        "request_per_day": request_per_day,
        "ticket_count": ticket_count,
    })


@api_view(["GET", "POST", "DELETE"])
@permission_classes([IsAuthenticated])
@user_passes_test(lambda u: u.is_superuser)
def admin_list(request):
    if request.method == "GET":
        admins = User.objects.values("id", "username", "mobile",'pezeshki_code', "is_active")
        return Response(admins)

    elif request.method == "POST":
        if "username" not in request.data:
            return Response({"message": "enter username"})
        try:
            user = User.objects.get(username=request.data["username"])
            if user.is_active == True:
                return Response({"message": "this user is already active"})
            else:
                user.is_active = True
                user.save()
                return Response({"message": "this user now is active"})

        except:
            return Response({"message": "mobile not exist"})

    elif request.method == "DELETE":
        if "username" not in request.data:
            return Response({"message": "enter username"})
        try:
            user = User.objects.get(username=request.data["username"])
            if user.is_superuser == True:
                return Response({"message": "you can not change a superuser"})
            if user.is_active == False:
                return Response({"message": "this user is already not active"})
            else:
                user.is_active = False
                user.save()
                return Response({"message": "this user now is not active"})
        except:
            return Response({"message": "username not exist"})



@api_view(["GET", "PUT", "DELETE", "POST"])
@permission_classes([IsAuthenticated, ])
@user_passes_test(lambda u: u.is_active)
def slide_list(request, pk=None):
    if request.method == "GET":
        if pk is None:
            slides = Slides.objects.all().values()
            return Response(slides)
        else:
            try:
                slide = Slides.objects.values().get(id=pk)
                return Response(slide)
            except:
                return Response({"message": "id not found"})
    elif request.method == "DELETE":
        try:
            slide = Slides.objects.get(id=pk).delete()
            return Response({"message": "slide deleted"})
        except:
            return Response({"message": "id not found"})
    elif request.method == "POST":
        if "title" not in request.POST or "text" not in request.POST or "image" not in request.FILES or "status" not in request.POST:
            return Response({"message":"enter all fields"})

        try:
            slide = Slides.objects.create(
                title=request.POST["title"],
                text=request.POST["text"],
                image=request.FILES["image"],
                status=request.POST["status"]
            )
            slide.save()
            slide.image_url=slide.image.url
            slide.save()
            return Response({"message": "slide created"})

        except:
            return Response({'message':"slide not created (for som reason)"})


    elif request.method == "PUT":
        try:
            slide = Slides.objects.get(id=pk)
            if "title" in request.POST:
                slide.title = request.POST["title"]
            if "text" in request.POST:
                slide.text = request.POST["text"]
            if "image" in request.FILES:
                slide.image = request.FILES["image"]
                slide.save()
                slide.image_url=slide.image.url
            if "status" in request.POST:
                slide.status = request.POST["status"]

            slide.save()
            return Response({"message": "slide changed"})
        except:
            return Response({"message": "id not found"})



@api_view(["GET", "DELETE", "PUT", "POST"])
@permission_classes([IsAuthenticated, ])
@user_passes_test(lambda u: u.is_active)
def menu_list(request, pk=None):
    if request.method == "GET":
        if pk == None:
            menus = Menu.objects.all().annotate(
                parent_name=Subquery(
                    Menu.objects.filter(id=OuterRef('parent_id')).values('title')[:1]
                )
            ).values()
            return Response(menus)
        else:
            try:
                menu = Menu.objects.values().get(id=pk)
                return Response(menu)
            except:
                return Response({"message": "id not found"})
    elif request.method == "DELETE":
        try:
            menu = Menu.objects.get(id=pk).delete()
            return Response({"message": "menu deleted"})
        except:
            return Response({"message": "id not found"})

    elif request.method == "POST":
        if "title" not in request.data or "link" not in request.data or "parent_id" not in request.data or "type" not in request.data:
            return Response({"message": "enter all fields"})
        menu = Menu.objects.create(
            title=request.data["title"],
            link=request.data["link"],
            parent_id=request.data["parent_id"],
            type=request.data["type"]
        ).save()
        return Response({"message": "menu created"})

    elif request.method == "PUT":
        try:
            menu = Menu.objects.get(id=pk)
            if "title" in request.data:
                menu.title = request.data["title"]
            if "link" in request.data:
                menu.link = request.data["link"]
            if "parent_id" in request.data:
                menu.parent_id = request.data["parent_id"]
            if "type" in request.data:
                menu.type = request.data["type"]

            menu.save()
            return Response({"message": "menu changed"})
        except:
            return Response({"message": "id not found"})


@api_view(["GET", "PUT", "DELETE","POST"])
@permission_classes([IsAuthenticated, ])
@user_passes_test(lambda u: u.is_active)
def tickets_list(request, pk=None):
    if request.method == "GET":
        if pk == None:
            tickets = ContactUs.objects.all()
            tickets=tickets.annotate(
                answer=Subquery(
                    TicketAnswer.objects.filter(ticket_id=OuterRef('id')).values('answer')[:1]
                )
            ).values()
            return Response(tickets.order_by("is_answer","-id"))
        else:
            try:
                tickets = ContactUs.objects
                tickets = tickets.annotate(
                    answer=Subquery(
                        TicketAnswer.objects.filter(ticket_id=OuterRef('id')).values('answer')[:1]
                    )
                ).values().get(id=pk)
                return Response(tickets)
            except:
                return Response({"message": "id not found"})

    elif request.method == "DELETE":
        try:
            ContactUs.objects.get(id=pk).delete()
            return Response({"message": "ticket deleted"})
        except:
            return Response({"message": "id not found"})

    # elif request.method == "PUT":
    #     try:
    #         contact = ContactUs.objects.get(id=pk)
    #         if "answer" in request.data:
    #
    #
    #
    #             return Response({"message": "comment changed"})
    #         else:
    #             return Response({"message": "enter is_suggest field"})
    #     except:
    #         return Response({"message": "id not found"})


    elif request.method == "POST":
        if "answer" not in request.data or "id" not in request.data or pk==None:
            return Response({"message":"fill all fields"})

        try:
            answer=TicketAnswer.objects.create(
                answer=request.data["answer"],
                name=User.objects.get(id=request.data["id"]).name,
                ticket_id=ContactUs.objects.get(id=pk)
            ).save()
            c=ContactUs.objects.get(id=pk)
            c.is_answer=True
            c.save()
            return Response({"message":"answer created"})
        except:
            return Response({"message":"User or ticket id not found"})





@api_view(['POST', 'PUT', 'DELETE',"GET"])
@permission_classes([IsAuthenticated])
@user_passes_test(lambda u: u.is_staff)
def posts_list(request, pk=None):
    if request.method == "GET":
        if pk is None:
            posts = Post.objects.all()
            posts=posts.annotate(
                author_name=Concat('author__username',Value(''))
            ).values()
            return Response(posts)
        else:
            try:
                post = Post.objects.annotate(
                    author_name=Concat('author__username',Value(''))
                ).values().get(id=pk)
                return Response(post)
            except:
                return Response({"message": "id not found"})
    elif request.method == "DELETE":
        try:
            post = Post.objects.get(id=pk).delete()
            return Response({"message": "post deleted"})
        except:
            return Response({"message": "id not found"})

    elif request.method == "POST":
        if "title" not in request.POST or "sub_title" not in request.POST or "text" not in request.POST or "status" not in request.POST or "id" not in request.POST:
            return Response({"message": "enter all fields"})

        try:
            post = Post.objects.create(
                title=request.POST["title"],
                sub_title=request.POST["sub_title"],
                text=request.POST["text"],
                status=request.POST["status"],
                author=User.objects.get(id=request.POST["id"]),
                tags=request.POST['tags'],
            )
            if "image" in request.FILES:
                post.image=request.FILES["image"]
                post.save()
                post.image_url = post.image.url

            post.save()


            return Response({"message": "post created"})

        except:
            return Response({'message': "post not created (for some reason)"})


    elif request.method == "PUT":
        try:
            post = Post.objects.get(id=pk)
            if "title" in request.POST:
                post.title = request.POST["title"]
            if "sub_title" in request.POST:
                post.sub_title=request.POST["sub_title"]
            if "text" in request.POST:
                post.text = request.POST["text"]
            if "image" in request.FILES:
                post.image = request.FILES["image"]
                post.save()
                post.image_url=post.image.url
            if "status" in request.POST:
                post.status = request.POST["status"]
            if "tags" in request.POST:
                post.tags = request.POST['tags']

            post.save()
            return Response({"message": "post changed"})
        except:
            return Response({"message": "id not found"})



@api_view(["GET", "PUT", "DELETE", "POST"])
@permission_classes([IsAuthenticated, ])
@user_passes_test(lambda u: u.is_staff)
def teammate_list(request, pk=None):
    if request.method == "GET":
        if pk is None:
            teams = Teammate.objects.all().values()
            return Response(teams)
        else:
            try:
                team = Teammate.objects.values().get(id=pk)
                return Response(team)
            except:
                return Response({"message": "id not found"})

    elif request.method == "DELETE":
        try:
            team = Teammate.objects.get(id=pk).delete()
            return Response({"message": "teammate deleted"})
        except:
            return Response({"message": "id not found"})
    elif request.method == "POST":
        if "label" not in request.POST or "image" not in request.FILES or "link" not in request.POST:
            return Response({"message":"enter all fields"})

        try:
            team = Teammate.objects.create(
                label=request.POST["label"],
                link=request.POST["link"],
                image=request.FILES["image"],
            ).save()

            team.image_url = team.image.url
            team.save()
            return Response({"message": "teammate created"})

        except:
            return Response({'message':"teammate not created (for some reason)"})


    elif request.method == "PUT":
        try:
            team = Teammate.objects.get(id=pk)
            if "label" in request.POST:
                team.label = request.POST["label"]
            if "link" in request.POST:
                team.link = request.POST["link"]
            if "image" in request.FILES:
                team.save()
                team.image_url = team.image.url
                team.image = request.FILES["image"]

            team.save()
            return Response({"message": "teammate changed"})
        except:
            return Response({"message": "id not found"})








@api_view(["GET", "PUT"])
@permission_classes([IsAuthenticated, ])
@user_passes_test(lambda u: u.is_superuser)
def mainsettings(request):
    if request.method == "GET":
        try:
            info = RokhInfo.objects.values().get(id=1)
            return Response(info)
        except:
            return Response({"massage": "enter information"})

    elif request.method == "PUT":
        try:
            info = RokhInfo.objects.get_or_create(id=1)
            if "name" in request.POST:
                info.name = request.POST["name"]
            if "number" in request.POST:
                info.number = request.POST["number"]
            if "address" in request.POST:
                info.address = request.POST["address"]
            if "email" in request.POST:
                info.email=request.POST["email"]
            if "description" in request.POST:
                info.description = request.POST["description"]
            if "image" in request.FILES:
                info.image=request.FILES["image"]
                info.save()
                info.image_url=info.image.url
            info.save()
            return Response({"message": "information updated"})
        except:
            return Response({"massage": "enter information"})


# @api_view(["GET"])
# def doctor_profile(request, id):
#     if request.method == "GET":
#         # try:
#         #   expertise = Expertise.objects.values("name").get()
#         #     doctr = Profile.objects.values("name", 'bio', "pezeshki_code", "profile_image", 'working_hour', "expertise",
#         #                                    "birth_year").get(id=id)
#         p = Profile.objects.get(id=id)
#         s = ProfileSerializer(p)
#
#         return Response(s.data, status=200)
#
#         # except:
#         #     return Response({"massage": "doctr is not exsit"})
class DrProfileView(APIView):
    def get(self, request, id):
        # try:
            profile = Profile.objects.get(id=id)
            serializer = ProfileSerializer(profile)
            return Response(serializer.data)
        # except Profile.DoesNotExist:
        #     return Response({'error': 'DrProfile not found'}, status=404)

from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from django.views import generic
from django.http import Http404

from braces.views import SelectRelatedMixin
from posts import models,forms

from django.shortcuts import get_object_or_404

from django.contrib import messages

# Create your views here.

from django.contrib.auth import get_user_model
User=get_user_model()

class PostList(SelectRelatedMixin,generic.ListView):
    model = models.Post
    select_related = ('user','group')

class UserPosts(generic.ListView):
    model=models.Post
    template_name="posts/user_post_list.html"
  
    def get_queryset(self):
        try:
            self.post_user=User.objects.prefetch_related('posts').get(username__iexact=self.kwargs.get('username'))
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['post_user']=self.post_user
        return context

class PostDetail(SelectRelatedMixin,generic.DetailView):
    model=models.Post
    select_related=('user','group')

    def get_queryset(self):
        queryset=super().get_queryset()
        return queryset.filter(user__username__iexact=self.kwargs.get('username'))

class CreatePost(LoginRequiredMixin,SelectRelatedMixin,generic.CreateView):
    fields = ('message','group')
    model=models.Post

    def form_valid(self,form):
        self.object = form.save(commit=False)
        self.object.user= self.request.user
        self.object.save()
        return super().form_valid(form)


class DeletePost(LoginRequiredMixin,SelectRelatedMixin,generic.DeleteView):
    model=models.Post
    select_related=('user','group')
    success_url=reverse_lazy('posts:all')


    def get_queryset(self):
        queryset=super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self,*args,**kwargs):
        messages.success(self.request,'Post Deleted')
        return super().delete(*args,**kwargs)

class JoinGroup(LoginRequiredMixin,generic.RedirectView):

    def get_redirect_url(self,*args,**kwargs):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})

    def get(self, request,*args,**kwargs):
        group = get_object_or_404(Group,slug=self.kwargs.get('slug'))

        try:
            GroupMember.objects.create(user=self.request.user, group=group)
        except:
            messages.warning(self.request,'Warning aldready a member !!')

        else:
            messages.success(self.request,"you are now a member")

        return super().get(request,*args,**kwargs)

class LeaveGroup(LoginRequiredMixin,generic.RedirectView):
    def get_redirect_url(self,*args,**kwargs):
        return reverse('groups:single',kwargs={'slug':self.kwargs.get('slug')})

    def get(self, request,*args,**kwargs):
        group = get_object_or_404(Group,slug=self.kwargs.get('slug'))

        try:
            membership = models.GroupMember.objects.filter(
                user=self.request.user,
                group__slug=self.lwargs.get('slug')
            ).get()

        except models.GroupMember.DoesNotExist:
            messages.warning(self.request,'You are not a part of this group')

        else:
            membership.delete()
            messages.success(self.request,"you have left the group")

        return super().get(request,*args,**kwargs)










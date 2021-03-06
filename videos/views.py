from django.shortcuts import render, reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views import View
from .models import Video, Comment, Category
from .forms import CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin  # Mixins are used to restrict access to non logged in users


# Class based view to view all video content that's odered by date posted


class Index(ListView):
    model = Video
    template_name = 'videos/index.html'
    order_by = '-date_posted'

#  Create video class that uploads video and passes it into the detail video view
#  The create video class also has a form validator that validates that the uploader of the video is the current logged in user


class CreateVideo(LoginRequiredMixin, CreateView):
    model = Video
    fields = ['title', 'description', 'video_file', 'thumbnail', 'category']
    template_name = 'videos/create_video.html'

    def form_valid(self, form):
        form.instance.uploader = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('video-detail', kwargs={'pk': self.object.pk})


#  Detail video class that receives video from create video class
#  Get function retreives the video and comment form and shows similar videos
#  Post function allows the user to post a comment through the comment form on the video
#  The context is the variables that are being passed to the html template


class DetailVideo(View):
    def get(self, request, pk, *args, **kwargs):
        video = Video.objects.get(pk=pk)

        form = CommentForm()
        comments = Comment.objects.filter(video=video).order_by('-created_on')
        categories = Video.objects.filter(category=video.category)[:4]

        context = {
            'object': video,
            'comments': comments,
            'categories': categories,
            'form': form
        }
        return render(request, 'videos/detail_video.html', context)

    def post(self, request, pk, *args, **kwargs):
        video = Video.objects.get(pk=pk)

        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                user=self.request.user,
                comment=form.cleaned_data['comment'],
                video=video
            )
            comment.save()  # saves comment to the database

        comments = Comment.objects.filter(video=video).order_by('-created_on')
        categories = Video.objects.filter(category=video.category)[:4]

        context = {
            'object': video,
            'comments': comments,
            'categories': categories,
            'form': form
        }
        return render(request, 'videos/detail_video.html', context)


# Update video class where the video information can edited and updated
# User passes test mixin allows only the video uloader to edit or update the video
# The test function returns a true or false on if the current user is also the video uploader


class UpdateVideo(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Video
    fields = ['title', 'description']
    template_name = 'videos/create_video.html'

    def get_success_url(self):
        return reverse('video-detail', kwargs={'pk': self.object.pk})

    def test_func(self):
        video = self.get_object()
        return self.request.user == video.uploader


# Delete video class where the video can be deleted from the application
# User passes test mixin allows only the video uloader to delete the video


class DeleteVideo(LoginRequiredMixin, DeleteView):
    model = Video
    template_name = 'videos/delete_video.html'

    def get_success_url(self):
        return reverse('index')


#  Category class view where video can be seperated out into categories
#  Get function retrieves the category and the videos in that category


class VideoCategoryList(View):
    def get(self, request, pk, *args, **kwargs):
        category = Category.objects.get(pk=pk)
        videos = Video.objects.filter(category=pk).order_by('-date_posted')
        context = {
            'category': category,
            'videos': videos
        }

        return render(request, 'videos/video_category.html', context)

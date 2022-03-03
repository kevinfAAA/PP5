from django.shortcuts import render, get_object_or_404, reverse
from django.views import View
from django.views.generic.edit import UpdateView
from .models import Profile
from videos.models import Video


# Profile View
# gets the profile of returns a 404 error if the profile is not found identified by its primary key
# gets all the videos posted by this user where the uploader equals the primary key


class ProfileView(View):

    def get(self, request, pk, *args, **kwargs):
        profile = get_object_or_404(Profile, pk=pk)
        videos = Video.objects.filter(uploader=request.user).order_by('-date_posted')  # gets all the video objects and filters it by uploader and orders it by newest videos first

        context = {
            'profile': profile,
            'videos': videos,
        }

        return render(request, 'profiles/profile.html', context)


# Update profile class
# Form validater that uploads a default image if the user chooses not to upload a profile image


class UpdateProfile(UpdateView):
    model = Profile
    fields = ['name', 'location', 'image']
    template_name = 'profiles/update_profile.html'

    def form_valid(self, form):
        if not form.instance.image:
            form.instance.image = 'uploads/profile_pics/default.jpg'
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('profile', kwargs={'pk': self.object.pk})

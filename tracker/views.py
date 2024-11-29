from django.contrib import messages
from django.contrib.auth import login
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import CreateView
from django.views.generic.list import ListView
from django.http import JsonResponse

from .forms import SignUpForm
from .models import Contributor

class CreateUserView(CreateView):
    form_class = SignUpForm
    success_url = "/admin/"
    template_name = "signup.html"

    def get(self, request, *args, **kwargs) -> HttpResponse:
        """
        A GET request for this view.
        :param request: HttpRequest
        :param args: tuple
        :param kwargs: dict
        :return: HttpResponse
        """
        form = self.form_class()

        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs) -> HttpResponse:
        """
        A POST request for this view.
        :param request: HttpRequest
        :param args: tuple
        :param kwargs: dict
        :return: HttpResponse
        """
        form = self.form_class(request.POST)

        if form.is_valid():
            new_user = form.save()
            login(request, new_user)

            return redirect(self.success_url)

        [messages.error(request, error_) for error_ in form.errors.values()]

        return render(request, self.template_name, {"form": form})


class ContributorListView(ListView):
    """
    A view to list contributors with role-based data visibility.
    """

    model = Contributor

    def get_queryset(self):
        """
        Customize the queryset based on the user's role.
        Project leads can see notes and rank, while others cannot.
        """
        user = self.request.user

        if user.is_project_lead():
            return Contributor.objects.all()
        return Contributor.objects.all().only("id", "user", "role")

    def render_to_response(self, context, **response_kwargs):
        """
        Customize the JSON response to include contributor data.
        """
        queryset = self.get_queryset()
        user = self.request.user

        if user.is_project_lead():
            data = [
                {
                    "id": contributor.id,
                    "user": contributor.user.telegramuser.telegram_id,
                    "role": contributor.role,
                    "notes": contributor.notes,
                    "rank": contributor.rank,
                }
                for contributor in queryset
            ]
        else:
            data = [
                {
                    "id": contributor.id,
                    "user": contributor.user.telegramuser.telegram_id,
                    "role": contributor.role,
                }
                for contributor in queryset
            ]

        return JsonResponse(data, safe=False, **response_kwargs)
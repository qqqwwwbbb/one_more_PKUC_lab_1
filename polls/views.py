from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden, Http404

from .forms import RegisterForm, UpdateForm
from .models import Question, Choice, User
from django.template import loader
from django.urls import reverse, reverse_lazy
from django.views import generic


class Register(generic.CreateView):
    template_name = 'registration/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('polls:login')


class Profile(LoginRequiredMixin, generic.DetailView):
    model = User
    template_name = 'polls/profile.html'


class DeleteUser(LoginRequiredMixin, generic.DeleteView):
    model = User
    success_url = reverse_lazy('polls:index')


class UpdateUser(LoginRequiredMixin, generic.UpdateView):
    model = User
    form_class = UpdateForm
    success_url = reverse_lazy('polls:index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        other_user = User.objects.get(pk=self.kwargs['pk'])
        if self.request.user.pk != other_user.pk:
            raise Http404

        return context


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quest = Question.objects.get(pk=self.kwargs['pk'])
        if not quest.was_published_recently() and not self.request.user.is_superuser:
            raise Http404

        return context


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': 'Вы не сделали выбор'
        })
    else:
        if Question.objects.filter(id=question_id, voted_by=request.user):
            return render(request, 'polls/detail.html', {
                'question': question,
                'error_message': 'Вы уже приняли участие в голосовании'
            })
        else:
            question.voted_by.add(request.user)
            question.votes += 1
            question.save()
            selected_choice.votes += 1
            selected_choice.save()
            return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

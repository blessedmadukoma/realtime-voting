from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from .forms import UserForm, VoterUserForm
from .models import Question, Choice, Voter
import json

# Get questions and display them


def view_polls(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'users/view_polls.html', context)


@login_required
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]

    voters = Voter.objects.all()
    context = {'latest_question_list': latest_question_list, 'voter': voters}
    return render(request, 'users/index.html', context)


def register(request):
    if request.user.is_authenticated:
        return redirect("users:index")
    if request.method == "POST":
        form = UserForm(request.POST)
        voterForm = VoterUserForm(request.POST)

        if form.is_valid() and voterForm.is_valid():
            user = form.save()

            voter = voterForm.save(commit=False)

            voter.user = user

            voter.save()

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)

            # return redirect('users:login')
        else:
            form = UserForm()
            voterForm = VoterUserForm()
            context = {'form': form, 'voterForm': voterForm,
                       'error_message': "Form is not valid."}
            return render(request, 'users/register.html', context)
    else:
        form = UserForm()
        voterForm = VoterUserForm()

    context = {'form': form, 'voterForm': voterForm}
    return render(request, 'users/register.html', context)


def loginUser(request):
    if request.user.is_authenticated:
        return redirect("users:index")
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        login(request, user)
        # login(request, username, password)
        print('logging user!!!')
        return redirect('users:index')
    return render(request, 'users/login.html')


def logoutUser(request):
    logout(request)
    return redirect('users:login')


# Show specific question and choices: You need to log in to vote
@login_required
def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'users/detail.html', {'question': question})

# Get question and display results


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'users/results.html', {'question': question})


# Get all questions and their results
def all_result(request):
    questions = Question.objects.all()
    return render(request, 'users/all_result.html', {'questions': questions})

# Vote for a question choice


@login_required
def vote(request, question_id):
    # print(request.POST['choice'])
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'users/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        current_voter = request.user
        client_obj = Voter.objects.get(user=current_voter)
        if client_obj:
            clientJSON = str(client_obj.json)
            # print(client_obj)
            print(clientJSON)
            print("Type of clientJSON: ", type(clientJSON))
            appender = {
                question_id: str(selected_choice),
            }
            print("First Type of appender: ", type(appender))
            appender = json.dumps(appender)
            print("Second Type of appender: ", type(appender))
            clientJSON += appender
            # storing question: selected_choice
            # client_obj.is_vote = True
            # client_obj.question_vote = selected_choice
            selected_choice.votes += 1
            selected_choice.save()
            client_obj.json = clientJSON
            client_obj.save()
            print(client_obj.json)
            print(clientJSON)
            current_voter.save()
            # Always return an HttpResponseRedirect after successfully dealing
            # with POST data. This prevents data from being posted twice if a
            # user hits the Back button.
            return HttpResponseRedirect(reverse('users:results', args=(question.id, )))

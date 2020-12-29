from django.db import IntegrityError
from django.shortcuts import render,redirect
from django.http import HttpResponse,Http404,HttpResponseRedirect
from django.urls import reverse_lazy
from poll.models import *
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.contrib import messages
from django.views.generic import View
from poll.forms import PollForm, ChoiceForm
from poll.models import  Questions,Choice
from django.shortcuts import  get_object_or_404
# Create your views here.
#@login_required(login_url="/login/")  # For Url
@login_required(login_url="login")  # For url name
def index(request):
    questions = Questions.objects.all()
    return render(request,'poll/index.html',{"questions":questions})
@login_required(login_url="login")
def details(request,id= None):
    try:
        question  =Questions.objects.get(id=id)
        return render(request, 'poll/detail.html', {"question": question})
    except Exception as e:

        raise e

@login_required(login_url="login")
def poll(request,id= None):
    if request.method == "GET":
        try:
            question  =Questions.objects.get(id=id)
            return render(request, 'poll/choice.html', {"question": question})
        except Exception as e:
            raise Http404
    if request.method == "POST":
        '''
        #To Print session key and values        
        for key, value in request.session.items():
            print('{} => {}'.format(key, value))
        '''
        data = request.POST
        user_id = request.session.get("_auth_user_id")
        try:
            res=Answer.objects.create(user_id = user_id,choice_id=data["choice"])
            if res:
                messages.success(request,"You Vote Casted Successfully")

                return redirect(f'/poll/{id}/details/')
        except IntegrityError:
            messages.error(request, "You Vote Not Casted")
            return redirect(f'/poll/{id}/details/')

class PollView(View):
    def get(self,request,id=None):
        if id:
            pass
        else:
            poll_form = PollForm(instance=Questions())
            choice_forms = [ChoiceForm(prefix=str(
                x), instance=Choice()) for x in range(3)]
            context = {'poll_form': poll_form, 'choice_forms': choice_forms}
            return render(request, 'poll/new_poll.html', context)

    def post(self, request, id=None):
        context = {}
        if id:
            print("aaaaaaaaaaaa")
            return self.put(request, id)
        print("bbbbbbb")
        poll_form = PollForm(request.POST, instance=Questions())
        choice_forms = [ChoiceForm(request.POST, prefix=str(
            x), instance=Choice()) for x in range(0, 3)]
        if poll_form.is_valid() and all([cf.is_valid() for cf in choice_forms]):
            new_poll = poll_form.save(commit=False)
            new_poll.created_by = request.user
            new_poll.save()
            for cf in choice_forms:
                new_choice = cf.save(commit=False)
                new_choice.Question = new_poll
                new_choice.save()
            return HttpResponseRedirect('/poll/')
        context = {'poll_form': poll_form, 'choice_forms': choice_forms}
        return render(request, 'poll/new_poll.html', context)


class PollViewEdit(View):
    def get(self, request, id=None):
        context = {}
        question = get_object_or_404(Questions, id=id)
        poll_form = PollForm(request.POST, instance=question)
        choice_forms = [ChoiceForm(request.POST, prefix=str(choice.id), instance=choice) for choice in question.choice_set.all()]
        # if poll_form.is_valid() and all([cf.is_valid() for cf in choice_forms]):
        #     new_poll = poll_form.save(commit=False)
        #     new_poll.created_by = request.user
        #     new_poll.save()
        #     for cf in choice_forms:
        #         new_choice = cf.save(commit=False)
        #         new_choice.Question = new_poll
        #         new_choice.save()
        #     return redirect('poll')
        context = {'poll_form': poll_form, 'choice_forms': choice_forms}
        return render(request, 'poll/edit_poll.html', context)
    def put(self):
        return HttpResponse("put")

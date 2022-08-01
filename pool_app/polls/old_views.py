from django.http import HttpResponseRedirect
# from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .models import Question, Choice

def index(req):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    # template = loader.get_template('polls/index.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    # return HttpResponse(template.render(context, request))
    return render(req, 'polls/index.html', context)

def detail(req, q_id):
    # try:
    #     question = Question.objects.get(pk=q_id)
    # except Question.DoesNotExist:
    #     raise Http404('Question does not exist')

    question = get_object_or_404(Question, pk=q_id)

    return render(req, 'polls/details.html', {'question': question})

def results(req, q_id):
    question = get_object_or_404(Question, pk=q_id)
    
    return render(req, 'polls/results.html', {
        'question': question
    })

def vote(req, q_id):
    question = get_object_or_404(Question, pk=q_id)
    try:
        selected_choice = question.choice_set.get(pk=req.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(req, 'polls/detail.html', {
            'question': question,
            'error_message' : "You didn't select a choice",
        })
    else:
        selected_choice.votes += 1 
        selected_choice.save()

        return HttpResponseRedirect(reverse('polls:results', args=(q_id,)))

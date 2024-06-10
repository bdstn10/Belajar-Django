from typing import Any
from django.db.models.query import QuerySet
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.db.models import F
from django.urls import reverse
from .models import Choice, Question
from django.views import generic
from django.utils import timezone

class IndexView(generic.ListView):
    """
    Return the last five published questions (not including those set to be
    published in the future).
    """
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"
    
    def get_queryset(self):
        question_list = Question.objects.filter(pub_date__lte=timezone.now()).order_by("pub_date")
        question_to_return = [][:5]
        
        # Ensure that only question with choice that is shown on the Index
        for q in question_list:
            if q.choice_set.count() > 0:
                question_to_return.append(q)
            
        return question_to_return
    

class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"
    
    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"
    
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(request, "polls/detail.html", {
            "question": question,
            "error_message": "You didn't select a choice"
        })
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        
        return HttpResponseRedirect(reverse("polls:results", args=(question_id,)))

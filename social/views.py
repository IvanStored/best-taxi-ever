import sweetify
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from social.forms import ThreadForm, MessageForm
from social.models import ThreadModel, MessageModel


class CreateThread(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = ThreadForm()
        context = {"form": form}
        return render(request, "social/create_thread.html", context)

    def post(self, request, *args, **kwargs):
        form = ThreadForm(request.POST)
        username = request.POST.get("username")
        try:
            receiver = get_object_or_404(get_user_model(), username=username)

            if ThreadModel.objects.filter(
                user=request.user, receiver=receiver
            ).exists():
                thread = ThreadModel.objects.filter(
                    user=request.user, receiver=receiver
                )[0]
                return redirect("social:thread", pk=thread.pk)
            elif ThreadModel.objects.filter(
                user=receiver, receiver=request.user
            ).exists():
                thread = ThreadModel.objects.filter(
                    user=receiver, receiver=request.user
                )[0]
                return redirect("social:thread", pk=thread.pk)
            if form.is_valid():
                sender_thread = ThreadModel(
                    user=request.user, receiver=receiver
                )
                sender_thread.save()
                thread_pk = sender_thread.pk
                return redirect("social:thread", pk=thread_pk)
        except Http404:
            sweetify.error(request, "User doesn`t exist!")
            return redirect("social:inbox")


class ListThreads(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        threads = ThreadModel.objects.filter(
            Q(user=request.user) | Q(receiver=request.user)
        )
        form = ThreadForm()

        context = {"threads": threads, "form": form}
        return render(request, "social/inbox.html", context)


class CreateMessage(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        thread = ThreadModel.objects.get(pk=pk)
        if thread.receiver == request.user:
            receiver = thread.user
        else:
            receiver = thread.receiver
        message = MessageModel(
            thread=thread,
            sender_user=request.user,
            receiver_user=receiver,
            body=request.POST.get("message"),
        )
        message.save()
        return redirect("social:thread", pk=pk)


class ThreadView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        form = MessageForm()
        thread = ThreadModel.objects.get(pk=pk)
        message_list = MessageModel.objects.filter(thread__pk__contains=pk)
        context = {
            "thread": thread,
            "form": form,
            "message_list": message_list,
        }
        return render(request, "social/thread.html", context)

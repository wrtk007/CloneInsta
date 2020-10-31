from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Photo
# Create your views here.

class PhotoList(ListView) :
    model = Photo
    template_name_suffix = '_list'

class PhotoCreate(CreateView):
    model = Photo
    fields = ['text', 'image']
    template_name_suffix = '_create'
    success_url = '/'

    def form_valid(self, form) :
        form.instance.author_id = self.request.user.id
        if form.is_valid() : #올바르다면 모델폼은 저장
            form.instance.save()
            return redirect('/')
        else :
            return self.render_to_response({'form' : form})

class PhotoUpdate(UpdateView):
    model = Photo
    fields = ['text', 'image']
    template_name_suffix = '_update'
    
    def dispatch(self, request, *args, **kwargs) :
        object = self.get_object()
        if object.author != request.user :
            messages.warning(request, '수정할 권한이 없습니다.')
            return HttpResponseRedirect('/')
        else :
            return super(PhotoUpdate, self).dispatch(request, *args, **kwargs)


class PhotoDelete(DeleteView) :
    model = Photo
    template_name_suffix = '_delete'
    success_url = '/'

    def dispatch(self, request, *args, **kwargs) :
        object = self.get_object()
        if object.author != request.user :
            messages.warning(request, '삭제할 권한이 없습니다.')
            return HttpResponseRedirect('/')
        else :
            return super(PhotoDelete, self).dispatch(request, *args, **kwargs)

class PhotoDetail(DetailView) :
    model = Photo
    template_name_suffix = '_detail'


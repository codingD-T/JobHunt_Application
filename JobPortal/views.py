from django.shortcuts import render,redirect
import torch
from .classes import Model,Vocabulary
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import nltk
import numpy as np
nltk.download('punkt')
import pickle
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,logout,authenticate
from .forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import os
from twilio.rest import Client
import smtplib

# Create your views here.
def home(request):
    if request.user.is_authenticated:
        companies=Company.objects.all()
        pro = Profile.objects.get(user=request.user)
        temp = pro.bio
        ans = recommend(temp)
        com = []
        comCan = []
        can = []
        setId = []
        userJob = Company.objects.filter(profile__user=request.user)
        for company in companies:
            com.append(company)
            con = Candidates.objects.filter(user_id = request.user.id)
            for c in con:
                setId.append(c)
        print(setId)
        companyExclude = []
        companyExcludeSet = set()
        if len(setId) >0 and len(userJob) >0 :
            companiesCand = setId[0].company.all()
            companyExclude = []
            companyExcludeSet = set()
            for c in companiesCand:
                print(c)
                companyExclude.append(c)
                companyExcludeSet.add(c)
            for c in userJob:
                companyExclude.append(c)
                companyExcludeSet.add(c)
            for ele in ans:
                for i,c in enumerate(companies):
                    if ele[0] == c.position:
                        can.append(c)
                        com.remove(c)
            for i in com:
                can.append(i)
            for c in companyExcludeSet:
                can.remove(c)
            context={
                'companies':can,
            }
            return render(request, 'Jobseeker.html', context)
        elif len(userJob) >0 and len(setId) == 0:
            print("Only Job")
            for c in userJob:
                companyExclude.append(c)
                companyExcludeSet.add(c)
            print(ans)
            for ele in ans:
                for i, c in enumerate(companies):
                    if ele[0] == c.position:
                        can.append(c)
                        com.remove(c)
            for i in com:
                can.append(i)
            for c in companyExcludeSet:

                can.remove(c)

            context = {
                'companies': can,
            }
            return render(request,'Jobseeker.html',context)
        elif len(setId) >0 and len(userJob) == 0:
            print("Holla")
            companiesCand = setId[0].company.all()
            companyExclude = []
            companyExcludeSet = set()
            for c in companiesCand:
                print(c)
                companyExclude.append(c)
                companyExcludeSet.add(c)
            for ele in ans:
                for i, c in enumerate(companies):
                    if ele[0] == c.position:
                        can.append(c)
                        com.remove(c)
            for i in com:
                can.append(i)
            for c in companyExcludeSet:

                can.remove(c)

            context = {
                'companies': can,
            }
            return render(request,'Jobseeker.html',context)
        else:
            for ele in ans:
                for i,c in enumerate(companies):
                    if ele[0] == c.position:
                        can.append(c)
            context = {
                'companies': can
            }
            return render(request, 'Jobseeker.html', context)
    else:
        if request.method == 'POST':
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, f'Account created for {username}!')
                return redirect('login')
        else:
            form = UserRegisterForm()
        return render(request, 'register.html', {'form': form})
        

def logoutUser(request):
    logout(request)
    return redirect('login')


def loginUser(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
       if request.method=="POST":
        name=request.POST.get('username')
        pwd=request.POST.get('password')
        user=authenticate(request,username=name,password=pwd)
        if user is not None:
            login(request,user)
            return redirect('home')
       return render(request,'login.html')

def registerUser(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

# class deleteAccount(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
#     model = User
#     template_name = 'account_confirm_delete.html'
#     success_url = '/'
#     def test_func(self):
#         user = self.get_object()
#         if self.request.user == user.profile.user:
#             return True
#         return False

def deleteAccount(request):
    user = User.objects.get(id = request.user.id)
    print(user)
    return render(request,'account_confirm_delete.html')

def delete(request):
    user = User.objects.get(id=request.user.id)
    print(user)
    user.delete()
    return redirect('register')

@login_required
def applyPage(request,pk):
    form=ApplyForm(instance=request.user.profile)
    #user = User.objects.get(username=request.user.username)
    company1 = Company.objects.get(id = pk)
    if request.method=='POST':
        form=ApplyForm(request.POST,request.FILES)
        if form.is_valid():
            candidates = form.save(commit=False)
            candidates.user = request.user
            candidates.name = request.user.username
            candidates.email = request.user.email
            candidates.save()
            candidates = Candidates.objects.filter(user_id= request.user.id)
            for can in candidates:                
                can.company.add(company1)
            return redirect('home')
    context={'form':form}
    return render(request,'apply.html',context)

@login_required
def profile(request):
    return render(request, 'profile.html')

@login_required
def profileUpdate(request):
    user = User.objects.get(id = request.user.id)
    print(user)
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            user.profile = request.user.profile
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'profileUpdate.html', context)

"""@login_required
def postJob(request):
    form=postForm()
    if request.method=='POST':
        form=postForm(request.POST)
        if form.is_valid():
            #form.instance.author = self.request.user
            form.save()                         
            return redirect('home')
    context={'form':form}
    return render(request,'postjob.html',context)"""

class postjob(LoginRequiredMixin, CreateView):
    model = Company
    fields = ["name","position","description","salary","experience","Location"]
    success_url = '/'
    template_name = 'company_form.html'
    def form_valid(self, form):
        form.instance.username = self.request.user
        form.instance.profile = self.request.user.profile
        return super().form_valid(form)


class jobdetail(DetailView):
    model = Company

class jobupdate(LoginRequiredMixin, UpdateView):
    model = Company
    fields ="__all__"
    template_name = 'company_form.html'
    success_url = '/'
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class jobdelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Company
    template_name = 'job_confirm_delete.html'
    success_url = '/'
    def test_func(self):
        company = self.get_object()
        if self.request.user == company.profile.user:
            return True
        return False
    
@login_required
def applicants(request,pk):
    jobs = ['Project Manager', 'Project Coordinator', 'Marketing Manager', 'Accountant', 'PHP Developer', 'Software Engineer', 'Java Developer', 'Lawyer', 'Administrative Assistant', 'Marketing Specialist', 'Chief Accountant', 'Software Developer', 'QA Engineer', 'Medical Representative', 'Sales Manager', 'Office Manager', 'Web Developer', 'Project Assistant', 'Receptionist/ Administrative Assistant']
    coma = Company.objects.get(id = pk)
    if coma.position not in jobs:
        candidates = Candidates.objects.filter(company__id=pk)
        context = {
            'candidates': candidates,
        }
        return render(request, 'applicants.html', context)

    print("Companies applicants ",coma)
    print(coma.position)
    candidates=Candidates.objects.filter(company__id=pk)
    print("Applicants",candidates)
    dic = {}
    for c in candidates:
        dic[c] = []
        user = c.user
        bio = Profile.objects.get(user=user).bio
        print(user,bio)
        x = recommend(bio)
        for i in range(len(x)):
            print(i)
            dic[c].append(x[i][0])
        print(dic)
    dicPos = {}
    for i,j in dic.items():
        dicPos[i] = dic.get(i,[]).index(coma.position)
    dicPos = dict(sorted(dicPos.items(), key=lambda x: x[1]))
    finList = []
    for i in dicPos.keys():
        finList.append(i)
    context={
        'candidates':finList,
    }        
    return render(request, 'applicants.html',context)

@login_required
def applications(request):
    profile=Profile.objects.get(user=request.user)
    can=Candidates.objects.filter(id=request.user.id)
    print(can)
    companies=Company.objects.filter(candidates__user=request.user)
    print(companies)
    context={
        'companies':companies,
    }
    
    di={}
    for c in companies:
        di[c]=di.get(c,0)+1
    s=di.keys()
    print(s)
    x={"companies":s}
    return render(request, 'applications.html',x)

@login_required
def jobs(request):
    profile = Profile.objects.get(user= request.user)
    print(profile)
    companies=Company.objects.filter(profile= profile)
    context={
        'companies':companies,
    }
    return render(request,'jobs.html',context)

def hireCandidates(request,pk):
    candidate = Candidates.objects.get(id=pk)
    pro = Profile.objects.get(user = candidate.user)
    number = pro.mobile
    print("Mobile number is: ",number)
    candidate.delete()
    return redirect('home')

def call(voca, word):
    if not word in voca:
        return voca['<unk>']
    return voca[word]

def preprocess(st, vocab):
    tokens = nltk.tokenize.word_tokenize(str(st))
    caption = []
    caption.append(call(vocab,'<start>'))
    caption.extend([call(vocab,token) for token in tokens])
    caption.append(call(vocab,'<end>'))
    caption = torch.Tensor(caption)
    return caption

def recommend(st):

    with open(r"words2idx.pkl", "rb") as f:
        voca = pickle.load(f)
    # print(voca)
    # vocab = Vocabulary(voca)
    with open(r"labelsDeploy.pkl", "rb") as f:
        le = pickle.load(f)
    print(le)
    # with open(r"labelEncoder.pkl", "rb") as f:
    #     le = pickle.load(f)
    s = preprocess(st, voca)
    device = torch.device('cpu')
    model = Model(1024, 512, len(voca), 3).to(device)
    model.load_state_dict(torch.load("epoch14.pb", map_location=device))
    # model = torch.load(r"finalModel.pb", map_location=device)
    model.eval()
    with torch.no_grad():
        outputs = model(s.unsqueeze(0).type(torch.LongTensor))
        _, predicted = torch.max(outputs.data, 1)
        finalRes = []
        argFinal = torch.argsort(outputs, descending=True).squeeze(0)
        for i in argFinal:
            l = []
            j = i.numpy().reshape(1)[0]
            l.append(le.get(j))
            finalRes.append(l)
    print(finalRes)
    return finalRes

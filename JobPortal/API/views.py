from django.db.models import Q
from django.contrib.auth import get_user_model
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
import torch
import nltk
import pickle
from django.shortcuts import redirect,render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.parsers import FileUploadParser,FormParser,MultiPartParser
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from ..models import *
from ..classes import Model
from .serializers import *
from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
)

from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin

from rest_framework.generics import (
    CreateAPIView,
    DestroyAPIView,
    ListAPIView,
    UpdateAPIView,
    RetrieveAPIView,
    RetrieveUpdateAPIView
)

from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,

)

from .permissions import IsOwnerOrReadOnly

User = get_user_model()

from .serializers import (
    UserCreateSerializer,
    UserLoginSerializer,
)

class UserAuthentication(ObtainAuthToken):
    def post(self,request,*args,**kwargs):
        serializer = self.serializer_class(data=request.data,context={'request':request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token,created= Token.objects.get_or_create(user=user)
        return Response(token.key)

class UserCreateAPIView(CreateAPIView):
    serializer_class = UserCreateSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

@api_view(http_method_names=['GET'])
@login_required
def jobs(request):
    profile = Profile.objects.get(user= request.user)
    print(profile)
    companies=Company.objects.filter(profile= profile)
    print(companies)
    context={
        'companies':companies,
    }
    serializer_class = CompanyHomeSerializer(companies, many=True)
    print(serializer_class)
    return JsonResponse(serializer_class.data, status=HTTP_200_OK, safe=False)


@api_view(http_method_names=['GET','POST'])
@login_required
def delete(request):
    user = User.objects.get(id=request.user.id)
    print(user)
    user.delete()
    return JsonResponse({"Deleted Account":":("},status=HTTP_200_OK)

@api_view(http_method_names=['POST'])
@login_required
def logoutUser(request):
    logout(request)
    return JsonResponse({"Logged out":":)"},status=HTTP_200_OK)

class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        name = data['username']
        pwd = data['password']
        user = authenticate(request, username=name, password=pwd)
        print("User",user)
        if user is not None:
            login(request, user)
            serializer = UserLoginSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                new_data = serializer.data
                print(new_data)
                return Response(new_data, status=HTTP_200_OK)
        return Response( status=HTTP_400_BAD_REQUEST)

class CompanyHomeAPIView(APIView):
    serializer_class = CompanyHomeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        companies = Company.objects.all()
        pro = Profile.objects.get(user= self.request.user)
        temp = pro.bio
        ans = recommend(temp)
        com = []
        comCan = []
        can = []
        setId = []
        userJob = Company.objects.filter(profile__user=self.request.user)
        for company in companies:
            com.append(company)
            con = Candidates.objects.filter(user_id=self.request.user.id)
            for c in con:
                setId.append(c)
        print(setId)
        companyExclude = []
        companyExcludeSet = set()
        if len(setId) > 0 and len(userJob) > 0:
            print("first")
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
                for i, c in enumerate(companies):
                    if ele[0] == c.position:
                        can.append(c)
                        com.remove(c)
            for i in com:
                can.append(i)
            for c in companyExcludeSet:
                print("Secnd Lst", c)
                can.remove(c)
                print("Last", can)
            print(can)
            context = {
                'companies': can,
            }
            serializer_class = CompanyHomeSerializer(can, many=True)
            print(serializer_class)
            return JsonResponse(serializer_class.data, status=HTTP_200_OK, safe=False)
        elif len(userJob) > 0 and len(setId) == 0:
            print("Second")
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
                print("Secnd Lst", c)
                can.remove(c)
                print("Last", can)
            print(can)
            context = {
                'companies': can,
            }
            serializer_class = CompanyHomeSerializer(can, many=True)
            print(serializer_class)
            return JsonResponse(serializer_class.data, status=HTTP_200_OK, safe=False)
        elif len(setId) > 0 and len(userJob) == 0:
            print("Third")
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
                print("Secnd Lst", c)
                can.remove(c)
                print("Last", can)
            print(can)
            context = {
                'companies': can,
            }
            serializer_class = CompanyHomeSerializer(can, many=True)
            print(serializer_class)
            return JsonResponse(serializer_class.data, status=HTTP_200_OK, safe=False)
        else:
            print("Fourth")
            for ele in ans:
                for i, c in enumerate(companies):
                    if ele[0] == c.position:
                        can.append(c)
            print(can)
            for c in companies:
                if c not in can:
                    can.append(c)
            print(can)
            context = {
                'companies': can
            }
            serializer_class = CompanyHomeSerializer(can, many=True)
            print(serializer_class)
            return JsonResponse(serializer_class.data, status=HTTP_200_OK, safe=False)

class PostJobAPIView(CreateAPIView):
    serializer_class = PostJobSerializer
    queryset = Company.objects.all()
    permission_classes = [IsAuthenticated]

class UpdateProfileAPIView(CreateAPIView):
    serializer_class = UpdateProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [IsAuthenticated]

    # def pre_save(self, obj):
    #     print("Resumeeeeee",)
    #     obj.resume = self.request.FILES.get('file')


class ApplyJobAPIView(RetrieveAPIView):
    queryset = Company.objects.all()
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ApplyJobSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)

@api_view(http_method_names=['POST'])
@parser_classes([MultiPartParser,FileUploadParser])
@login_required
def applyJob(request,pk):
    print("Request Data",request.data)
    print("DATA",request.FILES)
    serializer = ApplyJobSerializer(data=request.data)
    print("hello", serializer)
    serializer.is_valid(raise_exception=True)
    print(serializer.validated_data)
    serializer.save(user= request.user)
    print("hello",serializer.data)
    candidates = Candidates.objects.filter(user_id = request.user.id)
    company1 = Company.objects.get(id=pk)
    for can in candidates:
        can.company.add(company1)
    return Response(status=status.HTTP_201_CREATED)

@api_view(http_method_names=['GET'])
@login_required
def giveProfile(request):
    pro = Profile.objects.filter(user = request.user)
    print(pro[0])
    if len(pro) > 0:
        serializer = GiveProfileSerializer(pro,many=True)
        print(serializer.data)
        return Response(serializer.data, status=HTTP_200_OK)
    # else:
    #     return JsonResponse({"Build Profile":":)"}, status=HTTP_200_OK, safe=False)

@api_view(http_method_names=['GET'])
@login_required
def home(request):
    print("hello")
    companies = Company.objects.all()
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
        con = Candidates.objects.filter(user_id=request.user.id)
        for c in con:
            setId.append(c)
    print(setId)
    companyExclude = []
    companyExcludeSet = set()
    if len(setId) > 0 and len(userJob) > 0:
        print("first")
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
            for i, c in enumerate(companies):
                if ele[0] == c.position:
                    can.append(c)
                    com.remove(c)
        for i in com:
            can.append(i)
        for c in companyExcludeSet:
            print("Secnd Lst", c)
            can.remove(c)
            print("Last", can)
        print(can)
        context = {
            'companies': can,
        }
        serializer_class = CompanyHomeSerializer(can, many=True)
        print(serializer_class)
        return JsonResponse(serializer_class.data, status=HTTP_200_OK, safe=False)
    elif len(userJob) > 0 and len(setId) == 0:
        print("Second")
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
            print("Secnd Lst", c)
            can.remove(c)
            print("Last", can)
        print(can)
        context = {
            'companies': can,
        }
        serializer_class = CompanyHomeSerializer(can, many=True)
        print(serializer_class)
        return JsonResponse(serializer_class.data, status=HTTP_200_OK, safe=False)
    elif len(setId) > 0 and len(userJob) == 0:
        print("Third")
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
            print("Secnd Lst", c)
            can.remove(c)
            print("Last", can)
        print(can)
        context = {
            'companies': can,
        }
        serializer_class = CompanyHomeSerializer(can, many=True)
        print(serializer_class)
        return JsonResponse(serializer_class.data, status=HTTP_200_OK, safe=False)
    else:
        print("Fourth")
        for ele in ans:
            for i, c in enumerate(companies):
                if ele[0] == c.position:
                    can.append(c)
        print(can)
        for c in companies:
            if c not in can:
                can.append(c)
        print(can)
        context = {
            'companies': can
        }
        serializer_class = CompanyHomeSerializer(can, many=True)
        print(serializer_class)
        return JsonResponse(serializer_class.data, status=HTTP_200_OK, safe=False)

    # print(request.user)
    # queryset = Company.objects.all()
    # print(queryset)
    # serializer_class = CompanyHomeSerializer(queryset,many=True)
    # print(serializer_class)
    # return JsonResponse(serializer_class.data,status=HTTP_200_OK,safe=False)

@api_view(http_method_names=['GET'])
@login_required
def applicants(request,pk):
    jobs = ['Project Manager', 'Project Coordinator', 'Marketing Manager', 'Accountant', 'PHP Developer', 'Software Engineer', 'Java Developer', 'Lawyer', 'Administrative Assistant', 'Marketing Specialist', 'Chief Accountant', 'Software Developer', 'QA Engineer', 'Medical Representative', 'Sales Manager', 'Office Manager', 'Web Developer', 'Project Assistant', 'Receptionist/ Administrative Assistant']
    coma = Company.objects.get(id = pk)
    if coma.position not in jobs:
        candidates = Candidates.objects.filter(company__id=pk)
        context = {
            'candidates': candidates,
        }
        serializer_class = ApplicantsSerializer(candidates, many=True)
        print(serializer_class)
        return JsonResponse(serializer_class.data, status=HTTP_200_OK, safe=False)

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
    serializer_class = ApplicantsSerializer(finList,many=True)
    print(serializer_class)
    return JsonResponse(serializer_class.data, status=HTTP_200_OK, safe=False)

@api_view(http_method_names=['GET'])
@login_required
def applications(request):
    profile = Profile.objects.get(user=request.user)
    can = Candidates.objects.filter(id=request.user.id)
    print(can)
    companies = Company.objects.filter(candidates__user=request.user)
    print(companies)
    context = {
        'companies': companies,
    }

    di = {}
    for c in companies:
        di[c] = di.get(c, 0) + 1
    s = di.keys()
    print(s)
    x = {"companies": s}
    serializer_class = ApplicantionSerializer(s,many=True)
    print(serializer_class)
    return JsonResponse(serializer_class.data, status=HTTP_200_OK, safe=False)

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

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.template.context_processors import csrf
from django.contrib.auth import login as auth_login, logout
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .models import *
from django.db.models import Sum, Avg
from django.forms import ModelForm
from django.contrib import messages
import datetime 
import bisect

##########################################################################################
'''
Main view of the system
'''
##########################################################################################
def main_base_view(request):
    dictionary = dict(request=request)
    dictionary.update(csrf(request))    
    return render(request,'main/index.html', dictionary)

##########################################################################################
'''
User Authentication System
'''
##########################################################################################
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request,'main/index.html')
        else:
            msg_to_html = custom_message('Input password salah, lakukan sesuai ketentuan !!!', TagType.danger)
            dictionary = dict(request=request, messages = msg_to_html)
            dictionary.update(csrf(request))            
    else:
        form = UserCreationForm()        
    return render(request,'main/index.html',dictionary)

def login(request):        
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')   
        link1 = request.POST.get('code1')     
        user = authenticate(username=username, password=password)  
        if user is not None:
            auth_login(request=request, user=user)
            dictionary = dict(request=request)
            dictionary.update(csrf(request))
            link.objects.create(username=username,code=link1,date=datetime.datetime.now().strftime ("%Y-%m-%d"))
            date_link = datetime.datetime.now().strftime ("%Y-%m")
            return redirect('survey:survey',link1, date_link)            
        else:
            msg_to_html = custom_message('Anda tidak terdaftar', TagType.danger)
            dictionary = dict(request=request, messages = msg_to_html)
            dictionary.update(csrf(request))
        return render(request,'main/index.html',dictionary)

def update_pwd(username, pwd):
    user_model = User.objects.get(username=username)
    user_model.set_password(pwd)
    user_model.save()

def logout_view(request):
    logout(request)
    dictionary = dict(request=request)
    dictionary.update(csrf(request))
    return render(request,'main/index.html', dictionary)

##########################################################################################
'''
This code for manage the 'wilayah' table, use case of code (CRUD)
'''
##########################################################################################
class SubwilForm(ModelForm):
    class Meta:
        model = subwil
        fields = ['kode', 'wilayah']

def wilayah(request):  
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')                
        user = authenticate(username=username, password=password)    
        if user is not None:
            auth_login(request=request, user=user)
            dictionary = dict(request=request)
            dictionary.update(csrf(request))
            return redirect('survey:wilayah_list')            
        else:
            msg_to_html = custom_message('Anda tidak terdaftar', TagType.danger)
            dictionary = dict(request=request, messages = msg_to_html)
            dictionary.update(csrf(request))
        return render(request,'main/index.html',dictionary)      
    
def wilayah_list(request, template_name='main/wilayah/wilayah_list.html'):
    Subwil = subwil.objects.all()
    data = {}
    data['object_list'] = Subwil
    return render(request, template_name, data)

def wilayah_create(request, template_name='main/wilayah/wilayah_form.html'):
    form = SubwilForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('survey:wilayah_list')
    return render(request, template_name, {'form':form})

def wilayah_update(request, pk, template_name='main/wilayah/wilayah_form.html'):
    Subwil= get_object_or_404(subwil, pk=pk)
    form = SubwilForm(request.POST or None, instance=Subwil)
    if form.is_valid():
        form.save()
        return redirect('survey:wilayah_list')
    return render(request, template_name, {'form':form})

def wilayah_delete(request, pk, template_name='main/wilayah/wilayah_confirm_delete.html'):
    Subwil= get_object_or_404(subwil, pk=pk)    
    if request.method=='POST':
        Subwil.delete()
        return redirect('survey:wilayah_list')
    return render(request, template_name, {'object':Subwil})

##########################################################################################
'''
This code for manage the survey system
'''
##########################################################################################
def survey(request, link1, date_link):    
    link_count = subwil.objects.filter(kode=link1).count()   
    message = None
    if link_count == 0:
        msg_to_html = custom_message('Kode wilayah tidak terdaftar', TagType.danger)
        dictionary = dict(request=request, messages = msg_to_html)
        dictionary.update(csrf(request))
        return render(request,'main/index.html', dictionary)
    
    else :
        dictionary = dict(request=request)
        dictionary.update(csrf(request)) 
        wilayah = subwil.objects.filter(kode=link1)[0]

    if request.method == 'POST':
        name = request.POST.get('name')
        nip = request.POST.get('NIP')
        sex = request.POST.get('sex')
        age = request.POST.get('age')
        study = request.POST.get('quality[25]')
        job = request.POST.get('quality[21]')

        U1 = (request.POST.get('quality[1]'))
        U2 = (request.POST.get('quality[2]'))
        U3 = (request.POST.get('quality[3]'))
        U4 = (request.POST.get('quality[4]'))
        U5 = (request.POST.get('quality[5]'))
        U6 = (request.POST.get('quality[6]'))
        U7 = (request.POST.get('quality[7]'))
        U8 = (request.POST.get('quality[8]'))
        U9 = (request.POST.get('quality[9]'))
        U10 = (request.POST.get('quality[10]'))
        U11 = (request.POST.get('quality[11]'))
        U12 = (request.POST.get('quality[12]'))
        U13 = (request.POST.get('quality[13]'))
        U14 = (request.POST.get('quality[14]'))
        
        if name is None or nip is None or sex is None or age is None or study is None or job is None :
            message = str('Data tidak lengkap !!!')

        
        if U1 is None or U2 is None or U3 is None or U4 is None or U5 is None or U6 is None or U7 is None or U8 is None or U9 is None or U10 is None or U11 is None or U12 is None or U13 is None or U14 is None:
            message = str('Data tidak lengkap !!!')
        

        else :            
            comp_date = datetime.datetime.now().strftime ("%Y-%m")

            if comp_date == date_link:
                comp_nip = koresponden.objects.filter(NIP=nip).count()
                if comp_nip == 0:
                    koresponden.objects.create(name=name,NIP=nip,sex=sex,
                    age=age,study=study,job=job,code=link1,
                    date=datetime.datetime.now().strftime ("%Y-%m-%d"))
                            
                    data.objects.create(NIP=nip,U1=U1,U2=U2,U3=U3,U4=U4,
                    U5=U5,U6=U6,U7=U7,U8=U8,U9=U9,U10=U10,U11=U11,
                    U12=U12,U13=U13,U14=U14,code=link1,
                    date=datetime.datetime.now().strftime ("%Y-%m-%d"))                      
                else :                             
                    message = str('Anda sudah pernah melakukan survey ini !!!')               
                    
            else:   
                message = str('Waktu survey sudah berakhir !!!')             

    return render(request, 'main/survey.html',{'wilayah': wilayah, 'message':message})

##########################################################################################
'''
This code for view the result of survey
'''
##########################################################################################
def main(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        date = request.POST.get('date')        

        if code == ('') or date == (''):
            msg_to_html = custom_message('Masukan data salah !!!', TagType.danger)
            dictionary = dict(request=request, messages = msg_to_html)
            dictionary.update(csrf(request))
            return render(request,'main/index.html', dictionary)

        else :
            x = date.split("-")
            print(date)
            year = x[0]
            month = x[1]

            ########Data Survey##########                
            comp_data = data.objects.filter(code=code,date__year=year,date__month=month)
            count_data = data.objects.filter(code=code,date__year=year,date__month=month).count()

            #######Data Koresponden#########
            count_L = koresponden.objects.filter(code=code,date__year=year,date__month=month,sex='L').count()
            count_P = koresponden.objects.filter(code=code,date__year=year,date__month=month,sex='P').count()

            count_SLTP = koresponden.objects.filter(code=code,date__year=year,date__month=month,study='SLTP').count()
            count_SLTA = koresponden.objects.filter(code=code,date__year=year,date__month=month,study='SLTA').count()
            count_D1 = koresponden.objects.filter(code=code,date__year=year,date__month=month,study='D1').count()
            count_D2 = koresponden.objects.filter(code=code,date__year=year,date__month=month,study='D2').count()
            count_D3 = koresponden.objects.filter(code=code,date__year=year,date__month=month,study='D3').count()
            count_S1 = koresponden.objects.filter(code=code,date__year=year,date__month=month,study='S1').count()
            count_S2 = koresponden.objects.filter(code=code,date__year=year,date__month=month,study='S2').count()
            count_S3 = koresponden.objects.filter(code=code,date__year=year,date__month=month,study='S3').count()

            count_Mahasiswa = koresponden.objects.filter(code=code,date__year=year,date__month=month,job='Mahasiswa').count()
            count_Swasta = koresponden.objects.filter(code=code,date__year=year,date__month=month,job='Swasta').count()
            count_PNS = koresponden.objects.filter(code=code,date__year=year,date__month=month,job='PNS').count()
            count_Wiraswasta = koresponden.objects.filter(code=code,date__year=year,date__month=month,job='Wiraswasta').count()
            count_BUMN = koresponden.objects.filter(code=code,date__year=year,date__month=month,job='BUMN').count()
            count_Lainnya = koresponden.objects.filter(code=code,date__year=year,date__month=month,job='Lainnya').count()
            
            r1,r2,r3,r4,r5,r6,r7,r8 = 20,21,30,31,40,41,50,51
            count_age1 = koresponden.objects.filter(code=code,date__year=year,date__month=month,age__lte=r1).count()
            count_age2 = koresponden.objects.filter(code=code,date__year=year,date__month=month,age__gte=r2,age__lte=r3).count()
            count_age3 = koresponden.objects.filter(code=code,date__year=year,date__month=month,age__gte=r4,age__lte=r5).count()
            count_age4 = koresponden.objects.filter(code=code,date__year=year,date__month=month,age__gte=r6,age__lte=r7).count()
            count_age5 = koresponden.objects.filter(code=code,date__year=year,date__month=month,age__gte=r8).count()
            
            if count_data != 0 :
                #nilai unsur
                U1 = comp_data.aggregate(Sum('U1'))
                U2 = comp_data.aggregate(Sum('U2'))
                U3 = comp_data.aggregate(Sum('U3'))
                U4 = comp_data.aggregate(Sum('U4'))
                U5 = comp_data.aggregate(Sum('U5'))
                U6 = comp_data.aggregate(Sum('U6'))
                U7 = comp_data.aggregate(Sum('U7'))
                U8 = comp_data.aggregate(Sum('U8'))
                U9 = comp_data.aggregate(Sum('U9'))
                U10 = comp_data.aggregate(Sum('U10'))
                U11 = comp_data.aggregate(Sum('U11'))
                U12 = comp_data.aggregate(Sum('U12'))
                U13 = comp_data.aggregate(Sum('U13'))
                U14 = comp_data.aggregate(Sum('U14'))

                #rata-rata unsur
                U1_avg = comp_data.aggregate(Avg('U1'))
                U2_avg = comp_data.aggregate(Avg('U2'))
                U3_avg = comp_data.aggregate(Avg('U3'))
                U4_avg = comp_data.aggregate(Avg('U4'))
                U5_avg = comp_data.aggregate(Avg('U5'))
                U6_avg = comp_data.aggregate(Avg('U6'))
                U7_avg = comp_data.aggregate(Avg('U7'))
                U8_avg = comp_data.aggregate(Avg('U8'))
                U9_avg = comp_data.aggregate(Avg('U9'))
                U10_avg = comp_data.aggregate(Avg('U10'))
                U11_avg = comp_data.aggregate(Avg('U11'))
                U12_avg = comp_data.aggregate(Avg('U12'))
                U13_avg = comp_data.aggregate(Avg('U13'))
                U14_avg = comp_data.aggregate(Avg('U14'))

                #Terbagi unsur
                k=0.071
                U1_tpu = U1_avg['U1__avg'] * k
                U2_tpu = U2_avg['U2__avg'] * k
                U3_tpu = U3_avg['U3__avg'] * k
                U4_tpu = U4_avg['U4__avg'] * k
                U5_tpu = U5_avg['U5__avg'] * k
                U6_tpu = U6_avg['U6__avg'] * k
                U7_tpu = U7_avg['U7__avg'] * k
                U8_tpu = U8_avg['U8__avg'] * k
                U9_tpu = U9_avg['U9__avg'] * k
                U10_tpu = U10_avg['U10__avg'] * k
                U11_tpu = U11_avg['U11__avg'] * k
                U12_tpu = U12_avg['U12__avg'] * k
                U13_tpu = U13_avg['U13__avg'] * k
                U14_tpu = U14_avg['U14__avg'] * k

                #Jumlah terbagi unsur            
                sum_U_tpu =  U1_tpu + U2_tpu + U3_tpu + U4_tpu + U5_tpu + U6_tpu + U7_tpu 
                + U8_tpu + U9_tpu + U10_tpu + U11_tpu + U12_tpu + U13_tpu + U14_tpu

                #Nilai ikm_mutu =_pelayanan
                ikm_mutu_pelayanan = round(sum_U_tpu*25, 2)
                
                #Grade mutu pelayanan
                mutu_pelayanan = check_grade(ikm_mutu_pelayanan)

                #Data chart untuk tiap unsur
                chart_labels = ["U1","U2","U3","U4","U5","U6","U7","U8","U9","U10","U11","U12","U13","U14"]            
                #Data
                chart_data_val = [U1_avg['U1__avg'], U2_avg['U2__avg'], U3_avg['U3__avg'], U4_avg['U4__avg'], U5_avg['U5__avg'], U6_avg['U6__avg']
                , U7_avg['U7__avg'], U8_avg['U8__avg'], U9_avg['U9__avg'], U10_avg['U10__avg'], U11_avg['U11__avg'], U12_avg['U12__avg'], 
                U13_avg['U13__avg'], U14_avg['U14__avg']]
                #Sum data
                tot = sum(chart_data_val)
                #Chart data
                chart_data = []
                for i in chart_data_val:
                    percent = round(i/tot*100,2)
                    chart_data.append(percent)
                
            else:
                ikm_mutu_pelayanan = 0
                mutu_pelayanan = 0
                chart_data = []
                chart_labels = []

            wilayah = subwil.objects.filter(kode=code)[0]
            ###########
            context = {
                'L': count_L, 
                'P': count_P,
                'SLTP': count_SLTP,
                'SLTA': count_SLTA,
                'D1': count_D1,
                'D2': count_D2,
                'D3': count_D3,
                'S1': count_S1,
                'S2': count_S2,
                'S3': count_S3,
                'job1': count_Mahasiswa,
                'job2': count_Swasta,
                'job3': count_PNS,
                'job4': count_Wiraswasta,
                'job5': count_BUMN,
                'job6': count_Lainnya,
                'age1': count_age1,
                'age2': count_age2,
                'age3': count_age3,
                'age4': count_age4,
                'age5': count_age5,
                'ikm': ikm_mutu_pelayanan,
                'mutu': mutu_pelayanan,
                'total': count_data,
                'labels': chart_labels,
                'data': chart_data,
                'wilayah':wilayah
                }
            
        ###########                     
        return render(request,'main/index.html', context)

def check_grade(scores, breakpoints=[25, 43.76, 62.51, 81.26], grades='DCBA'):
    i = bisect.bisect(breakpoints, scores)
    return grades[i]

##########################################################################################
'''
Message class for system response
'''
##########################################################################################
class Messages:
    def __init__(self):
        self.message = ''

    message = ''
    tag = ''

def custom_message(message, tag):
    # 1.- success, 2.-info, 3.- warning 4.- danger
    msg = Messages()
    if tag == 0:
        msg.tag = "alert alert-success"
    elif tag == 1:
        msg.tag = "alert alert-info"
    elif tag == 2:
        msg.tag = "alert alert-warning"
    else:
        msg.tag = "alert alert-danger"

    msg.message = message
    return msg

class TagType:
    def __init__(self):
        pass

    success, info, warning, danger = range(4)

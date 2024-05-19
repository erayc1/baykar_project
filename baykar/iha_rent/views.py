import json
from django.shortcuts import redirect, render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
from django.contrib.auth.hashers import make_password, check_password
from django.views.decorators.csrf import csrf_exempt
from iha_rent.models import IhaDetails, RentRecords, Users
from django.db.models import Q 
from datetime import datetime
from django.contrib.auth.decorators import login_required


#Kullanıcı logout işlem
@csrf_exempt
def logout(request):
    if request.method == 'POST':
        if 'user_id' in request.session:
            del request.session['user_id']
        return JsonResponse({'success': True, 'message': 'Logged out successfully'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

#Admin logout işlem
@csrf_exempt
def admin_logout(request):
    if request.method == 'POST':
        if 'user_id' in request.session:
            del request.session['admin_user_id']
        return JsonResponse({'success': True, 'message': 'Logged out successfully'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

#Kullanıcı anasayfa işlem
def index(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return render(request, 'login.html')
    return render(request, 'index.html')

def admin_login(request):

    return render(request, 'admin.html')

def admin_register(request):

    return render(request, 'admin_register.html')

def admin_home(request):
    if not request.session.get('admin_user_id'):
        return render(request,'admin.html')
    return render(request, 'admin_home.html')



def admin_iha_add(request):
    if not request.session.get('admin_user_id'):
        return render(request,'admin.html')
    return render(request, 'admin_iha_add.html')

def signUp(request):
    
    return render(request, 'signUp.html')

def login(request):
    return render(request, 'login.html')


#Admin login işlemleri fonksiyonu
@api_view(['POST'])
def admin_login_api(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    # Kullanıcıyı veritabanında ara
    try:
        user = Users.objects.get(email=email)
        
        
        # Şifreyi kontrol et
        if (user.password == password and user.is_admin == True):
            request.session['admin_user_id'] = user.id

            return JsonResponse({'success': True, 'message': 'Login successful'})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid credentials1'})
    except Users.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Invalid credentials2'})

#Kullanıcı login işlemleri fonksiyonu
@api_view(['POST'])
def user_login_api(request):
    email = request.data.get('email')
    password = request.data.get('password')
    
    # Kullanıcıyı veritabanında ara
    try:
        user = Users.objects.get(email=email)
        
        # Şifreyi kontrol et
        if (password== user.password and user.is_admin == False):
            request.session['user_id'] = user.id
            return JsonResponse({'success': True, 'message': 'Login successful'})
        else:
            return JsonResponse({'success': False, 'message': 'Invalid credentials1'})
    except Users.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Invalid credentials2'})
    


#Kullanıcı kayıt işlemleri fonksiyonu
@api_view(['POST'])
def user_signUp_api(request):
    name = request.data.get('name')
    surname = request.data.get('surname')
    email = request.data.get('email')
    password = request.data.get('password')

    # Kullanıcıyı veritabanında ara
    try:
        user = Users.objects.get(email=email)
        
        return JsonResponse({'success': False, 'message': 'Böyle bir kullanıcı zaten var.'})
    except Users.DoesNotExist:
        # Kullanıcı mevcut değilse yeni bir kullanıcı oluştur
        hashed_password = make_password(password)
        new_user = Users.objects.create(email=email, password=password, name=name, surname=surname)
        request.session['user_id'] = new_user.id
        
        return JsonResponse({'success': True, 'message': 'Kullanıcı başarıyla oluşturuldu.'})

#Admin kayıt işlemleri fonksiyonu    
@api_view(['POST'])
def admin_register_api(request):
    name = request.data.get('name')
    surname = request.data.get('surname')
    email = request.data.get('email')
    password = request.data.get('password')
    is_admin = request.data.get('is_admin', False)

    try:
        user = Users.objects.get(email=email)
        return JsonResponse({'success': False, 'message': 'Böyle bir kullanıcı zaten var.'})
    except Users.DoesNotExist:
        new_admin_user = Users.objects.create(
            email=email,
            password=password,
            name=name,
            surname=surname,
            is_admin=is_admin
        )
        request.session['admin_user_id'] = new_admin_user.id
        return JsonResponse({'success': True, 'message': 'Kullanıcı başarıyla oluşturuldu.'})


#Admin anasayfada kullanıcı bilgileri görüntüleme fonksiyonu
@csrf_exempt
def users_data(request):
    draw = int(request.POST.get('draw'))
    start = int(request.POST.get('start'))
    length = int(request.POST.get('length'))
    search_value = request.POST.get('search[value]')

    query = Users.objects.all()
    if search_value:
        query = query.filter(email__icontains=search_value) | query.filter(name__icontains=search_value) | query.filter(surname__icontains=search_value)

    total = query.count()
    data = query[start:start+length]

    response = {
        'draw': draw,
        'recordsTotal': total,
        'recordsFiltered': total,
        'data': list(data.values('email', 'name', 'surname', 'is_admin'))
    }

    return JsonResponse(response)


#Admin anasayfada iha bilgileri görüntüleme fonksiyonu - Kullanıcı iha ekleme fonkiyonunda iha bilgileri görüntüleme fonksiyonu
@csrf_exempt
def iha_data(request):
    draw = int(request.POST.get('draw'))
    start = int(request.POST.get('start'))
    length = int(request.POST.get('length'))
    search_value = request.POST.get('search[value]')

    query = IhaDetails.objects.all()
    if search_value:
        query = query.filter(brand__icontains=search_value) | query.filter(model__icontains=search_value) | query.filter(category__icontains=search_value) | query.filter(height__icontains=search_value)

    total = query.count()
    data = query[start:start+length]

    response = {
        'draw': draw,
        'recordsTotal': total,
        'recordsFiltered': total,
        'data': list(data.values('brand', 'model', 'category', 'height', 'id'))
    }

    return JsonResponse(response)


#Tüm iha bilgilerini getirir
@csrf_exempt
def get_all_ihas(request):
    if request.method == 'GET':
        iha_records = IhaDetails.objects.all()
        data = list(iha_records.values('id', 'brand', 'model', 'category', 'height'))
        return JsonResponse({'success': True, 'data': data})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})



#Admin sayfasında kiralanan iha bilgilerini göster
@csrf_exempt
def rent_data(request):
    draw = int(request.POST.get('draw'))
    start = int(request.POST.get('start'))
    length = int(request.POST.get('length'))
    search_value = request.POST.get('search[value]')

    query = RentRecords.objects.all()
    if search_value:
        query = query.filter(
            Q(user_id__icontains=search_value) |
            Q(iha_id__icontains=search_value) |
            Q(start_date__icontains=search_value) |
            Q(end_date__icontains=search_value)
        )

    total = query.count()
    data = query[start:start + length]

    records = []
    for record in data:
        try:
            iha_details = IhaDetails.objects.get(id=record.iha_id)
            records.append({
                'user_id': record.user_id,
                'iha_id': record.iha_id,
                'brand': iha_details.brand,
                'model': iha_details.model,
                'start_date': record.start_date.strftime("%Y-%m-%d %H:%M:%S"),
                'end_date': record.end_date.strftime("%Y-%m-%d %H:%M:%S"),
                'id': record.id
            })
        except IhaDetails.DoesNotExist:
            records.append({
                'user_id': record.user_id,
                'iha_id': record.iha_id,
                'brand': 'Unknown',
                'model': 'Unknown',
                'start_date': record.start_date.strftime("%Y-%m-%d %H:%M:%S"),
                'end_date': record.end_date.strftime("%Y-%m-%d %H:%M:%S"),
                'id': record.id
            })

    response = {
        'draw': draw,
        'recordsTotal': total,
        'recordsFiltered': total,
        'data': records
    }

    return JsonResponse(response)



#Kullanıcı sayfasında kiralanan iha bilgilerini göster
@csrf_exempt
def user_rent_data(request):
    draw = int(request.POST.get('draw'))
    start = int(request.POST.get('start'))
    length = int(request.POST.get('length'))
    search_value = request.POST.get('search[value]')

    user_id = request.session.get('user_id')
    if not user_id:
        return JsonResponse({
            'draw': draw,
            'recordsTotal': 0,
            'recordsFiltered': 0,
            'data': [],
            'message': 'User not logged in'
        })

    query = RentRecords.objects.filter(user_id=user_id)
    if search_value:
        query = query.filter(
            Q(iha_id__icontains=search_value) |
            Q(start_date__icontains=search_value) |
            Q(end_date__icontains=search_value)
        )

    total = query.count()
    data = query[start:start + length]

    records = []
    for record in data:
        try:
            iha_details = IhaDetails.objects.get(id=record.iha_id)
            records.append({
                'user_id': record.user_id,
                'iha_id': record.iha_id,
                'brand': iha_details.brand,
                'model': iha_details.model,
                'start_date': record.start_date.strftime("%Y-%m-%d %H:%M:%S"),
                'end_date': record.end_date.strftime("%Y-%m-%d %H:%M:%S"),
                'id': record.id
            })
        except IhaDetails.DoesNotExist:
            records.append({
                'user_id': record.user_id,
                'iha_id': record.iha_id,
                'brand': 'Unknown',
                'model': 'Unknown',
                'start_date': record.start_date.strftime("%Y-%m-%d %H:%M:%S"),
                'end_date': record.end_date.strftime("%Y-%m-%d %H:%M:%S"),
                'id': record.id
            })

    response = {
        'draw': draw,
        'recordsTotal': total,
        'recordsFiltered': total,
        'data': records
    }

    return JsonResponse(response)


#Admin yeni IHA ekleme fonksiyonu
@api_view(['POST'])
def admin_iha_add_api(request):
    model = request.data.get('model')
    brand = request.data.get('brand')
    category = request.data.get('category')
    height = request.data.get('height')
    
    # Kullanıcıyı veritabanında ara
    try:
        brand = IhaDetails.objects.create(model = model ,brand=brand, category=category, height=height)
        
        
        return JsonResponse({'success': True, 'message': 'Create successful'})
       
    except Users.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Create failed'})
    


#Kullanıcı yeni IHA kiralama fonksiyonu
@csrf_exempt
def add_rent_record(request):
    if request.method == 'POST':
        user_id = request.session.get('user_id')
        if not user_id:
            return JsonResponse({'success': False, 'message': 'User not logged in'})

        data = json.loads(request.body)
        iha_id = data.get('id')
        start_date_str = data.get('start_date')
        end_date_str = data.get('end_date')

        date_format = "%Y-%m-%d %H:%M:%S"
        try:
            start_date = datetime.strptime(start_date_str, date_format)
            end_date = datetime.strptime(end_date_str, date_format)
        except ValueError:
            return JsonResponse({'success': False, 'message': 'Invalid date format'})

        new_record = RentRecords(
            user_id=user_id,
            iha_id=iha_id,
            start_date=start_date,
            end_date=end_date
        )
        new_record.save()
        
        return JsonResponse({'success': True, 'message': 'Rent record added successfully'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

#Kullanıcı kiralanan iha silme fonksiyonu
@csrf_exempt
def delete_rent_record(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        record_id = data.get('id')
        
        try:
            record = RentRecords.objects.get(id=record_id)
            record.delete()
            return JsonResponse({'success': True, 'message': 'Record deleted successfully'})
        except RentRecords.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Record not found'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

#Kullanıcı kiralanan iha düzenleme fonksiyonu
@csrf_exempt
def update_rent_record(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        record_id = data.get('id')
        user_id = data.get('user_id')
        iha_id = data.get('iha_id')
        start_date_str = data.get('start_date')
        end_date_str = data.get('end_date')

        date_format = "%Y-%m-%d %H:%M:%S"
        try:
            start_date = datetime.strptime(start_date_str, date_format)
            end_date = datetime.strptime(end_date_str, date_format)
        except ValueError:
            return JsonResponse({'success': False, 'message': 'Invalid date format'})

        try:
            record = RentRecords.objects.get(id=record_id)
            record.user_id = user_id
            record.iha_id = iha_id
            record.start_date = start_date
            record.end_date = end_date
            record.save()
            return JsonResponse({'success': True, 'message': 'Record updated successfully'})
        except RentRecords.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Record not found'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})


#Admin eklenen iha düzenleme fonksiyonu
@csrf_exempt
def update_iha(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        iha_id = data.get('id')
        brand = data.get('brand')
        model = data.get('model')
        category = data.get('category')
        height = data.get('height')

        try:
            iha = IhaDetails.objects.get(id=iha_id)
            iha.brand = brand
            iha.model = model
            iha.category = category
            iha.height = height
            iha.save()
            return JsonResponse({'success': True, 'message': 'IHA updated successfully'})
        except IhaDetails.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'IHA not found'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

#Admin eklenen iha silme fonksiyonu
@csrf_exempt
def delete_iha(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        iha_id = data.get('id')

        try:
            iha = IhaDetails.objects.get(id=iha_id)
            iha.delete()
            return JsonResponse({'success': True, 'message': 'IHA deleted successfully'})
        except IhaDetails.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'IHA not found'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})




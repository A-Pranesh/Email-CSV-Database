import json
import csv
import re

from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render
from .models import Student
from django.core.mail import send_mail
from django.utils.encoding import smart_str

def try_rest_framework(request, id):
    if request.method == 'GET':
        return get(request, id)
    elif request.method == 'POST':
        return post(request)
    elif request.method == 'PUT':
        return put(request, id)
    elif request.method == 'DELETE':
        return delete(request, id)

def get(request, id=None):
    if id:
        try:
            data = serializers.serialize("json", Student.objects.filter(id=id))
            return HttpResponse(data)
        except:
            return HttpResponse('No record found')
    data = serializers.serialize("json", Student.objects.all())
    return HttpResponse(data)

def post(request):
    data = json.loads(request.body.decode('utf-8'))
    obj = Student()
    obj.name = data['name']
    obj.age = data['age']
    obj.email = data['email']
    obj.save()
    return HttpResponse('Student saved successfully')

def put(request, id=None):
    data = json.loads(request.body.decode('utf-8'))
    try:
        obj = Student.objects.get(id=id)
        obj.update(name=data['name'])
        return HttpResponse('Student updated successfully')
    except:
        return HttpResponse('No record found')

def delete(request, id=None):
    try:
        obj = Student.objects.get(id=id)
        obj.delete()
        return HttpResponse('Student deleted successfully')
    except:
        return HttpResponse('No record found')

def send_email(request):
    try:
        send_mail('Simple Mail',
                  'This is a sample SMTP message',
                  'pranesh24599@gmail.com',
                  ['viperpranesh007@gmail.com'],
                  )
        return HttpResponse("Email send successfully")
    except:
        return HttpResponse("Unable to send mail")

def database_to_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=mymodel.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8')) # BOM (optional...Excel needs it to open UTF-8 file properly)
    writer.writerow([
        smart_str(u"ID"),
        smart_str(u"Name"),
        smart_str(u"Age"),
        smart_str(u"EmailID"),
    ])
    queryset = Student.objects.all()
    for obj in queryset:
        writer.writerow([
            smart_str(obj.pk),
            smart_str(obj.name),
            smart_str(obj.age),
            smart_str(obj.email),
        ])
    return response

def csv_to_database(request):
    with open('sample_data.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            obj = Student(name=row['name'], age=row['age'], email=row['email'])
            obj.save()
    return HttpResponse('Saved to database successfully!')

def csv_to_database_with_validation(request):
    li = []
    count = 0
    regex = re.compile('[a-zA-Z0-9!@#$%^&*_]+')
    with open('sample_data.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            count += 1
            if regex.search(row['name']) and regex.search(row['age']) and regex.search(row['email']):
                obj = Student(name=row['name'], age=row['age'], email=row['email'])
                obj.save()
            else:
                li.append(count)
    print(li)
    return HttpResponse('Saved to database successfully!')
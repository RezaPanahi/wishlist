from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages
import bcrypt



def index(request):
    return render(request, 'index.html')

def register(request):
    errors = User.objects.regValidator(request.POST)
    print(request.POST)
    print()
    print()
    print()

    if errors:
        for key, value in errors.items():
            messages.error(request,value, extra_tags=key)
        print(errors)
        return redirect('/')
    else:
        hash = bcrypt.hashpw(request.POST['reg_password'].encode(), bcrypt.gensalt())
        user = User.objects.create(name=request.POST['name'], username=request.POST['username'], password=hash.decode(), date_hired=request.POST['date_hired'])

        request.session['id'] = user.id
    return redirect('/')


def login(request):
    result = User.objects.loginValidator(request.POST)
    if result[0]:
        for key, value in result[0].items():
            messages.error(request, value, extra_tags=key)
        return redirect('/')
    else:
        request.session['id'] = result[1].id
        return redirect('/dashboard')

def dashboard(request):
    logged_user = User.objects.get(id=request.session['id'])
    items = wishList.objects.filter(add_other_user_item_to_wishlist=request.session['id'])
    loggedUserItem = wishList.objects.exclude(add_other_user_item_to_wishlist=request.session['id'])
    context = {
        'logged_user': logged_user,
        'items': items,
        'loggedUserItem': loggedUserItem
    }


    return render(request, 'dashboard.html', context)

def createItemPage(request):


    print(request.POST)
    print()
    print()
    print()
    # print(errors)
    return render(request, 'create.html')

def afterItemCreation(request):
    errors = wishList.objects.wishListValidator(request.POST)

    if errors:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect('wish_item/create')
    else:
        added_item = wishList.objects.create(item=request.POST['item'], added_by_id = request.session['id'])
        print(request.POST)

        return redirect('/dashboard')

def wish_items(request, item_id):
    item = wishList.objects.get(id=item_id)
    users = item.add_other_user_item_to_wishlist.all()
    context = {
        'item': item,
        'users': users,
    }
    return render(request, 'wish_items.html', context)

def removeItem(request, item_id):
    item = wishList.objects.get(id=item_id)
    user = User.objects.get(id=request.session['id'])
    user.other_user_item_added.remove(item)
    return redirect('/dashboard')

def addOtherUserItem(request, item_id):
    item = wishList.objects.get(id=item_id)
    user = User.objects.get(id=request.session['id'])
    user.other_user_item_added.add(item)
    return redirect('/dashboard')

def delete(request, item_id):
    item = wishList.objects.get(id=item_id)
    item.delete()
    return redirect('/dashboard')


def logout(request):
    request.session.clear()
    return redirect('/')

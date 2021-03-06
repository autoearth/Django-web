from django.shortcuts import render, redirect
from django.http import HttpResponse  #(เป็น function ที่โชว์ข้อมูลหน้าเว็บได้)
from .models import *
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from datetime import datetime

from django.core.paginator import Paginator


def Home(request):
	product = AllProduct.objects.all().order_by('id').reverse()[:3]
	preorder = AllProduct.objects.filter(quantity__lte=0)
	context = {'product': product, 'preorder': preorder}
	return render(request,'myapp/home.html', context)

def About(request):
	return render(request, 'myapp/about.html')

def Contact(request):
	return render(request, 'myapp/contact.html')

def Zasumi(request):
	return render(request, 'myapp/zasumi.html')

def Addproduct(request):

	if request.user.profile.usertype != 'admin':
		return redirect('home-page')


	if request.method == 'POST' and request.FILES['imageupload']:
		data = request.POST.copy()
		name = data.get('name')
		price = data.get('price')
		detail = data.get('detail')
		imageurl = data.get('imageurl')
		quantity = data.get('quantity')
		unit = data.get('unit')

		new = AllProduct()
		new.name = name
		new.price = price
		new.detail = detail
		new.imageurl = imageurl
		new.quantity = quantity
		new.unit = unit

		file_image = request.FILES['imageupload']
		file_image_name = request.FILES['imageupload'].name.replace(' ', '')
		print('FILE_IMAGE:', file_image)
		print('IMAGE_NAME:', file_image_name)
		fs = FileSystemStorage()
		filename = fs.save(file_image_name, file_image)
		upload_file_url = fs.url(filename)
		new.image = upload_file_url[6:]

		new.save()


	return render(request, 'myapp/addproduct.html')

def Product(request):
	product = AllProduct.objects.all().order_by('id').reverse()
	paginator = Paginator(product,2)
	page = request.GET.get('page')
	product = paginator.get_page(page)
	context = {'product': product}
 
	return render(request, 'myapp/allproduct.html', context)


def Register(request):
	if request.method == 'POST':
		data = request.POST.copy()
		first_name = data.get('first_name')
		last_name = data.get('last_name')
		email = data.get('email')
		password = data.get('password')

		newuser = User()
		newuser.username = email
		newuser.email = email
		newuser.first_name = first_name
		newuser.last_name = last_name
		newuser.set_password(password)
		newuser.save()

		profile = Profile()
		profile.user = User.objects.get(username=email)
		profile.save()

		user = authenticate(username=email, password=password)
		login(request,user)
	return render(request, 'myapp/register.html')



def AddtoCart(request,pid):
	
	print('CURRENT USER:', request.user)
	username = request.user.username
	user = User.objects.get(username=username)
	check = AllProduct.objects.get(id=pid)
	
	try:
		# กรณีที่สินค้าซ้ำกัน
		newcart = Cart.objects.get(user=user, productid=str(pid))
		newquan = newcart.quantity + 1
		newcart.quantity = newquan
		calculate = newcart.price * newquan 
		newcart.total = calculate
		newcart.save()
		
		##อัพเดทจำนวนของตะกร้า
		count = Cart.objects.filter(user=user)
		count = sum([c.quantity for c in count])
		updatequan = Profile.objects.get(user=user)
		updatequan.cartquan = count
		updatequan.save()
		
		return redirect('allproduct-page')
		
	except:
	
		newcart = Cart()
		newcart.user = user
		newcart.productid = pid
		newcart.productname = check.name
		newcart.price = int(check.price)
		newcart.quantity = 1  
		calculate = int(check.price) * 1
		newcart.total = calculate
		newcart.save()
		
		  ##อัพเดทจำนวนของตะกร้า
		count = Cart.objects.filter(user=user)
		count = sum([c.quantity for c in count])
		updatequan = Profile.objects.get(user=user)
		updatequan.cartquan = count
		updatequan.save()
	
		return redirect('allproduct-page')


def Mycart(request):
	username = request.user.username
	user = User.objects.get(username=username)
	
	context = {}
	
	if request.method == 'POST':
		data = request.POST.copy()
		productid = data.get('productid')
		item = Cart.objects.get(user=user, productid=productid)
		item.delete()  
		context['status' ] = 'delete'
		
		count = Cart.objects.filter(user=user)
		count = sum([c.quantity for c in count])
		updatequan = Profile.objects.get(user=user)
		updatequan.cartquan = count
		updatequan.save()
	
	
	mycart = Cart.objects.filter(user=user)
	count = sum([c.quantity for c in mycart])
	total = sum([c.total for c in mycart])
	
	context['mycart'] = mycart 
	context['count'] = count
	context['total'] = total
	return render(request, 'myapp/mycart.html', context)   



def MycartEdit(request):
	username = request.user.username
	user = User.objects.get(username=username)
	
	context = {}

	if request.method == 'POST':
		data = request.POST.copy()   
		
		if data.get('clear') == 'clear':
			print(data.get('clear'))
			clear = Cart.objects.filter(user=user).delete()
			updatequan = Profile.objects.get(user=user)
			updatequan.cartquan = 0
			updatequan.save()
			return redirect('mycart-page')
		
		editlist = []
		for k,v in data.items():
			print([k,v])
			if k[:2] == 'pd':
			 pid = int(k.split('_')[1])
			 dt = [pid, int(v)]
			 editlist.append(dt)
			print('Editlist:', editlist)
			
			for ed in editlist:
				edit = Cart.objects.get(productid=ed[0],user=user)
				edit.quantity = ed[1]
				calculate = edit.price * ed[1]
				edit.total = calculate
				edit.save()
				
		count = Cart.objects.filter(user=user)
		count = sum([c.quantity for c in count])
		updatequan = Profile.objects.get(user=user)
		updatequan.cartquan = count
		updatequan.save()
		
		return redirect('mycart-page')
				
			  
	mycart = Cart.objects.filter(user=user)
	context['mycart'] =  mycart 
	return render(request, 'myapp/mycartedit.html', context)    



def Checkout(request):
	username = request.user.username
	user = User.objects.get(username=username)
	if request.method == 'POST':
		data = request.POST.copy()
		name = data.get('name')
		tel = data.get('tel')
		address = data.get('address')
		shipping = data.get('shipping')
		payment = data.get('payment')
		other = data.get('other')
		page = data.get('page')
		if page == 'information':
			context = {}
			context['name'] = name
			context['tel'] = tel
			context['address'] = address
			context['shipping'] = shipping
			context['payment'] = payment
			context['other'] = other

			mycart = Cart.objects.filter(user=user)
			count = sum([ c.quantity for c in mycart])
			total = sum([ c.total for c in mycart])

			context['mycart'] = mycart
			context['count'] = count
			context['total'] = total
			
			return render(request, 'myapp/checkout2.html',context)

		if page == 'confirm':
			print('Confirm')
			print(data)
			mycart = Cart.objects.filter(user=user)
			# id = OD 0007 2020 09 03 22 00 30
			# id = OD 0230 20200903220030
			mid = str(user.id).zfill(4)
			dt = datetime.now().strftime('%Y%m%d%H%M%S')
			orderid = 'OD' + mid + dt

			for pd in mycart:
				order = OrderList()
				order.orderid = orderid
				order.productid = pd.productid
				order.productname = pd.productname
				order.price = pd.price
				order.quantity = pd.quantity
				order.total = pd.total
				order.save()

			#create order pending
			odp = OrderPending()
			odp.orderid = orderid
			odp.user = user
			odp.name = name
			odp.tel = tel
			odp.address = address
			odp.shipping = shipping
			odp.payment = payment
			odp.other = other
			odp.save()

			# clear cart
			Cart.objects.filter(user=user).delete()
			updatequan = Profile.objects.get(user=user)
			updatequan.cartquan = 0
			updatequan.save()
			return redirect('mycart-page')

			# generate order no. and save to Order Models
			# save product in cart to OrderProduct models
			# clear cart
			# redirect to order list page

	return render(request, 'myapp/checkout.html')


def OrderListPage(request):
	username = request.user.username
	user = User.objects.get(username=username)
	context = {}

	order = OrderPending.objects.filter(user=user)

	for od in order:
		orderid = od.orderid
		odlist = OrderList.objects.filter(orderid=orderid)
		total = sum([c.total for c in odlist])
		od.total = total
		
	context['allorder'] = order    

	return render(request, 'myapp/orderlist.html', context)


def AllOrderListPage(request):
  
	context = {}

	order = OrderPending.objects.all()

	for od in order:
		orderid = od.orderid
		odlist = OrderList.objects.filter(orderid=orderid)
		total = sum([c.total for c in odlist])
		od.total = total
  
		paginator = Paginator(order,15)
		page = request.GET.get('page')
		order = paginator.get_page(page)
		context['allorder'] = order    

	return render(request, 'myapp/allorderlist.html', context)



def UploadSlip(request, orderid):
	print('ORDER ID :', orderid)
	
	if request.method == 'POST' and request.FILES['slip']:
		data = request.POST.copy()
		sliptime = data.get('sliptime')
		
		update = OrderPending.objects.get(orderid=orderid)
		update.sliptime = sliptime
		
		file_image = request.FILES['slip']
		file_image_name = request.FILES['slip'].name.replace(' ', '')
		print('FILE_IMAGE:', file_image)
		print('IMAGE_NAME:', file_image_name)
		fs = FileSystemStorage()
		filename = fs.save(file_image_name, file_image)
		upload_file_url = fs.url(filename)
		update.slip = upload_file_url[6:]
		update.save()

	odlist = OrderList.objects.filter(orderid=orderid)
	total = sum([c.total for c in odlist])
	oddetail = OrderPending.objects.get(orderid=orderid)


	count = sum([c.quantity for c in odlist])
	if oddetail.shipping == 'ems':
		shipcost = sum([50 if i == 0 else 10 for i in range(count)])
	else:
		shipcost = sum([30 if i == 0 else 10 for i in range(count)])

	if oddetail.payment == 'cod':
		shipcost += 20

	context =  {'orderid': orderid,
				'total': total,
				'shipcost': shipcost,
				'grandtotal': total+shipcost,
				'oddetail': oddetail,
				'count': count}   
		

	return render(request, 'myapp/uploadslip.html',context)


def UpdatePaid(request, orderid, status):
		
	if request.user.profile.usertype != 'admin':
		return redirect('home-page')
	  
	order = OrderPending.objects.get(orderid=orderid)
	if status == 'confirm':
		order.paid = True
	elif status == 'cancel':
		order.paid = False
	order.save()

	return redirect('allorderlist-page')



def UpdateTracking(request, orderid):
	
	if request.user.profile.usertype != 'admin':
		return redirect('home-page')
	   
	if request.method == 'POST':
		order = OrderPending.objects.get(orderid=orderid)
		data = request.POST.copy()
		trackingnumber = data.get('trackingnumber')
		order.trackingnumber = trackingnumber
		order.save()       
		
		return redirect('allorderlist-page')
		
	context = {'orderid': orderid }
		
	return render(request, 'myapp/updatetracking.html', context)
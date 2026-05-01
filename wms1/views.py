
from django.db import transaction
from django.contrib import messages
import pandas as pd


from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from django.shortcuts import get_object_or_404, redirect

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from decimal import Decimal

from django.contrib.auth import authenticate, login


#Import Models
from django.db import models
from app1.models import User
from app1.models import supplier
from app1.models import product
from app1.models import productbarcode
from app1.models import asn_form
from app1.models import asn
from app1.models import stockin
from app1.models import stockin_detail
from app1.models import Location
from app1.models import gatepass
from .forms import ExcelUploadForm
from django.conf import settings
import pandas as pd
from django.shortcuts import render
from django.db.models import Sum, Max, F
from django.utils import timezone
from datetime import datetime
from app1.models import stockout
from app1.models import dn_form
from app1.models import dn
from app1.models import PickingHistory
from app1.models import outgatepass 
from collections import defaultdict

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    return render(request, "dashboard.html")
    
#@permission_required('app1.view_stock_report', raise_exception=True)
#def stock_balance_report(request):
    
#Use Models
current_datetime = timezone.now()
#login
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
#from django.contrib.auth.models import User  # Import Django's User model


from app1.models import User  # Your custom User model
@login_required
def userlist(request):
    # Fetch all users from app1_user table
    usr = User.objects.all()
    context = {
        'usr': usr
    }
    return render(request, 'userlists.html', context)
    

#User
@login_required
def userlist(request):
        usr = User.objects.all()
        context = {
            'usr':usr
        }

        return render(request,'userlists.html',context)
# Dashboard
@login_required
def dashboard(request):

    today = timezone.now().date()

    inbound_today = stockin.objects.filter(rec_dat=today).aggregate(Sum('qty'))['qty__sum'] or 0

    outbound_today = stockout.objects.filter(dat=today).aggregate(Sum('qty'))['qty__sum'] or 0

    total_in = stockin.objects.aggregate(Sum('qty'))['qty__sum'] or 0
    total_out = stockout.objects.aggregate(Sum('qty'))['qty__sum'] or 0

    current_stock = total_in - total_out
    sup_total = supplier.objects.count()
    prod_total = product.objects.count()
    context = {
        "inbound_today": inbound_today,
        "outbound_today": outbound_today,
        "current_stock": current_stock,
        'sup_total': sup_total,
        'prod_total': prod_total,
    }

    return render(request, "index.html", context)
    
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login

def signin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, "Please enter both username and password")
            return render(request, 'signin.html')

        user_obj = authenticate(request, username=username, password=password)

        if user_obj is not None:
            login(request, user_obj)
            return redirect('/dashboard/')
        else:
            # This is the key line
            messages.error(request, "Invalid Username or Password")
            return render(request, 'signin.html')  # render same page to show messages

    return render(request, 'signin.html')
    
def aboutus(request):
    today = timezone.now().date()

    inbound_today = stockin.objects.filter(rec_dat=today).aggregate(Sum('qty'))['qty__sum'] or 0

    outbound_today = stockout.objects.filter(dat=today).aggregate(Sum('qty'))['qty__sum'] or 0

    total_in = stockin.objects.aggregate(Sum('qty'))['qty__sum'] or 0
    total_out = stockout.objects.aggregate(Sum('qty'))['qty__sum'] or 0

    current_stock = total_in - total_out

    context = {
        "inbound_today": inbound_today,
        "outbound_today": outbound_today,
        "current_stock": current_stock,
    }
    
    return render(request, 'index.html')
    
# Supplier
@login_required
def addsupplier(request):
  #  'MEDIA_URL': settings.MEDIA_URL,   # Correct
    return render(request, 'addsupplier.html')

@login_required
def SupplierAdd(request):
    if request.method =="POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        phone=request.POST.get('phone')
        con=request.POST.get('con')
        city=request.POST.get('city')
        address=request.POST.get('address')
        desc=request.POST.get('desc')
        pic=request.FILES['image']

        sup = supplier(
          sup_name = name,
          sup_email = email,
          sup_country = con,
          sup_city=city,
          sup_phone=phone,
          sup_address=address,
          sup_desc=desc,
          sup_pic=pic,
          

       )
        sup.save()
    return redirect('supplierlist')
 
@login_required   
def supplierlist(request):
    sup = supplier.objects.all()

    context = {
        'sup': sup
        
    }

    return render(request, 'supplierlist.html', context)

  
def upload_excel(request):
    if request.method == "POST":
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            df = pd.read_excel(request.FILES['file'])  # Read the uploaded Excel file
            
            for _, row in df.iterrows():
                supplier.objects.get_or_create(
                    sup_name=row['sup_name'],
                    defaults={
                        'sup_email': row['sup_email'], 
                        'sup_phone': row['sup_phone'],
                        'sup_country': row['sup_country'], 
                        'sup_city': row['sup_city'],
                        'sup_address': row['sup_address'], 
                        'sup_desc': row['sup_desc'],
                        'sup_pic': row['sup_pic'], 
                        'sup_blc': row['sup_blc'],
                    }
                )
    else:
        form = ExcelUploadForm()

    return render(request, 'supplierlist.html')

@login_required
def export_supplier_excel(request):
    # Fetch only the last row
    data = supplier.objects.all().values().last()  # returns a dictionary

    if not data:
        return HttpResponse("No supplier data available.")

    df = pd.DataFrame([data])  # wrap dict in a list

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="supplier_last_row.xlsx"'

    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Supplier List')

    return response


@login_required
def editsupplier(request, id):
    sup1 = supplier.objects.filter(id=id)
    context = {
       'sup1':sup1,
    }
    return render(request,'editsupplier.html',context)

@login_required 
def UpdateSupplier(request, id):
    sup = supplier.objects.get(id=id)  # ← Get existing row

    if request.method == "POST":
        sup.sup_name = request.POST.get('name')
        sup.sup_email = request.POST.get('email')
        sup.sup_phone = request.POST.get('phone')
        sup.sup_country = request.POST.get('con')
        sup.sup_city = request.POST.get('city')
        sup.sup_address = request.POST.get('address')
        sup.sup_desc = request.POST.get('desc')

        # Handle file upload
        if request.FILES.get('pic'):
            sup.sup_pic = request.FILES['pic']

        sup.save()
        return redirect('supplierlist')

    return redirect('supplierlist')
    
# PDF 
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from app1.models import supplier
from django.shortcuts import render, redirect

@login_required
def supplier_pdf(request):
    # Create PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="supplier_list.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    y = 750  # starting Y position

    p.setFont("Helvetica-Bold", 14)
    p.drawString(200, 800, "Supplier List")

    p.setFont("Helvetica", 10)

    suppliers = supplier.objects.all()

    for s in suppliers:
        line = f"ID: {s.id} | Name: {s.sup_name} | Email: {s.sup_email} | Phone: {s.sup_phone}"
        p.drawString(50, y, line)
        y -= 20

        if y < 50:  # new page if space ends
            p.showPage()
            p.setFont("Helvetica", 10)
            y = 750

    p.showPage()
    p.save()
    return response

#pirnt
from django.shortcuts import render

@login_required
def supplier_print(request):
    sup = supplier.objects.all()
    return render(request, "supplier_print.html", {"sup": sup})

    
# Product    
@login_required
def productlist(request):
    pod = product.objects.all()
    
    context = {
        'pod' : pod 
    }
    return render(request, 'productlist.html', context)
     
@login_required
def addproduct(request):
    sup = supplier.objects.all()

    context = {
        'sup': sup
        
    }
    return render(request, 'addproduct.html',context)
    
# product
@login_required
def ProductAdd(request):
    if request.method =="POST":
        name=request.POST.get('name')
        desc=request.POST.get('code')
        volume=request.POST.get('volume')
        uom=request.POST.get('uom')
        supid=request.POST.get('supid')
        weight=request.POST.get('weight')
        branch=request.POST.get('branch')
        
        pic=request.FILES['image']

        pod = product(
          prod_name = name,
          prod_desc=desc,
          prod_volume = volume,
          prod_uom = uom,
          prod_supid=supid,
          prod_weight=weight,
          prod_branch=branch,
          
          prod_pic=pic,
          

       )
        pod.save()
    return redirect('productlist')

#Barcode
@login_required
def barcodelist(request):
    pod = productbarcode.objects.all()
    
    context = {
         'pod' : pod 
    }
    return render(request, 'barcodelist.html', context)
     

@login_required
def addbarcode(request):
    sup = product.objects.all()

    context = {
        'sup': sup
        
    }
    return render(request, 'addbarcode.html',context)
    
# product Barcode
@login_required
def BarcodeAdd(request):
    if request.method =="POST":
        prodid=request.POST.get('prodid')
        barcode=request.POST.get('barcode') 
        
#   pic=request.FILES['image']  
  
        pod = productbarcode(
          product_id=prodid,
          product_barcode=barcode,
       )
        pod.save()
    return redirect('barcodelist')


#  Stock
@login_required
def addstock(request):
    
    return render(request, 'addstock.html')
def parse_date(value):
    if pd.isna(value):
        return None
    if isinstance(value, pd.Timestamp):
        return value.date()
    return value  # already correct

import pandas as pd
from datetime import datetime

def clean_date(value):
    if pd.isna(value):
        return None
    if isinstance(value, pd.Timestamp):
        return value.date()
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, str):
        return value  # already fine
    return None  # fallback
    
from django.db import connection

@login_required
def upload_excelstock(request):
    if request.method == "POST":
        Location.objects.all().delete()

        # ✅ Reset ID to 1
        with connection.cursor() as cursor:
            cursor.execute("ALTER TABLE app1_location AUTO_INCREMENT = 1")

        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            df = pd.read_excel(request.FILES['file'])

            for _, row in df.iterrows():
                Location.objects.create(
                    prod_id=row['prod_id'],
                    batch_id=row['batch_id'],
                    stockin_id=row['stockin_id'],
                    volume=row['volume'],
                    uom=row['uom'],
                    sup_id=row['sup_id'],
                    mfg_dat=clean_date(row.get('mfg_dat')),
                    expiry_dat=clean_date(row.get('expiry_dat')),
                    block_stock=0.00,
                    expire_stock=0.00,
                    blc=row['blc'],
                    location_name=row['location_name'],
                    branch=1,
                )

    else:
        form = ExcelUploadForm()

    return render(request, 'addstock.html', {'form': form})
     
@login_required   
def supplierlist(request):
    sup = supplier.objects.all()

    context = {
        'sup': sup
        
    }

    return render(request, 'supplierlist.html', context)
    
@login_required    
def editproduct(request,id):
    pod1 = product.objects.filter(id=id)
    context = {
       'pod1':pod1
    }
    return render(request, 'editproduct.html', context)

@login_required
def UpdateProduct(request, id):
    pod = product.objects.get(id=id)  # ← Get existing row

    if request.method == "POST":
        pod.prod_name = request.POST.get('name')
        pod.prod_desc = request.POST.get('code')
        pod.prod_volume = request.POST.get('size')
        pod.prod_uom = request.POST.get('uom')
        
        # Handle file upload
        if request.FILES.get('pic'):
            pod.prod_pic = request.FILES['pic']

        pod.save()
        return redirect('productlist')

    return redirect('productlist')

@login_required    
def upload_excelproduct(request):
    if request.method == "POST":
        form = ExcelUploadForm(request.POST, request.FILES)
        if form.is_valid():
            df = pd.read_excel(request.FILES['file'])  # Read the uploaded Excel file
            
            for _, row in df.iterrows():
                product.objects.get_or_create(
                    prod_name=row['prod_name'],
                    defaults={
                        'prod_desc': row['prod_desc'], 
                        'prod_volume': row['prod_volume'],
                        'prod_uom': row['prod_uom'], 
                        'prod_supid': row['prod_supid'],
                        'prod_weight': row['prod_weight'], 
                        'prod_pic': row['prod_pic'],
                        'prod_branch': 1,
                    }
                )
    else:
        form = ExcelUploadForm()

    return render(request, 'productlist.html',context)

@login_required
def export_product_excel(request):
    # Fetch only the last row
    data = product.objects.all().values().last()  # returns a dictionary

    if not data:
        return HttpResponse("No supplier data available.")

    df = pd.DataFrame([data])  # wrap dict in a list

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="product_last_row.xlsx"'

    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Supplier List')

    return response
    
@login_required    
def productdetails(request):
    return render(request, 'productdetails.html')
def side(request):
    return render(request, 'side.html')

#ASN 
@login_required
def asn_load(request):
    # Fetch all asn format table
    frm = asn.objects.all()
    sup = supplier.objects.all()
    context = {
        'frm': frm,
        'sup': sup
    }
    return render(request, 'asn.html', context)

def load_products(request):
    supplier_id = request.GET.get('supplier_id')

    products = product.objects.filter(prod_supid=supplier_id)

    return render(request, 'product_dropdown_list.html', {
        'products': products
    })
     
# ASN Upload
@login_required
def upload_asn(request):
    if request.method == "POST":
        form = ExcelUploadForm(request.POST, request.FILES)

        if form.is_valid():
            df = pd.read_excel(request.FILES['file'])

            # 🔹 First: Check duplicate ASN
            for _, row in df.iterrows():
                asn_no = row['asn_no']
                if stockin.objects.filter(rec_asnno=asn_no).exists():
                    messages.error(request, f"ASN No {asn_no} already exists")
                    return render(request, 'asn.html', {'form': form})

            # 🔹 Second: Process rows
            for _, row in df.iterrows():
                asn_no = row['asn_no']
                prod_code = row['prod_id']

                # Try to get product
                product_obj = product.objects.filter(prod_desc=prod_code).first()

                if product_obj:
                    # ✅ Product found → insert into stockin
                    stockin.objects.create(
                        rec_asnno=asn_no,
                        prod_id=prod_code,
                        sup_id=product_obj.prod_supid,
                        volume=product_obj.prod_volume,
                        batch=row['batch'],
                        asn_qty=row['qty'],
                        transporter=row['trns'],
                        truck_no=row['veh'],
                        gatepass_id='0',
                        
                    )
                else:
                    # ❌ Product not found → insert into ASN table
                    asn.objects.create(
                        asn_no=asn_no,
                        prod_id=prod_code,
                        batch=row['batch'],
                        ctn=row['qty'],
                        qty=row['qty'],
                        branch_id=1,
                        trns=row['trns'],
                        veh=row['veh'], 
                        
                        remarks="Product code not found"
                    )

            messages.success(request, "ASN uploaded successfully")
            return render(request, 'asn.html', {'form': form})

    else:
        form = ExcelUploadForm()

    return render(request, 'asn.html', {'form': form})
#return redirect('/asn/')


@login_required
def asn_view(request):

    if request.method == "POST":
        asn_no = request.POST.get('asn_no')
        product = request.POST.get('product')
        batch = request.POST.get('batch')
        qty = request.POST.get('qty')
        supplier_id = request.POST.get('supplier')

        # Save data
        asn.objects.create(
            asn_no=asn_no,
            prod_id=product,
            batch=batch,
            ctn=qty,
            branch_id=1,
            remarks="Added manually"
        )

        
        return redirect('asnview') 

        
@login_required
def export_asn_excel(request):
    # Fetch only the last row
    data = asn_form.objects.values('asn_no','prod_id','item','batch','qty','veh','trns').last()  # returns a dictionary

    if not data:
        return HttpResponse("No ASN data available.")

    df = pd.DataFrame([data])  # wrap dict in a list

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="ASN Format.xlsx"'

    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='ASN Format')

    return response

@login_required
def editasn(request,id):
    pod2 = asn.objects.filter(id=id)
    context = {
       'pod2':pod2
    }
    return render(request, 'edit_asn.html',context)

@login_required
def updateasn(request, id):
    pod3 = asn.objects.get(id=id)  # ← Get existing row

    if request.method == "POST":
        pod3.asn_no = request.POST.get('asn_no')
        pod3.prod_id = request.POST.get('prod_id')
        pod3.qty = request.POST.get('qty')
        pod3.ctn = request.POST.get('qty')
        pod3.batch = request.POST.get('batch')
        
        # Handle file upload
        #if request.FILES.get('pic'):
        #    pod.prod_pic = request.FILES['pic']

        pod3.save()
        return redirect('/asn/')

   # return redirect('/asn/')

@login_required
def deletesn(request, id):
    obj = get_object_or_404(asn, id=id)
    obj.delete()
    return redirect('/asn/')

@login_required
def process_asn(request):

    asn_records = asn.objects.all()

    for record in asn_records:

        try:
            product_obj = product.objects.get(
                prod_desc=record.prod_id
            )

            stockin.objects.create(
                rec_asnno=record.asn_no,
                prod_id=product_obj.prod_desc,
                sup_id=product_obj.prod_supid,
                batch=record.batch,
                asn_qty=record.qty,
                transporter=record.trns,
                truck_no=record.veh,
                gatepass_id='0',
            )

            record.delete()

        except product.DoesNotExist:
            pass   # do nothing if product not found

    return redirect('/asn/')

# Gate Pass
@login_required        
def gatepasslist(request):
    pod = gatepass.objects.all()
    
    context = {
        'pod' : pod 
    }
    return render(request, 'gatepasslist.html', context)

@login_required
def addgpass(request):
    #frm = stockin.objects.all()
    frm = stockin.objects.filter(
    gatepass_id=0
).values('rec_asnno').distinct()
    context = {
        'frm': frm
    }
    return render(request, 'addgpass.html',context)

def gpassadd(request):
    if request.method =="POST":
        gpid=request.POST.get('gpid')
        name=request.POST.get('name')
        cnic=request.POST.get('cnic')
        mobile=request.POST.get('mobile')
        typ=request.POST.get('type')
        
        bilty=request.POST.get('bilty')
        seal=request.POST.get('seal')
        vehtemp=request.POST.get('vehtemp')
        rem=request.POST.get('rem')
     

        gp = gatepass(
          gp_asnno = gpid,
          driver = name,
          cnic=cnic,
          mobile = mobile,
          typ = typ,
          branch_id='1',
          remarks=rem,
          user_id='1',
          final='1',
          seal=seal,
          

       )
        gp.save()
        
        # 2️⃣ Update stockin table
        stockin.objects.filter(
            rec_asnno=gpid,
            gatepass_id=0
        ).update(
            gatepass_id=gp.id
        )
    
    return redirect('gatepasslist')
    

# Gatepass Print
@login_required
def ingatepass_print(request, id):
    """
    Inward Gatepass (Stock Receipt) Print View
    """

    # Get the gatepass header
    pod = get_object_or_404(gatepass, id=id)

    # Get all stockin items for this gatepass
    stock_items = stockin.objects.filter(gatepass_id=id)

    # Preload products
    products = {p.prod_desc: p.prod_name for p in product.objects.all()}

    # Group items by supplier and calculate totals
    distributor_group = {}
    grand_total = Decimal("0")

    for item in stock_items:
        # 🔹 Get supplier name
        try:
            dealer = item.sup_id.sup_name  # If ForeignKey
        except AttributeError:
            # If sup_id is integer, look up manually
            try:
                dealer = supplier.objects.get(id=item.sup_id).sup_name
            except supplier.DoesNotExist:
                dealer = f"Supplier ID {item.sup_id or 'Unknown'}"

        # Attach product name
        item.prod_name = products.get(item.prod_id, item.prod_id)

        # Safe decimal conversion
        try:
            qty = Decimal(item.qty or 0)
            return_qty = Decimal(item.return_qty or 0)
        except:
            qty = Decimal("0")
            return_qty = Decimal("0")

        actual_in = qty - return_qty
        item.actual_in = actual_in

        # Initialize distributor group if not exists
        if dealer not in distributor_group:
            distributor_group[dealer] = {"items": [], "total": Decimal("0")}

        distributor_group[dealer]["items"].append(item)
        distributor_group[dealer]["total"] += actual_in
        grand_total += actual_in

    context = {
        "pod": pod,
        "distributor_group": distributor_group,
        "grand_total": grand_total,
    }

    return render(request, "ingatepass_print.html", context)
    
# Receiveing
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import Sum, Max, F, ExpressionWrapper, IntegerField

from app1.models import stockin


@login_required
def addreceive(request):

    frm = stockin.objects.filter(
        gatepass_id__gt=0
    ).values('rec_asnno').annotate(
        total_asn_qty=Sum('asn_qty'),
        total_rec_qty=Sum('qty'),
        truck_no=Max('truck_no'),
        gt_pass=Max('gatepass_id'),
        ss=Max('sup_id'),
        transporter=Max('transporter'),
        id=Max('id'),

        # ✅ Correct balance calculation
        blc=ExpressionWrapper(
            F('total_asn_qty') - F('total_rec_qty'),
            output_field=IntegerField()
        )
    ).filter(
        total_rec_qty__lt=F('total_asn_qty')
    )

    return render(request, 'addreceive.html', {
        'frm': frm
    })


from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.db.models import F, OuterRef, Subquery, Value
from django.db.models.functions import Coalesce

from app1.models import stockin, productbarcode  # adjust if your app name differs


@login_required
def receivelist(request, rec_asnno):

    pod = list(stockin.objects.filter(
        rec_asnno=rec_asnno,
        qty__lt=F('asn_qty')
    ))

    # Get all barcodes
    barcodes = productbarcode.objects.all()

    # Create mapping: product_id → [barcodes]
    barcode_map = {}
    for b in barcodes:
        barcode_map.setdefault(b.product_id, []).append(b.product_barcode)

    # Attach to each stock item
    for item in pod:
        item.barcodes_list = barcode_map.get(item.prod_id, [])

    return render(request, 'receivelist.html', {
        'pod': pod
    })
@login_required
def editrec(request, id):
    pod1 = stockin.objects.get(id=id)

    prod = product.objects.filter(prod_desc=pod1.prod_id).first()

    context = {
        'pod1': pod1,
        'prod_name': prod.prod_name if prod else ''
     #   'today': date.today().isoformat()
    }
    return render(request, 'editrec.html', context)
    
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages

@login_required
def UpdateRec(request, id):
    pod = get_object_or_404(stockin, id=id)

    if request.method == "POST":

        rec_qty = int(request.POST.get('recqty', 0))
        status_qty = int(request.POST.get('statusqty', 0))

        # 🔎 1️⃣ Check if received qty greater than ASN qty
        if rec_qty > pod.asn_qty:
            messages.error(request, "Received quantity cannot be greater than ASN quantity!")
            return redirect('editrec', id=id)
        
        # ✅ Update date & time automatically
        from datetime import datetime

        current_datetime = datetime.now()

        pod.rec_dat = current_datetime.date()
        pod.rec_tim = current_datetime.time().replace(microsecond=0)

        # 🔎 2️⃣ Add received qty to existing qty
        pod.qty = (pod.qty or 0) + rec_qty

        # 🔎 3️⃣ Add condition qty
        pod.cond_qty = (pod.cond_qty or 0) + status_qty

        # Other fields
        pod.cond = request.POST.get('status')
        pod.expiry = request.POST.get('exp')
        pod.mfg = request.POST.get('mfg')
    #    pod.remarks = request.POST.get('rem')
        
        pod.rec_userid = 1
        pod.branch_id = 1
        pod.asn_balance = pod.asn_qty - pod.qty   # ✅ assign to model field
        pod.save()

# 🔎 3️⃣ Update / Create detail record
        detail, created = stockin_detail.objects.get_or_create(
            rec_id=pod,
            mfg=pod.mfg,
            expiry=pod.expiry,
            defaults={'qty': rec_qty}
        )

        if not created:
            detail.qty += rec_qty
            detail.save()
    
    # ✅ If fully received
        if pod.qty == pod.asn_qty:
            messages.success(request, "All items received successfully!")
            return redirect('/addreceive/')


        messages.success(request, "Record updated successfully!")
        return redirect('editrec', id=id)

    return redirect('editrec', id=id)
    
    
from django.db.models import Sum, Max, F
from django.contrib.auth.decorators import login_required

@login_required
def addlocation(request):

    # Step 1: Aggregate ASN data
    qs = stockin.objects.filter(
        gatepass_id__gt=0
    ).values(
        'rec_asnno'
    ).annotate(
        total_qty=Sum('qty'),
        total_located=Sum('location'),
        truck_no=Max('truck_no'),
        transporter=Max('transporter'),
        id=Max('id'),
        gt=Max('gatepass_id'),
        rc_dt=Max('rec_dat')
    )

    # Step 2: Filter only pending (not fully located)
    frm = list(qs.filter(total_located__lt=F('total_qty')))

    # Step 3: Add calculated fields
    for i in frm:
        i['remaining'] = (i['total_qty'] or 0) - (i['total_located'] or 0)

        i['progress'] = int(
            (i['total_located'] / i['total_qty']) * 100
        ) if i['total_qty'] else 0

    # Step 4: Summary totals
    total_qty = sum(i['total_qty'] or 0 for i in frm)
    located_qty = sum(i['total_located'] or 0 for i in frm)
    remaining_qty = total_qty - located_qty

    progress = int((located_qty / total_qty) * 100) if total_qty else 0

    # Step 5: Send to template
    context = {
        'frm': frm,
        'total_qty': total_qty,
        'located_qty': located_qty,
        'remaining_qty': remaining_qty,
        'progress': progress
    }

    return render(request, 'addlocation.html', context)
from django.db.models import F, OuterRef, Subquery

@login_required
def locationlist(request, rec_asnno):
    # Subquery to get product name for each stockin row
    prod_name_subquery = product.objects.filter(
        prod_desc=OuterRef('prod_id')
    ).values('prod_name')[:1]  # [:1] limits to single value

    pod = stockin.objects.filter(
        rec_asnno=rec_asnno,
        location__lt=F('qty')
    ).annotate(
        prod_name=Subquery(prod_name_subquery)
    ).order_by('id')

    return render(request, 'locationlist.html', {'pod': pod})

@login_required    
def editlocation(request, id):
    pod1 = stockin.objects.get(id=id)

    prod = product.objects.filter(prod_desc=pod1.prod_id).first()

    context = {
        'pod1': pod1,
        'prod_name': prod.prod_name if prod else ''
     #   'today': date.today().isoformat()
    }
    return render(request, 'editlocation.html', context)

import traceback

@login_required
def UpdateLocation(request, id):
    try:
        pod = get_object_or_404(stockin, id=id)

        if request.method == "POST":
            location_name = request.POST.get('location', '').strip().lower()
            status = request.POST.get('status', 'Good')
            spid = request.POST.get('spid')
            rec_qty = Decimal(request.POST.get('recqty', '0.00'))

            if rec_qty > (pod.qty or Decimal('0.00')):
                messages.error(request, "Qty exceeded!")
                return redirect('editlocation', id=id)

            pod.location = Decimal(pod.location or 0) + rec_qty
            pod.save()

            existing = Location.objects.filter(
                stockin=pod,
                prod_id=pod.prod_id,
                batch_id=pod.batch,
                expiry_dat=pod.expiry,
                location_name__iexact=location_name
            ).first()

            if existing:
                existing.blc = Decimal(existing.blc or 0)
                existing.block_stock = Decimal(existing.block_stock or 0)
                existing.sup_id = spid  # ✅ update supplier
                if status == "Damage":
                    existing.block_stock += rec_qty
                else:
                    existing.blc += rec_qty

                existing.save()

            else:
                Location.objects.create(
                    stockin=pod,
                    prod_id=pod.prod_id,
                    sup_id=spid,  # ✅ added
                    batch_id=pod.batch,
                    location_name=location_name,
                    mfg_dat=pod.mfg,
                    expiry_dat=pod.expiry,
                    blc=rec_qty if status != "Damage" else Decimal('0.00'),
                    block_stock=rec_qty if status == "Damage" else Decimal('0.00')
                )

            return redirect('editlocation', id=id)

        return redirect('editlocation', id=id)

    except Exception as e:
        print("ERROR:", str(e))
        print(traceback.format_exc())
        messages.error(request, f"Error: {str(e)}")
        return redirect('editlocation', id=id)
#D.N 
@login_required
def dn_load(request):
    # Fetch all dn format table
    frm = dn.objects.all()
    context = {
        'frm': frm
    }
    return render(request, 'dn.html', context)

# D.N Upload

from django.db.models import Sum
from django.contrib import messages
import pandas as pd

@login_required
def upload_dn(request):

    if request.method == "POST":
        form = ExcelUploadForm(request.POST, request.FILES)

        if form.is_valid():
            df = pd.read_excel(request.FILES['file'])

            # 🔹 Dictionary to store remaining stock per product+batch
            stock_balance = {}

            # =========================================================
            # 🔹 1️⃣ Duplicate DN Check (DN + gatepass_id = 0)
            # =========================================================
            for _, row in df.iterrows():
                dn_no = row['dn_no']

                if stockout.objects.filter(
                        stockout_orderno=dn_no,
                        gatepass_id='0'
                ).exists():

                    messages.error(request, f"DN No {dn_no} already exists with Gatepass 0")
                    return render(request, 'dn.html', {'form': form})

            # =========================================================
            # 🔹 2️⃣ Process Rows
            # =========================================================
            for _, row in df.iterrows():

                dn_no = row['dn_no']
                prod_code = row['prod_id']
                batch_no = row['batch']
                excel_qty = float(row['qty'])
                dealer = row['dealer']
                vehicle = row['veh']

                key = f"{prod_code}_{batch_no}"

                # ✅ Step 1: Check Product Exists
                product_obj = product.objects.filter(
                    prod_desc=prod_code
                ).first()

                if not product_obj:
                    dn.objects.create(
                        dn_no=dn_no,
                        prod_id=prod_code,
                        batch=batch_no,
                        qty=excel_qty,
                        branch_id=1,
                        dealer=dealer,
                        veh=vehicle,
                        remarks="Product code not found"
                    )
                    continue

                # =====================================================
                # ✅ Step 2: Load stock only first time into variable
                # =====================================================
                if key not in stock_balance:

                    total_blc = Location.objects.filter(
                        prod_id=prod_code,
                        batch_id=batch_no
                    ).aggregate(total=Sum('blc'))['total'] or 0

                    stock_balance[key] = float(total_blc)

                # =====================================================
                # ✅ Step 3: Check Remaining Balance from Variable
                # =====================================================
                if stock_balance[key] >= excel_qty:

                    # Deduct from variable
                    stock_balance[key] -= excel_qty

                    # Insert into stockout
                    stockout.objects.create(
                        stockout_orderno=dn_no,
                        prod_id=prod_code,
                        sup_id=product_obj.prod_supid,
                        volume=product_obj.prod_volume,
                        batch=batch_no,
                        dn_qty=excel_qty,
                        dealer=dealer,
                        truck_no=vehicle,
                        gatepass_id='0',
                    )

                else:
                    # Not enough stock in remaining variable
                    dn.objects.create(
                        dn_no=dn_no,
                        prod_id=prod_code,
                        batch=batch_no,
                        qty=excel_qty,
                        branch_id=1,
                        dealer=dealer,
                        veh=vehicle,
                        remarks="Insufficient stock after previous deductions"
                    )

            messages.success(request, "D.N uploaded successfully")
            return render(request, 'dn.html', {'form': form})

    else:
        form = ExcelUploadForm()

    return render(request, 'dn.html', {'form': form})
    
@login_required
def editdn(request,id):
    pod2 = dn.objects.filter(id=id)
    context = {
       'pod2':pod2
    }
    return render(request, 'edit_dn.html',context)

@login_required    
def updatedn(request, id):
    pod3 = dn.objects.get(id=id)  # ← Get existing row

    if request.method == "POST":
        pod3.dn_no = request.POST.get('asn_no')
        pod3.prod_id = request.POST.get('prod_id')
        pod3.qty = request.POST.get('qty')
        pod3.batch = request.POST.get('batch')
        
        # Handle file upload
        #if request.FILES.get('pic'):
        #    pod.prod_pic = request.FILES['pic']

        pod3.save()
        return redirect('/dn/')

@login_required        
def deletedn(request, id):
    obj = get_object_or_404(dn, id=id)
    obj.delete()
    return redirect('/dn/')

from django.db.models import Sum
from django.shortcuts import redirect

@login_required
def process_dn(request):

    asn_records = dn.objects.all()

    # 🔹 Store remaining stock per product+batch
    stock_balance = {}

    for record in asn_records:
 
        try:
            product_obj = product.objects.get(
                prod_desc=record.prod_id
            )

            key = f"{record.prod_id}_{record.batch}"

            # =====================================================
            # ✅ Load stock only first time from DB
            # =====================================================
            if key not in stock_balance:

                total_blc = Location.objects.filter(
                    prod_id=record.prod_id,
                    batch_id=record.batch
                ).aggregate(total=Sum('blc'))['total'] or 0

                stock_balance[key] = float(total_blc)

            # =====================================================
            # ✅ Check Remaining Stock from Variable
            # =====================================================
            if stock_balance[key] >= float(record.qty):

                # Deduct from variable
                stock_balance[key] -= float(record.qty)

                # Insert into stockout
                stockout.objects.create(
                    stockout_orderno=record.dn_no,
                    prod_id=product_obj.prod_desc,
                    sup_id=product_obj.prod_supid,
                    batch=record.batch,
                    dn_qty=record.qty,
                    dealer=record.dealer,
                    truck_no=record.veh,
                    gatepass_id='0',
                )

                # Delete only if successfully processed
                record.delete()

            else:
                # ❌ Not enough stock → skip this record
                continue

        except product.DoesNotExist:
            # ❌ Product not found → skip
            continue

    return redirect('/dn/')
    
@login_required    
def export_dn_excel(request):
    # Fetch only the last row
    data = dn_form.objects.values('dn_no','prod_id','item','batch','qty','veh','dealer').last()  # returns a dictionary

    if not data:
        return HttpResponse("No DN data available.")

    df = pd.DataFrame([data])  # wrap dict in a list

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="DN Format.xlsx"'

    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='DN Format')

    return response

# Picking
@login_required
def pick(request):
    # Fetch all dn format table
    frm = (
    stockout.objects
    .filter(qty='0')    # or qty=0 if exists
    .values(
        'stockout_orderno',
        'prod_id',
        'batch',
    )
    .annotate(dnqty=Sum('dn_qty'))
    )
    
    context = {  
        'frm': frm 
    }
    return render(request, 'pick.html', context)
    

@login_required
def pick_stock(request):

    if request.method == "POST":

        # multiple dn numbers from form (comma separated)
        dn_list = request.POST.get('dnno')
        dn_numbers = [dn.strip() for dn in dn_list.split(',')]

        with transaction.atomic():

            for dnno in dn_numbers:

                rows = stockout.objects.filter(
                    stockout_orderno=dnno,
                    qty=0
                )

                for row in rows:

                    required_qty = row.dn_qty

                    # pick from lowest stock locations first
                    locations = Location.objects.filter(
                        prod_id=row.prod_id,
                        batch_id=row.batch,
                        blc__gt=0
                    ).order_by('blc')   # lowest stock first

                    for loc in locations:

                        if required_qty <= 0:
                            break

                        if loc.blc >= required_qty:
                            picked = required_qty
                            loc.blc -= required_qty
                            required_qty = 0
                        else:
                            picked = loc.blc
                            required_qty -= loc.blc
                            loc.blc = 0

                        loc.save()

                        now = timezone.now()

                        # save history
                        PickingHistory.objects.create(
                            prod_id=row.prod_id,
                            batch_id=row.batch,
                            picked_qty=picked,
                            pick_date=now.date(),
                            pick_time=now.time(),
                            created_at=now,
                            location_id=loc.id,
                            stockout_id=row.id,
                            user_id=request.user.id
                        )

                    # update stockout picked qty
                    row.qty = row.dn_qty - required_qty
                    row.save()

        # after all DN processed
        return redirect('/pick/')

    return redirect('/pick/')
    

from django.db.models import Sum, OuterRef, Subquery
from django.db.models.functions import Cast
from django.db.models import CharField

@login_required
def picking_report(request):
    """
    Show picking records grouped by date with location names and product names
    when PickingHistory.prod_id is integer and Product.prod_desc is string
    """
    date_str = request.GET.get('date')
    report_date = timezone.now().date()
    if date_str:
        try:
            report_date = timezone.datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            pass

    # Subquery: cast PickingHistory.prod_id to CharField to match Product.prod_desc
    product_name_subquery = product.objects.filter(
        prod_desc=Cast(OuterRef('prod_id'), CharField())
    ).values('prod_name')[:1]

    # Subquery: location name
    location_name_subquery = Location.objects.filter(
        id=OuterRef('location_id')
    ).values('location_name')[:1]

    report = PickingHistory.objects.filter(
        pick_date=report_date,
        picked_confirm_date__isnull=True
    ).annotate(
        prod_name=Subquery(product_name_subquery),
        location_name=Subquery(location_name_subquery)
    ).values(
        'id',
        'prod_name',
        'batch_id',
        'location_name',
        'picked_qty',
        'prod_id'
    ).annotate(
        total_picked=Sum('picked_qty')
    ).order_by('location_name')

    context = {
        'report': report,
        'report_date': report_date
    }
    return render(request, 'picking_report.html', context)

@login_required    
def confirm_pick(request, id):

    pick = get_object_or_404(PickingHistory, id=id)

    pick.picked_confirm_user = request.user.username
    pick.picked_confirm_date = timezone.now().date()
    pick.picked_confirm_time = timezone.now().time().replace(microsecond=0)

    pick.save()

    return redirect('picking_report')
    
# Outward Gate Pass
        
def outgatepasslist(request):
    pod = outgatepass.objects.all()
    
    context = {
        'pod' : pod 
    }
    return render(request, 'outgatepasslist.html', context)

@login_required    
def outaddgpass(request):
    #frm = stockout.objects.all()
    frm = stockout.objects.filter(
    gatepass_id=0
).values('stockout_orderno').distinct()
    context = {
        'frm': frm
    }
    return render(request, 'outaddgpass.html', context)

@login_required
def outgpassadd(request):
    if request.method == "POST":

        gpid_list = request.POST.getlist('gpid')  # multiple DN numbers

        name = request.POST.get('name')
        cnic = request.POST.get('cnic')
        mobile = request.POST.get('mobile')
        typ = request.POST.get('type')
        bilty = request.POST.get('dealer')
        seal = request.POST.get('seal')
        vehtemp = request.POST.get('vehtemp')
        rem = request.POST.get('rem')

        # Convert list to string
        gpid_string = ",".join(gpid_list)

        # Create ONLY ONE gatepass
        gp = outgatepass.objects.create(
            gp_asnno=gpid_string,
            driver=name,
            cnic=cnic,
            mobile=mobile,
            typ=typ,
            branch_id='1',
            remarks=rem,
            user_id='1',
            final='1',
            seal=seal,
            dealer=bilty,
        )

        # Update ALL stockout rows
        stockout.objects.filter(
            stockout_orderno__in=gpid_list,
            gatepass_id=0
        ).update(
            gatepass_id=gp.id
        ) 

    return redirect('outgatepasslist')
    
@login_required
def outgatepass_print(request, id):

    pod = get_object_or_404(outgatepass, id=id)

    stock_items = stockout.objects.filter(gatepass_id=id)

    products = {p.prod_desc: p.prod_name for p in product.objects.all()}

    distributor_group = {}
    grand_total = Decimal("0")

    for item in stock_items:

        dealer = item.dealer
        prod_name = products.get(item.prod_id, item.prod_id)

        return_qty = Decimal(item.return_qty or 0)
        actual_out = item.qty - return_qty

        if dealer not in distributor_group:
            distributor_group[dealer] = {
                "items": [],
                "total": Decimal("0")
            }

        item.prod_name = prod_name
        item.actual_out = actual_out

        distributor_group[dealer]["items"].append(item)
        distributor_group[dealer]["total"] += actual_out

        grand_total += actual_out

    context = {
        "pod": pod,
        "distributor_group": distributor_group,
        "grand_total": grand_total,
    }

    return render(request, "outgatepass_print.html", context)

# Reports
@login_required
def stock_balance_report(request, branch_id=None):
    """
    Stock Balance Report: Shows available quantity per product and batch
    """

    # Step 1: Get all products
    products = product.objects.all()

    # Step 2: Prepare stock balance data
    stock_data = []

    for p in products:
        # Total received (stockin)
        stock_in_qs = stockin.objects.filter(prod_id=p.prod_desc)
        if branch_id:
            stock_in_qs = stock_in_qs.filter(branch_id=branch_id)
        total_in = stock_in_qs.aggregate(total_in=Sum('qty'))['total_in'] or 0

        # Total returned / deducted (stockout)
        stock_out_qs = stockout.objects.filter(prod_id=p.prod_desc)
        if branch_id:
            stock_out_qs = stock_out_qs.filter(branch_id=branch_id)
        total_out = stock_out_qs.aggregate(total_out=Sum('qty'))['total_out'] or 0

        # Actual stock
        balance_qty = total_in - total_out

        if balance_qty > 0:
            stock_data.append({
                "product": f"{p.prod_desc} - {p.prod_name}",
                "batch": stock_in_qs.first().batch if stock_in_qs.exists() else "",
                "balance_qty": balance_qty,
            })

    context = {
        "stock_data": stock_data,
    }

    return render(request, "stock_balance_report.html", context)
    
    
def test_messages(request):
    if request.method == "POST":
        # Just test a message
        messages.error(request, "This is an ERROR message!")
        messages.success(request, "This is a SUCCESS message!")
        return render(request, 'test_messages.html')  # render same page to show messages

    return render(request, 'test_messages.html')
    
# Reports New


from django.db.models import Sum

from django.db.models import Sum, Subquery, OuterRef

def index_stock(request):
    suppliers = supplier.objects.all().order_by('sup_name')
    sup_id = request.GET.get('sup_id')

    stock_data = []

    if sup_id:
        try:
            sup_id = int(sup_id)
        except:
            sup_id = None

        if sup_id:
            stock_data = (
                Location.objects
                .filter(sup_id=sup_id)
                .annotate(
                    prod_name=Subquery(
                        product.objects
                        .filter(prod_desc=OuterRef('prod_id'))  # ✅ relation
                        .values('prod_name')[:1]                # ✅ GET NAME
                    )
                )
                .values(
                    'location_name',
                    'prod_id',
                    'prod_name',
                    'batch_id'
                )
                .annotate(
                    total_good=Sum('blc'),
                    total_damage=Sum('block_stock')
                )
                .order_by('location_name')
            )

    return render(request, 'index_stock.html', {
        'suppliers': suppliers,
        'stock_data': stock_data,
        'selected_supplier': sup_id
    })
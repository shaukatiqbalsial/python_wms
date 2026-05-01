"""
URL configuration for wms1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from wms1 import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    
    path('userlist/',views.userlist, name="userlist"),
    path('', auth_views.LoginView.as_view(template_name='signin.html'), name='login'),
   
    #path('signin/',views.signin, name="signin"),
# Supplier    
    path('addsupplier/',views.addsupplier, name="addsupplier"),
    path('supplieradd',views.SupplierAdd,name='supplieradd'),
    path('supplierlist/',views.supplierlist, name="supplierlist"),
    path('editsupplier/<int:id>/',views.editsupplier, name="editsupplier"),
    path('updatesupplier/<int:id>/',views.UpdateSupplier,name='updatesupplier'),
    path('uploadperson',views.upload_excel,name='uploadperson'),
    path('export-excel',views.export_supplier_excel, name='export_supplier_excel'),
    
    path('supplier/pdf/', views.supplier_pdf, name='supplier_pdf'),
    path('supplier/print/', views.supplier_print, name='supplier_print'),

#Product
    #path('',views.aboutus, name="aboutus"),
    path('aboutus/',views.aboutus, name="aboutus"),
    path('productlist/',views.productlist, name="productlist"),
    path('addproduct/',views.addproduct, name="addproduct"),
    path('productadd/',views.ProductAdd, name="productadd"),
    path('productdetails/',views.productdetails, name="productdetails"),
    path('editproduct/<int:id>/',views.editproduct, name="editproduct"),
    path('updateproduct/<int:id>/',views.UpdateProduct, name='updateproduct'),
    path('uploadproduct',views.upload_excelproduct,name='uploadproduct'),
    path('export-excelproduct',views.export_product_excel, name='export_product_excel'),
    
    path('load-products/', views.load_products, name='load_products'),
    path('side/',views.side, name="side"),
    
# Barcode
    path('barcodelist/',views.barcodelist, name="barcodelist"),
    path('addbarcode/',views.addbarcode, name="addbarcode"),
    path('barcodeadd/',views.BarcodeAdd, name="barcodeadd"),

# Stock
    path('addstock/',views.addstock, name="addstock"),
    path('uploadstock',views.upload_excelstock,name='uploadstock'),
    
     
# ASN
   path('asn/',views.asn_load, name="asn_load"),
   path('export-asn-excel',views.export_asn_excel, name='export_asn_excel'),
   path('upload_asn',views.upload_asn,name='upload_asn'),
   
   path('deletesn/<int:id>/', views.deletesn, name='deletesn'),

   path('editasn/<int:id>/',views.editasn, name='editasn'),
   path('updateasn/<int:id>/',views.updateasn, name='updateasn'),
   
   path('process_asn',views.process_asn,name='process_asn'),
   
   path('asnview/', views.asn_view, name='asnview'),
   
# Gate Pass
path('gatepasslist/',views.gatepasslist, name="gatepasslist"),
path('addgpass/',views.addgpass, name="addgpass"),
path('gpassadd/',views.gpassadd, name="gpassadd"),
path('ingatepass_print/<int:id>/',views.ingatepass_print, name="ingatepass_print"),

# Received
path('addreceive/',views.addreceive, name="addreceive"),
path('receivelist/<str:rec_asnno>/',views.receivelist, name="receivelist"),
path('editrec/<int:id>/',views.editrec, name="editrec"),
path('updaterec/<int:id>/',views.UpdateRec, name='updaterec'),

# Locations
path('addlocation/',views.addlocation, name="addlocation"),
path('locationlist/<str:rec_asnno>/',views.locationlist, name="locationlist"),
path('editlocation/<int:id>/',views.editlocation, name="editlocation"),
path('updatelocation/<int:id>/',views.UpdateLocation, name='updatelocation'),

# D.N
   path('dn/',views.dn_load, name="dn_load"),
   path('export-dn-excel',views.export_dn_excel, name='export_dn_excel'),
   path('upload_dn',views.upload_dn,name='upload_dn'),
   path('editdn/<int:id>/',views.editdn, name='editdn'),
   path('updatedn/<int:id>/',views.updatedn, name='updatedn'),
   path('deletedn/<int:id>/', views.deletedn, name='deletedn'),
   path('process_dn',views.process_dn,name='process_dn'),

# Picking
   path('pick/',views.pick, name="pick"),
   path('pick_stock',views.pick_stock,name='pick_stock'),
   path('picking-report/', views.picking_report, name='picking_report'),
   path('confirm-pick/<int:id>/', views.confirm_pick, name='confirm_pick'),
   
# Outward Gate Pass

    path('outgatepasslist/',views.outgatepasslist, name="outgatepasslist"),
    path('outaddgpass/',views.outaddgpass, name="outaddgpass"),
    path('outgpassadd/',views.outgpassadd, name="outgpassadd"), 
    path('outgatepass_print/<int:id>/',views.outgatepass_print, name="outgatepass_print"),
    
# Reports
    path('stock_balance_report/',views.stock_balance_report, name="stock_balance_report"), 
    path('test-messages/', views.test_messages, name='test_messages'), 
    
    path('index-stock/', views.index_stock, name='index_stock'),
   
]

#if settings.DEBUG:
#    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


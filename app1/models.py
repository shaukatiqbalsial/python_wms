from django.db import models
from decimal import Decimal

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=100)   # text field
    password = models.CharField(max_length=50)  # text
    branch_id = models.IntegerField()          # integer
    status = models.TextField()  # optional text

    created_at = models.DateTimeField(auto_now_add=True)   # auto timestamp

    def __str__(self):
        return self.username  # makes objects readable in admin

# Create Supplier models here.
class supplier(models.Model):
    sup_name=models.CharField(max_length=100)
    sup_email=models.CharField(max_length=50)
    sup_phone=models.CharField(max_length=30)
    sup_country=models.CharField(max_length=30)
    sup_city=models.CharField(max_length=20)
    sup_address=models.CharField(max_length=200)
    sup_desc=models.CharField(max_length=300)
    sup_pic=models.ImageField(upload_to='supplier_images/', blank=True, null=True)
    sup_blc=models.FloatField(max_length=50, default=0)
   
    def __str__(self):
     return self.sup_name

# Create Product models here.
class product(models.Model):
    prod_name=models.CharField(max_length=100)
    prod_desc=models.CharField(max_length=50)
    prod_volume=models.CharField(max_length=30)
    prod_uom=models.CharField(max_length=30)
    prod_supid=models.CharField(max_length=10)
    prod_life=models.CharField(max_length=30)
    prod_weight=models.CharField(max_length=30)
    prod_condition=models.CharField(max_length=100)
    prod_branch=models.CharField(max_length=10)
    prod_pic=models.ImageField(upload_to='product_images/', blank=True, null=True)
    
    def __str__(self):
     return self.prod_name
     
# Create productbarcode here.
class productbarcode(models.Model):
    product_id=models.CharField(max_length=100)
    product_barcode=models.CharField(max_length=100)
    
    def __str__(self):
     return self.product_id
     
# Create ASN models here.
class asn_form(models.Model):
    asn_no=models.CharField(max_length=30)
    prod_id=models.CharField(max_length=50)
    item=models.CharField(max_length=100)
    batch=models.CharField(max_length=30)
    qty=models.CharField(max_length=10)
    branch_id=models.CharField(max_length=5)
    user_id=models.CharField(max_length=5)
    veh=models.CharField(max_length=30)
    trns=models.CharField(max_length=50)
    ctn=models.CharField(max_length=10, default=0)
    
    def __str__(self):
     return self.asn_no


# Create ASN models here.
class asn(models.Model):
    sup_id=models.CharField(max_length=10)
    prod_id=models.CharField(max_length=50)
    volume=models.CharField(max_length=30)
    uom=models.CharField(max_length=30)
    qty=models.CharField(max_length=10)
    branch_id=models.CharField(max_length=5)
    sno=models.CharField(max_length=30)
    batch=models.CharField(max_length=50)
    asn_no=models.CharField(max_length=30)
    veh=models.CharField(max_length=20, default='0')
    trns=models.CharField(max_length=30, default='0')
    ctn=models.CharField(max_length=10, default=0)
    remarks=models.CharField(max_length=100, default='')
    
    def __str__(self):
     return self.asn_no

# Create stockin models here.
class stockin(models.Model):
    rec_asnno=models.CharField(max_length=30)
    sup_id=models.CharField(max_length=10)
    prod_id=models.CharField(max_length=50)
    qty = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date=models.CharField(max_length=20)
    dt=models.CharField(max_length=20)
    branch_id=models.CharField(max_length=5)
    truck_no=models.CharField(max_length=15)
    remarks=models.CharField(max_length=50)
    transporter=models.CharField(max_length=50)
    user_id=models.CharField(max_length=5)
    final=models.CharField(max_length=5)
    serial_no=models.CharField(max_length=50)
    gatepass_id=models.CharField(max_length=10)
    asn_qty = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    asn_balance=models.DecimalField(max_digits=10, decimal_places=2, default=0)
    pack=models.CharField(max_length=10)
    pack_rec=models.CharField(max_length=10)
    Pack_blc=models.CharField(max_length=10)
    loose=models.CharField(max_length=10)
    loose_rec=models.CharField(max_length=10)
    loose_blc=models.CharField(max_length=10)
    batch=models.CharField(max_length=50)
    expiry=models.CharField(max_length=20)
    cond=models.CharField(max_length=20)
    cond_qty = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    return_status=models.CharField(max_length=20)
    return_qty=models.CharField(max_length=10)
    return_dat=models.CharField(max_length=10)
    return_gid=models.CharField(max_length=10)
    return_balance=models.CharField(max_length=10)
    rec_userid=models.CharField(max_length=5)
    rec_dat = models.DateField(auto_now=True)
    rec_tim = models.TimeField()
    location = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    access=models.CharField(max_length=10)
    mfg=models.CharField(max_length=20)
    checked=models.CharField(max_length=5)
    verified=models.CharField(max_length=5)
    approved=models.CharField(max_length=5)
    weightp=models.CharField(max_length=10)
    weight_rec=models.CharField(max_length=10)
    
    def __str__(self):
     return self.asn_no

# Create Gate Pass models here.
class gatepass(models.Model):
    gp_asnno=models.CharField(max_length=30, default=0)
    driver=models.CharField(max_length=10, default=0)
    cnic=models.CharField(max_length=30, default=0)
    mobile=models.CharField(max_length=20, default=0)
    typ=models.CharField(max_length=20)
    indt=models.CharField(max_length=50)
    outdt=models.CharField(max_length=50)
    branch_id=models.CharField(max_length=5)
    remarks=models.CharField(max_length=50)
    transporter=models.CharField(max_length=50)
    user_id=models.CharField(max_length=5)
    final=models.CharField(max_length=5)
    seal=models.CharField(max_length=50)
    
    def __str__(self):
     return self.gp_asnno
     
# Create stockin_detail models here.

class stockin_detail(models.Model):
    rec_id = models.ForeignKey(stockin, on_delete=models.CASCADE)
    qty = models.IntegerField(default=0)
    mfg = models.DateField()
    expiry = models.DateField()
    
    def __str__(self):
     return self.rec_id
     

class Location(models.Model):
    stockin = models.ForeignKey('stockin', on_delete=models.CASCADE, related_name='locations')
    prod_id = models.CharField(max_length=50, null=True, blank=True)
    batch_id = models.CharField(max_length=50, null=True, blank=True)
    sup_id = models.IntegerField(null=True, blank=True)
    
    blc = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))  # Balance quantity
    block_stock = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))  # Quantity blocked/reserved
    expire_stock = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))  # Quantity expired
    
    volume = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))  # Volume
    uom = models.CharField(max_length=100, null=True, blank=True)  # e.g., Pack
    branch = models.IntegerField(null=True, blank=True) # e.g., Pack
    
    
    location_name = models.CharField(max_length=100)  # e.g., A1, Rack 3
    dat = models.DateField(auto_now_add=True)  # Date of placing in location
    mfg_dat = models.DateField(null=True, blank=True)
    expiry_dat = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.prod_id} - {self.location_name} - {self.blc}"

# Create DN models here.
class dn_form(models.Model):
    dn_no=models.CharField(max_length=30)
    prod_id=models.CharField(max_length=50)
    item=models.CharField(max_length=100)
    batch=models.CharField(max_length=30)
    qty=models.CharField(max_length=10)
    veh=models.CharField(max_length=30)
    dealer=models.CharField(max_length=50)
    
    def __str__(self):
     return self.dn_no
     
# Create stockout models here.
class stockout(models.Model):
    stockout_orderno=models.CharField(max_length=30, default=0)
    sup_id=models.CharField(max_length=10, default=0)
    prod_id=models.CharField(max_length=50, default=0)
    qty = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    dat = models.DateField(auto_now_add=True)  # Date of placing in location
    dt=models.CharField(max_length=20, default=0)
    branch_id=models.CharField(max_length=5, default=0)
    truck_no=models.CharField(max_length=15, default=0)
    remarks=models.CharField(max_length=50, default=0)
    dealer=models.CharField(max_length=50, default=0)
    user_id=models.CharField(max_length=5, default=0)
    final=models.CharField(max_length=5, default=0)
    serial_no=models.CharField(max_length=50, default=0)
    gatepass_id=models.CharField(max_length=10, default=0)
    dn_qty = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    dnn_balance=models.DecimalField(max_digits=10, decimal_places=2, default=0)
    volume=models.CharField(max_length=30, default=0)
    uom=models.CharField(max_length=30, default=0)
    pack=models.CharField(max_length=10, default=0)
    pack_deliver=models.CharField(max_length=10, default=0)
    Pack_blc=models.CharField(max_length=10, default=0)
    loose=models.CharField(max_length=10, default=0)
    loose_rec=models.CharField(max_length=10, default=0)
    loose_blc=models.CharField(max_length=10, default=0)
    batch=models.CharField(max_length=50, default=0)
    expiry=models.CharField(max_length=20, default=0)
    return_status=models.CharField(max_length=20, default=0)
    return_qty=models.CharField(max_length=10, default=0)
    return_dat=models.CharField(max_length=10, default=0)
    return_gid=models.CharField(max_length=10, default=0)
    return_balance=models.CharField(max_length=10, default=0)
    rec_userid=models.CharField(max_length=5, default=0)
    weightp=models.CharField(max_length=10, default=0)
    weight_rec=models.CharField(max_length=10, default=0)
    
    def __str__(self):
     return self.stockout_orderno
     
# Create D.N models here.
class dn(models.Model):
    sup_id=models.CharField(max_length=10)
    prod_id=models.CharField(max_length=50)
    volume=models.CharField(max_length=30)
    uom=models.CharField(max_length=30)
    qty=models.CharField(max_length=10)
    branch_id=models.CharField(max_length=5)
    sno=models.CharField(max_length=30)
    batch=models.CharField(max_length=50)
    dn_no=models.CharField(max_length=30)
    veh=models.CharField(max_length=20, default=0)
    dealer=models.CharField(max_length=30, default=0)
    remarks=models.CharField(max_length=100, default=0)
    def __str__(self): 
     return self.dn_no

class PickingHistory(models.Model):
    stockout = models.ForeignKey(stockout, on_delete=models.CASCADE)
    prod_id = models.IntegerField()
    batch_id = models.IntegerField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    picked_qty = models.DecimalField(max_digits=10, decimal_places=2)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    pick_date = models.DateField(auto_now_add=True)
    pick_time = models.TimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    picked_confirm_user = models.CharField(max_length=100, null=True, blank=True)
    picked_confirm_date = models.DateField(null=True, blank=True)
    picked_confirm_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.stockout.dn_no} - {self.picked_qty}"
        
# Create Outward Gate Pass models here.
class outgatepass(models.Model):
    gp_asnno=models.CharField(max_length=30, default=0)
    dealer=models.CharField(max_length=200, default=0)
    driver=models.CharField(max_length=10, default=0)
    cnic=models.CharField(max_length=30, default=0)
    mobile=models.CharField(max_length=20, default=0)
    typ=models.CharField(max_length=20)
    indt=models.CharField(max_length=50)
    outdt=models.CharField(max_length=50)
    branch_id=models.CharField(max_length=5)
    remarks=models.CharField(max_length=50)
    transporter=models.CharField(max_length=50)
    user_id=models.CharField(max_length=5)
    final=models.CharField(max_length=5)
    seal=models.CharField(max_length=50)
    
    def __str__(self):
     return self.gp_asnno
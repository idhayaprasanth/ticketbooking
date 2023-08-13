from django.db import models
from django.core.validators import MinLengthValidator,RegexValidator
import qrcode
from io import BytesIO
from django.core.files import File
from django.db.models.signals import post_save
from django.dispatch import receiver




# Create your models here.
class create_bus(models.Model):
    busname=models.CharField(max_length=500 ,blank=False,default="name")
    bustype=models.CharField(max_length=500,blank=False)
    contact=models.IntegerField(blank=False,default="0")
    stop1=models.CharField(max_length=500 ,blank=True,)
    stop2=models.CharField(max_length=500 ,blank=True)
    stop3=models.CharField(max_length=500 ,blank=True)
    stop4=models.CharField(max_length=500 ,blank=True)
    stop5=models.CharField(max_length=500 ,blank=True)
    ticket1=models.IntegerField(blank=True,default="0")
    ticket2=models.IntegerField(blank=True,default="0")
    ticket3=models.IntegerField(blank=True,default="0")
    ticket4=models.IntegerField(blank=True,default="0")
    ticket5=models.IntegerField(blank=True,default="0")
    ticket6=models.IntegerField(blank=True,default="0")
    ticket7=models.IntegerField(blank=True,default="0")
    ticket8=models.IntegerField(blank=True,default="0")    
    ticket9=models.IntegerField(blank=True,default="0")
    ticket10=models.IntegerField(blank=True,default="0") 
    ifsc = models.CharField(
        max_length=100,
        default="A1",
        validators=[
            RegexValidator(
                regex=r'^(?=.*[a-zA-Z])(?=.*\d)[a-zA-Z\d]+$',
                message="Field must contain at least one letter and one number."
            ),
            MinLengthValidator(8)
        ]
    ) 
    accountno=models.IntegerField(blank=False,unique=True,default="0")
    bankname=models.CharField(max_length=500 ,blank=False,default="BankName")
    qr_code = models.ImageField(upload_to='qr_codes', blank=True)

    def generate_qr_code(self):
        # Generate the QR code using the bus details
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        data = f"busname: {self.busname}\nbustype: {self.bustype}\ncontact:{self.contact}\nstop1:{self.stop1}\nstop2:{self.stop2}\nstop3:{self.stop3}\nstop4:{self.stop4}\nstop5:{self.stop5}\nticket1:{self.ticket1}\nticket2:{self.ticket2}\nticket3:{self.ticket3}\nticket4:{self.ticket4}\nticket5:{self.ticket5}\nticket6:{self.ticket6}\nticket7:{self.ticket7}\nticket8:{self.ticket8}\nticket9:{self.ticket9}\nticket10:{self.ticket10}\nifsc:{self.ifsc}\naccountno:{self.accountno}\nbankname:{self.bankname}"
        qr.add_data(data)
        qr.make(fit=True)

        # Create a stream to save the QR code image
        qr_img = qr.make_image(fill_color="black", back_color="white")
        stream = BytesIO()
        qr_img.save(stream)
        stream.seek(0)

        # Save the QR code image to the qr_code field
        self.qr_code.save(f'qr_code_{self.pk}.png', File(stream), save=False)

@receiver(post_save, sender=create_bus)
def generate_bus_qr_code(sender, instance, created, **kwargs):
    if created:
        instance.generate_qr_code()
        instance.save()




    

def __str__(self):
    return 'creat_bus details are shared'
def __str__(self):
    return self.title
def snipet(self):
    return self.posts[: 100]+'...'
from django.core.management import BaseCommand

from documents.models import SupportedExtension


class Command(BaseCommand):
    def handle(self, *args, **options):
        SupportedExtension.objects.get_or_create(name="3gp")
        SupportedExtension.objects.get_or_create(name="7z")
        SupportedExtension.objects.get_or_create(name="ae")
        SupportedExtension.objects.get_or_create(name="ai")
        SupportedExtension.objects.get_or_create(name="apk")
        SupportedExtension.objects.get_or_create(name="asf")
        SupportedExtension.objects.get_or_create(name="avi")
        SupportedExtension.objects.get_or_create(name="bak")
        SupportedExtension.objects.get_or_create(name="bmp")
        SupportedExtension.objects.get_or_create(name="cdr")
        SupportedExtension.objects.get_or_create(name="css")
        SupportedExtension.objects.get_or_create(name="csv")
        SupportedExtension.objects.get_or_create(name="divx")
        SupportedExtension.objects.get_or_create(name="dll")
        SupportedExtension.objects.get_or_create(name="doc")
        SupportedExtension.objects.get_or_create(name="docx")
        SupportedExtension.objects.get_or_create(name="dw")
        SupportedExtension.objects.get_or_create(name="dwg")
        SupportedExtension.objects.get_or_create(name="eps")
        SupportedExtension.objects.get_or_create(name="exe")
        SupportedExtension.objects.get_or_create(name="flv")
        SupportedExtension.objects.get_or_create(name="fw")
        SupportedExtension.objects.get_or_create(name="gif")
        SupportedExtension.objects.get_or_create(name="gz")
        SupportedExtension.objects.get_or_create(name="html")
        SupportedExtension.objects.get_or_create(name="ico")
        SupportedExtension.objects.get_or_create(name="iso")
        SupportedExtension.objects.get_or_create(name="jar")
        SupportedExtension.objects.get_or_create(name="jpg")
        SupportedExtension.objects.get_or_create(name="js")
        SupportedExtension.objects.get_or_create(name="mov")
        SupportedExtension.objects.get_or_create(name="mp3")
        SupportedExtension.objects.get_or_create(name="mp4")
        SupportedExtension.objects.get_or_create(name="mpeg")
        SupportedExtension.objects.get_or_create(name="pdf")
        SupportedExtension.objects.get_or_create(name="php")
        SupportedExtension.objects.get_or_create(name="png")
        SupportedExtension.objects.get_or_create(name="ppt")
        SupportedExtension.objects.get_or_create(name="ps")
        SupportedExtension.objects.get_or_create(name="psd")
        SupportedExtension.objects.get_or_create(name="rar")
        SupportedExtension.objects.get_or_create(name="svg")
        SupportedExtension.objects.get_or_create(name="swf")
        SupportedExtension.objects.get_or_create(name="sys")
        SupportedExtension.objects.get_or_create(name="tar")
        SupportedExtension.objects.get_or_create(name="tiff")
        SupportedExtension.objects.get_or_create(name="txt")
        SupportedExtension.objects.get_or_create(name="wav")
        SupportedExtension.objects.get_or_create(name="zip")

        self.stdout.write(self.style.SUCCESS("Successfully populated the database."))


from .models import *

# Register your models here.

admin.site.register(Dossiers)
admin.site.register(Sections, SectionsAdmin)
admin.site.register(Document, DocumentAdmin)
admin.site.register(Tags)
admin.site.register(AuditLog)

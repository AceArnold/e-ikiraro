from ninja import Router
from .models import Service, Application, PassportApplication, NationalIDApplication, DriversLicenseApplication, Payment, Document
from django.contrib.auth.models import User

service_router = Router()
application_router = Router()
passport_router = Router()
id_router = Router()
license_router = Router()
payment_router = Router()
document_router = Router()
user_router = Router()

@user_router.get("/", summary="List all users")
def list_users(request):
    return [{"id": u.id, "username": u.username, "email": u.email} for u in User.objects.all()]

@service_router.get("/", summary="List all services")
def list_services(request):
    return [{"id": str(s.id), "name": s.name, "fee": float(s.base_fee)} for s in Service.objects.all()]

@application_router.get("/", summary="List all applications")
def list_applications(request):
    return [{"id": str(a.id), "user": a.user.username, "service": a.service.name if a.service else None, "status": a.status} for a in Application.objects.all()]

@passport_router.get("/", summary="List all passport applications")
def list_passport_applications(request):
    return [{"id": str(p.application.id), "user": p.application.user.username, "passport_type": p.passport_type} for p in PassportApplication.objects.all()]

@id_router.get("/", summary="List all national ID applications")
def list_national_id_applications(request):
    return [{"id": str(n.application.id), "user": n.application.user.username, "father_name": n.father_name, "mother_name": n.mother_name} for n in NationalIDApplication.objects.all()]

@license_router.get("/", summary="List all driver's license applications")
def list_drivers_license_applications(request):
    return [{"id": str(l.application.id), "user": l.application.user.username, "license_type": l.license_type} for l in DriversLicenseApplication.objects.all()]

@payment_router.get("/", summary="List all payments")
def list_payments(request):
    return [{"id": str(p.id), "application_id": str(p.application.id), "amount": float(p.amount), "status": p.status} for p in Payment.objects.all()]

@document_router.get("/", summary="List all documents")
def list_documents(request):
    return [{"id": str(d.id), "application_id": str(d.application.id), "document_type": d.document_type, "file_url": d.file.url} for d in Document.objects.all()]


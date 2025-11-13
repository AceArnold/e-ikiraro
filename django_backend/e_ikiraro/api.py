from ninja import Router
from ninja import UploadedFile, File, Form
from .models import Service, PassportApplication, NationalIDApplication, DriversLicenseApplication, Payment, Document
from django.contrib.auth.models import User

service_router = Router()
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
    return [{"id": str(s.id), "name": s.name, "description": s.description, "fee": float(s.base_fee)} for s in Service.objects.all()]

@passport_router.get("/", summary="List all passport applications")
def list_passport_applications(request):
    return [{"id": str(p.id), "user": p.user.username, "passport_type": p.passport_type, "status": p.status} for p in PassportApplication.objects.all()]

@id_router.get("/", summary="List all national ID applications")
def list_national_id_applications(request):
    return [{"id": str(n.id), "user": n.user.username, "father_name": n.father_name, "mother_name": n.mother_name, "status": n.status} for n in NationalIDApplication.objects.all()]

@license_router.get("/", summary="List all driver's license applications")
def list_drivers_license_applications(request):
    return [{"id": str(l.id), "user": l.user.username, "license_type": l.license_type, "address": l.address, "status": l.status, "driving_school_certificate": l.driving_school_certificate.name if l.driving_school_certificate else None} for l in DriversLicenseApplication.objects.all()]


@license_router.post("/")
def submit_license_application(
    request,
    license_type: str = Form(...),
    photo: UploadedFile = File(...),
    medical_certificate: UploadedFile = File(...),
    eye_test_certificate: UploadedFile = File(...),
    national_id: UploadedFile = File(...),
    address: str = Form(...),
    driving_school_certificate: UploadedFile = File(None)
):
    # Get the current user (or create/get anonymous user)
    if request.user.is_authenticated:
        user = request.user
    else:
        user, _ = User.objects.get_or_create(username="anonymous", defaults={"email": "anonymous@example.com"})
    
    # Create the DriversLicenseApplication directly (no parent Application needed)
    license_app = DriversLicenseApplication.objects.create(
        user=user,
        license_type=license_type,
        photo=photo,
        medical_certificate=medical_certificate,
        eye_test_certificate=eye_test_certificate,
        national_id=national_id,
        address=address,
        driving_school_certificate=driving_school_certificate if driving_school_certificate else "",
        status="Pending"
    )
    return {"message": "Application submitted successfully", "id": str(license_app.id)}



@payment_router.get("/", summary="List all payments")
def list_payments(request):
    out = []
    for p in Payment.objects.all():
        app_type = None
        app_id = None
        if p.passport_application_id:
            app_type = 'passport'
            app_id = str(p.passport_application_id)
        elif p.national_id_application_id:
            app_type = 'national_id'
            app_id = str(p.national_id_application_id)
        elif p.drivers_license_application_id:
            app_type = 'drivers_license'
            app_id = str(p.drivers_license_application_id)
        out.append({
            "id": str(p.id),
            "application_type": app_type,
            "application_id": app_id,
            "amount": float(p.amount),
            "status": p.status,
            "transaction_id": p.transaction_id,
        })
    return out

@document_router.get("/", summary="List all documents")
def list_documents(request):
    out = []
    for d in Document.objects.all():
        app_type = None
        app_id = None
        if d.passport_application_id:
            app_type = 'passport'
            app_id = str(d.passport_application_id)
        elif d.national_id_application_id:
            app_type = 'national_id'
            app_id = str(d.national_id_application_id)
        elif d.drivers_license_application_id:
            app_type = 'drivers_license'
            app_id = str(d.drivers_license_application_id)
        out.append({
            "id": str(d.id),
            "application_type": app_type,
            "application_id": app_id,
            "document_type": d.document_type,
            "file_url": d.file.url,
        })
    return out


# POST endpoints

@service_router.post("/", summary="Create a service")
def create_service(request, name: str = Form(...), description: str = Form(...), base_fee: float = Form(0.0)):
    s, created = Service.objects.get_or_create(name=name, defaults={
        'description': description,
        'base_fee': base_fee,
    })
    return {"id": str(s.id), "created": created}


@passport_router.post("/", summary="Submit passport application")
def submit_passport_application(request,
    passport_type: str = Form(...),
    passport_photo: UploadedFile = File(...),
    birth_certificate: UploadedFile = File(...),
    national_id: UploadedFile = File(...),
):
    if request.user.is_authenticated:
        user = request.user
    else:
        user, _ = User.objects.get_or_create(username="anonymous", defaults={"email": "anonymous@example.com"})
    app = PassportApplication.objects.create(
        user=user,
        passport_type=passport_type,
        passport_photo=passport_photo,
        birth_certificate=birth_certificate,
        national_id=national_id,
        status='Pending',
    )
    return {"message": "Passport submitted", "id": str(app.id)}


@id_router.post("/", summary="Submit national ID application")
def submit_national_id_application(request,
    father_name: str = Form(...),
    mother_name: str = Form(...),
    birth_certificate: UploadedFile = File(...),
    address: str = Form(...),
):
    if request.user.is_authenticated:
        user = request.user
    else:
        user, _ = User.objects.get_or_create(username="anonymous", defaults={"email": "anonymous@example.com"})
    app = NationalIDApplication.objects.create(
        user=user,
        father_name=father_name,
        mother_name=mother_name,
        birth_certificate=birth_certificate,
        address=address,
        status='Pending',
    )
    return {"message": "National ID submitted", "id": str(app.id)}


@payment_router.post("/", summary="Create a payment")
def create_payment(request,
    application_type: str = Form(...),
    application_id: str = Form(...),
    service_type: str = Form(...),
    amount: float = Form(...),
    payment_method: str = Form(...),
    transaction_id: str = Form(...),
    provider_reference: str = Form(...),
):
    if request.user.is_authenticated:
        user = request.user
    else:
        user, _ = User.objects.get_or_create(username="anonymous", defaults={"email": "anonymous@example.com"})
    kwargs = {
        'user': user,
        'service_type': service_type,
        'amount': amount,
        'payment_method': payment_method,
        'transaction_id': transaction_id,
        'provider_reference': provider_reference,
        'status': 'Pending',
    }
    if application_type == 'passport':
        kwargs['passport_application_id'] = application_id
    elif application_type == 'national_id':
        kwargs['national_id_application_id'] = application_id
    elif application_type == 'drivers_license':
        kwargs['drivers_license_application_id'] = application_id
    else:
        return {"error": "unknown application_type"}
    p = Payment.objects.create(**kwargs)
    return {"message": "payment created", "id": str(p.id)}


@document_router.post("/", summary="Upload a document")
def upload_document(request,
    document_type: str = Form(...),
    file: UploadedFile = File(...),
    application_type: str = Form(...),
    application_id: str = Form(...),
):
    if request.user.is_authenticated:
        user = request.user
    else:
        user, _ = User.objects.get_or_create(username="anonymous", defaults={"email": "anonymous@example.com"})
    kwargs = {'user': user, 'document_type': document_type, 'file': file}
    if application_type == 'passport':
        kwargs['passport_application_id'] = application_id
    elif application_type == 'national_id':
        kwargs['national_id_application_id'] = application_id
    elif application_type == 'drivers_license':
        kwargs['drivers_license_application_id'] = application_id
    else:
        return {"error": "unknown application_type"}
    d = Document.objects.create(**kwargs)
    return {"message": "document uploaded", "id": str(d.id)}


@user_router.post("/", summary="Create user")
def create_user(request, username: str = Form(...), email: str = Form(""), password: str = Form(...)):
    u = User.objects.create_user(username=username, email=email, password=password)
    return {"id": u.id, "username": u.username}


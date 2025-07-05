from fastapi import APIRouter, HTTPException, Form, Query, UploadFile, File, Depends, Query, Path, Body
from typing import List, Optional
from datetime import datetime
from database import get_db
from modals.workers import Worker, Address, EmergencyContact, BankDetails, PoliceVerification, LocalReference, PreviousEmployer, Education
from sqlalchemy.orm import Session
from schema import workers
from sqlalchemy import or_
from urllib.parse import quote
import shutil
import os
import dotenv
import re
import json
import sqlalchemy
from schema.workers import WorkerRegisterRequest


dotenv.load_dotenv()
URL = os.getenv('URL')


router = APIRouter(
    tags = ["New Workers"],
    prefix = '/new_workers'
)

UPLOAD_DIR = "uploads-workers"
PHOTOS_DIR = os.path.join(UPLOAD_DIR, "photos")
DOCS_DIR = os.path.join(UPLOAD_DIR, "documents")
LIVE_CAPTURE_DIR = os.path.join(PHOTOS_DIR, "live-capture")
PHOTOSHOOT_DIR = os.path.join(PHOTOS_DIR, "photoshoot")

os.makedirs(PHOTOS_DIR, exist_ok=True)
os.makedirs(DOCS_DIR, exist_ok=True)
os.makedirs(LIVE_CAPTURE_DIR, exist_ok=True)
os.makedirs(PHOTOSHOOT_DIR, exist_ok=True)

@router.get("/{name}")
async def search_workers(name: str):
    try:
        db = next(get_db())
        
        if name:
            workers = db.query(Worker).filter(
                or_(
                    Worker.full_name.ilike(f"%{name}%"),
                    # Worker.email.ilike(f"%{name}%"),
                    # Worker.city.ilike(f"%{name}%")
                )
            ).all()
        else:
            workers = db.query(Worker).all()
        
        worker_list = []
        for worker in workers:
            created_at_val = worker.created_at
            if created_at_val is not None and not isinstance(created_at_val, sqlalchemy.Column):
                created_at_str = created_at_val.isoformat()
            else:
                created_at_str = None
            worker_dict = {
                "id": worker.id,
                "full_name": worker.full_name,
                "gender": worker.gender,
                "age": worker.age,
                "dob": worker.dob,
                "phone": worker.phone,
                "alternate_phone": worker.alternate_phone,
                "email": worker.email,
                "city": worker.city,
                "blood_group": worker.blood_group,
                "primary_service_category": worker.primary_service_category,
                "experience_years": worker.experience_years,
                "experience_months": worker.experience_months,
                "aadhar_number": worker.aadhar_number,
                "pan_number": worker.pan_number,
                "electricity_bill_url": worker.electricity_bill_url,
                "profile_photo_url": worker.profile_photo_url,
                "live_capture_url": worker.live_capture_url,
                "photoshoot_url": worker.photoshoot_url,
                "created_at": created_at_str,
                "status": worker.status,
                "religion": worker.religion
            }
            worker_list.append(worker_dict)
        
        return {
            "status": "success",
            "count": len(worker_list),
            "workers": worker_list
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()


@router.get('/')
async def get_workers(db: Session = Depends(get_db)):
    workers = db.query(Worker).all()
    result = []
    for worker in workers:
        # Get addresses by type
        addresses = {a.type: a for a in worker.addresses}
        permanent_address = addresses.get('permanent')
        current_address = addresses.get('current')
        # Compose response
        created_at_val = worker.created_at
        if created_at_val is not None and not isinstance(created_at_val, sqlalchemy.Column):
            created_at_str = created_at_val.isoformat()
        else:
            created_at_str = None
        result.append({
            "id": worker.id,
            "fullName": worker.full_name,
            "gender": worker.gender,
            "age": worker.age,
            "dateOfBirth": worker.dob if worker.dob is not None and not isinstance(worker.dob, sqlalchemy.Column) else None,
            "phone": worker.phone,
            "alternateMobile": worker.alternate_phone,
            "email": worker.email,
            "city": worker.city,
            "bloodGroup": worker.blood_group,
            "profilePhotoUrl": worker.profile_photo_url,
            "livecaptureurl": worker.live_capture_url,
            "photoshootUrl": worker.photoshoot_url,
            "primaryServiceCategory": worker.primary_service_category,
            "workExperience": {
                "years": worker.experience_years,
                "months": worker.experience_months
            },
            "languagesSpoken": worker.languages_spoken,
            "availability": worker.availability,
            "aadharNumber": worker.aadhar_number,
            "panNumber": worker.pan_number,
            "electricityBillUrl": worker.electricity_bill_url,
            "policeVerification": {
                "status": worker.police_verification.status if worker.police_verification else None,
                "documentUrl": worker.police_verification.document_url if worker.police_verification else None,
                "verificationDate": worker.police_verification.verification_date if worker.police_verification else None,
                "remarks": worker.police_verification.remarks if worker.police_verification else None
            } if worker.police_verification else None,
            "bankDetails": {
                "ifscCode": worker.bank_details.ifsc_code if worker.bank_details else None,
                "accountNumber": worker.bank_details.account_number if worker.bank_details else None,
                "bankName": worker.bank_details.bank_name if worker.bank_details else None
            } if worker.bank_details else None,
            "permanentAddress": {
                "line1": permanent_address.line1 if permanent_address else None,
                "city": permanent_address.city if permanent_address else None,
                "state": permanent_address.state if permanent_address else None,
                "zipCode": permanent_address.zip_code if permanent_address else None
            } if permanent_address else None,
            "currentAddress": {
                "line1": current_address.line1 if current_address else None,
                "city": current_address.city if current_address else None,
                "state": current_address.state if current_address else None,
                "zipCode": current_address.zip_code if current_address else None
            } if current_address else None,
            "emergencyContacts": [
                {
                    "name": c.name,
                    "relation": c.relation,
                    "phone": c.phone
                } for c in worker.emergency_contacts
            ],
            "localReferences": [
                {
                    "name": r.name,
                    "relation": r.relation,
                    "phone": r.phone
                } for r in worker.references
            ],
            "previousEmployer": [
                {
                    "companyName": e.company_name,
                    "position": e.position,
                    "duration": e.duration
                } for e in worker.employers
            ],
            "education": [
                {
                    "degree": edu.degree,
                    "institution": edu.institution,
                    "yearOfPassing": edu.year_of_passing
                } for edu in worker.education
            ],
            "status": worker.status,
            "religion": worker.religion,
            "bio": worker.bio,
            "createdAt": created_at_str
        })
    return result

@router.post("/register-worker", response_model=dict)
async def register_worker(
    worker: WorkerRegisterRequest = Body(..., example={
        "fullName": "Shantanu",
        "gender": "Male",
        "age": 30,
        "dob" : "1993-01-01",
        "phone": "1234567890",
        "alternateMobile": "0987654321",
        "email": "shan@example.com",
        "city": "Mumbai",
        "bloodGroup": "B+",
        "primaryServiceCategory": ["Cleaning"],
        "workExperience": {"years": 3, "months": 6},
        "languagesSpoken": ["Hindi", "Marathi"],
        "availability": ["Morning", "Evening"],
        "aadharNumber": "1234-5678-9012",
        "panNumber": "ABCDE1234F",
        "addresses": [
            {"line1": "123 Street", "city": "Mumbai", "state": "MH", "zipCode": "400001"},
            {"line1": "456 Lane", "city": "Pune", "state": "MH", "zipCode": "411001"}
        ],
        "emergencyContacts": [{"name": "Mom", "relation": "Mother", "phone": "1112223333"}],
        "localReferences": [{"name": "Ravi", "relation": "Friend", "phone": "9998887777"}],
        "previousEmployer": [{"companyName": "CleanCo", "position": "Cleaner", "duration": "1 year"}],
        "education": [{"degree": "10th", "institution": "SSC Board", "yearOfPassing": "2010"}],
        "bankDetails": {
            "ifscCode": "HDFC0001234",
            "accountNumber": "123456789012",
            "bankName": "HDFC Bank"
        },
        "policeVerification": {
            "status": "verified",
            "documentUrl": "http://example.com/doc.pdf",
            "verificationDate": "2024-01-01",
            "remarks": "Clear"
        }
    }),
    db: Session = Depends(get_db)
):
    # Save to DB logic here
    # return {"msg": "Worker registered successfully!"}

    try:
        # Use by_alias=True to get the original JSON keys
        data = worker.model_dump(by_alias=True)
        work_exp = data.get('workExperience', {})
        experience_years = work_exp.get('years', 0)
        experience_months = work_exp.get('months', 0)
        new_worker = Worker(
            full_name=data.get('fullName'),
            # gender=data.get('gender'),
            gender = data.get('gender', '').lower() or None,
            age=data.get('age'),
            dob=data.get('dob'),
            phone=data.get('phone'),
            alternate_phone=data.get('alternateMobile'),
            email=data.get('email'),
            city=data.get('city'),
            blood_group=data.get('bloodGroup'),
            primary_service_category=[data.get('primaryServiceCategory')] if isinstance(data.get('primaryServiceCategory'), str) else data.get('primaryServiceCategory'),
            experience_years=experience_years,
            experience_months=experience_months,
            languages_spoken=data.get('languagesSpoken'),
            availability=data.get('availability'),
            aadhar_number=data.get('aadharNumber'),
            pan_number=data.get('panNumber'),
            status="Pending",
            religion = data.get('religion', 'any').lower(),
            bio="",
            profile_photo_url=data.get('profilePhotoUrl'),
            electricity_bill_url=data.get('electricityBillUrl')
        )
        # db.add(new_worker)
        # db.flush()
        # # Addresses
        # if data.get('permanentAddress'):
        #     db.add(Address(worker_id=new_worker.id, type='permanent', **data['permanentAddress']))
        # if data.get('currentAddress'):
        #     db.add(Address(worker_id=new_worker.id, type='current', **data['currentAddress']))
        # # Emergency Contacts
        # for c in data.get('emergencyContacts', []):
        #     db.add(EmergencyContact(worker_id=new_worker.id, **c))
        # # Local References
        # for r in data.get('localReferences', []):
        #     db.add(LocalReference(worker_id=new_worker.id, **r))
        # # Previous Employers
        # # for e in data.get('previousEmployer', []):
        # #     db.add(PreviousEmployer(worker_id=new_worker.id, **e))

        # for e in worker.employers:  # <-- uses field name, not alias
        #     db.add(PreviousEmployer(worker_id=new_worker.id, **e.model_dump()))
        # # Education
        # for edu in data.get('education', []):
        #     db.add(Education(worker_id=new_worker.id, **edu))
        # # Bank Details
        # if data.get('bankDetails'):
        #     db.add(BankDetails(worker_id=new_worker.id, **data['bankDetails']))
        # # Police Verification
        # if data.get('policeVerification'):
        #     db.add(PoliceVerification(worker_id=new_worker.id, **data['policeVerification']))
        # db.commit()
        # db.refresh(new_worker)
        db.add(new_worker)
        db.flush()

        # Addresses (assuming Address model has a 'type' column: 'permanent' or 'current')
        for addr_type, key in [('permanent', 'permanentAddress'), ('current', 'currentAddress')]:
            addr_data = data.get(key)
            if addr_data:
                db.add(Address(worker_id=new_worker.id, type=addr_type, **addr_data))

        # Emergency Contacts
        for contact in worker.emergency_contacts:
            db.add(EmergencyContact(worker_id=new_worker.id, **contact.model_dump()))

        # Local References
        for ref in worker.references:
            db.add(LocalReference(worker_id=new_worker.id, **ref.model_dump()))

        # Previous Employers
        for emp in worker.employers:
            db.add(PreviousEmployer(worker_id=new_worker.id, **emp.model_dump()))

        # Education
        for edu in worker.education:
            db.add(Education(worker_id=new_worker.id, **edu.model_dump()))

        # Bank Details
        if worker.bank_details:
            db.add(BankDetails(worker_id=new_worker.id, **worker.bank_details.model_dump()))

        # Police Verification
        if worker.police_verification:
            db.add(PoliceVerification(worker_id=new_worker.id, **worker.police_verification.model_dump()))

        db.commit()
        db.refresh(new_worker)

        return {"status": "success", "worker_id": new_worker.id}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# @router.put("/update-worker/{worker_id}", response_model=dict)
# async def update_worker(
#     worker_id: int,
#     worker: WorkerRegisterRequest = Body(..., example={
#         "fullName": "string",
#         "gender": "string",
#         "age": 30,
#         "dateOfBirth": "1990-01-01",
#         "phone": "string",
#         "alternateMobile": "string",
#         "email": "string",
#         "city": "string",
#         "bloodGroup": "string",
#         "profilePhotoUrl": "string",
#         "primaryServiceCategory": "string",
#         "workExperience": {"years": 5, "months": 6},
#         "languagesSpoken": ["string"],
#         "availability": ["string"],
#         "preferredCommunity": ["string"],
#         "aadharNumber": "string",
#         "panNumber": "string",
#         "electricityBillUrl": "string",
#         "policeVerification": {
#             "status": "string",
#             "documentUrl": "string",
#             "verificationDate": "string",
#             "remarks": "string"
#         },
#         "bankDetails": {
#             "ifscCode": "string",
#             "accountNumber": "string",
#             "bankName": "string"
#         },
#         "permanentAddress": {
#             "line1": "string",
#             "city": "string",
#             "state": "string",
#             "zipCode": "string"
#         },
#         "currentAddress": {
#             "line1": "string",
#             "city": "string",
#             "state": "string",
#             "zipCode": "string"
#         },
#         "emergencyContacts": [
#             {"name": "string", "relation": "string", "phone": "string"}
#         ],
#         "localReferences": [
#             {"name": "string", "relation": "string", "phone": "string"}
#         ],
#         "previousEmployers": [
#             {"companyName": "string", "position": "string", "duration": "string"}
#         ],
#         "education": [
#             {"degree": "string", "institution": "string", "yearOfPassing": "string"}
#         ]
#     }),
#     db: Session = Depends(get_db)
# ):
#     db_worker = db.query(Worker).filter(Worker.id == worker_id).first()
#     if not db_worker:
#         raise HTTPException(status_code=404, detail="Worker not found")
#     try:
#         data = worker.model_dump(by_alias=True)
#         work_exp = data.get('workExperience', {})
#         db_worker.full_name = data.get('fullName', db_worker.full_name)
#         db_worker.gender = data.get('gender', db_worker.gender)
#         db_worker.age = data.get('age', db_worker.age)
#         db_worker.dob = data.get('dateOfBirth', db_worker.dob)
#         db_worker.phone = data.get('phone', db_worker.phone)
#         db_worker.alternate_phone = data.get('alternateMobile', db_worker.alternate_phone)
#         db_worker.email = data.get('email', db_worker.email)
#         db_worker.city = data.get('city', db_worker.city)
#         db_worker.blood_group = data.get('bloodGroup', db_worker.blood_group)
#         # Fix for primary_service_category assignment
#         psc = data.get('primaryServiceCategory')
#         if isinstance(psc, str):
#             db_worker.primary_service_category = [psc]
#         elif isinstance(psc, list):
#             db_worker.primary_service_category = [str(x) for x in psc if x is not None]
#         else:
#             db_worker.primary_service_category = db_worker.primary_service_category
#         db_worker.experience_years = work_exp.get('years', db_worker.experience_years)
#         db_worker.experience_months = work_exp.get('months', db_worker.experience_months)
#         db_worker.languages_spoken = data.get('languagesSpoken', db_worker.languages_spoken)
#         db_worker.availability = data.get('availability', db_worker.availability)
#         db_worker.aadhar_number = data.get('aadharNumber', db_worker.aadhar_number)
#         db_worker.pan_number = data.get('panNumber', db_worker.pan_number)
#         db_worker.profile_photo_url = data.get('profilePhotoUrl', db_worker.profile_photo_url)
#         db_worker.electricity_bill_url = data.get('electricityBillUrl', db_worker.electricity_bill_url)
#         # Addresses
#         addresses = {a.type: a for a in db_worker.addresses}
#         if data.get('permanentAddress'):
#             if 'permanent' in addresses:
#                 for k, v in data['permanentAddress'].items():
#                     setattr(addresses['permanent'], k, v)
#             else:
#                 db.add(Address(worker_id=db_worker.id, type='permanent', **data['permanentAddress']))
#         if data.get('currentAddress'):
#             if 'current' in addresses:
#                 for k, v in data['currentAddress'].items():
#                     setattr(addresses['current'], k, v)
#             else:
#                 db.add(Address(worker_id=db_worker.id, type='current', **data['currentAddress']))
#         # Emergency Contacts
#         db.query(EmergencyContact).filter(EmergencyContact.worker_id == db_worker.id).delete()
#         for c in data.get('emergencyContacts', []):
#             db.add(EmergencyContact(worker_id=db_worker.id, **c))
#         # Local References
#         db.query(LocalReference).filter(LocalReference.worker_id == db_worker.id).delete()
#         for r in data.get('localReferences', []):
#             db.add(LocalReference(worker_id=db_worker.id, **r))
#         # Previous Employers
#         db.query(PreviousEmployer).filter(PreviousEmployer.worker_id == db_worker.id).delete()
#         for e in data.get('previousEmployers', []):
#             db.add(PreviousEmployer(worker_id=db_worker.id, **e))
#         # Education
#         db.query(Education).filter(Education.worker_id == db_worker.id).delete()
#         for edu in data.get('education', []):
#             db.add(Education(worker_id=db_worker.id, **edu))
#         # Bank Details
#         db.query(BankDetails).filter(BankDetails.worker_id == db_worker.id).delete()
#         if data.get('bankDetails'):
#             db.add(BankDetails(worker_id=db_worker.id, **data['bankDetails']))
#         # Police Verification
#         db.query(PoliceVerification).filter(PoliceVerification.worker_id == db_worker.id).delete()
#         if data.get('policeVerification'):
#             db.add(PoliceVerification(worker_id=db_worker.id, **data['policeVerification']))
#         db.commit()
#         return {"status": "success", "worker_id": db_worker.id}
#     except Exception as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail=str(e))


# @router.put("/update-worker/{worker_id}", response_model=dict)
# async def update_worker(
#     worker_id: int,
#     worker: WorkerRegisterRequest,
#     db: Session = Depends(get_db)
# ):
#     db_worker = db.query(Worker).filter(Worker.id == worker_id).first()
#     if not db_worker:
#         raise HTTPException(status_code=404, detail="Worker not found")

#     try:
#         data = worker.model_dump(by_alias=True, exclude_unset=True)

#         work_exp = data.get('workExperience', {})
#         db_worker.full_name = data.get('fullName', db_worker.full_name)
#         db_worker.gender = data.get('gender', db_worker.gender)
#         db_worker.age = data.get('age', db_worker.age)
#         db_worker.dob = data.get('dob', db_worker.dob)
#         db_worker.phone = data.get('phone', db_worker.phone)
#         db_worker.alternate_phone = data.get('alternateMobile', db_worker.alternate_phone)
#         db_worker.email = data.get('email', db_worker.email)
#         db_worker.city = data.get('city', db_worker.city)
#         db_worker.blood_group = data.get('bloodGroup', db_worker.blood_group)

#         # Handle primaryServiceCategory
#         psc = data.get('primaryServiceCategory')
#         if psc:
#             db_worker.primary_service_category = [psc] if isinstance(psc, str) else psc

#         db_worker.experience_years = work_exp.get('years', db_worker.experience_years)
#         db_worker.experience_months = work_exp.get('months', db_worker.experience_months)
#         db_worker.languages_spoken = data.get('languagesSpoken', db_worker.languages_spoken)
#         db_worker.availability = data.get('availability', db_worker.availability)
#         db_worker.aadhar_number = data.get('aadharNumber', db_worker.aadhar_number)
#         db_worker.pan_number = data.get('panNumber', db_worker.pan_number)
#         db_worker.profile_photo_url = data.get('profilePhotoUrl', db_worker.profile_photo_url)
#         db_worker.electricity_bill_url = data.get('electricityBillUrl', db_worker.electricity_bill_url)
#         db_worker.status = data.get('status', db_worker.status)
#         db_worker.religion = data.get('religion', db_worker.religion)
#         db_worker.bio = data.get('bio', db_worker.bio)

#         # Nested/related data
#         # if data.get('addresses'):
#         #     db.query(Address).filter(Address.worker_id == db_worker.id).delete()
#         #     for i, addr in enumerate(data['addresses']):
#         #         db.add(Address(worker_id=db_worker.id, type='permanent' if i == 0 else 'current', **addr))

#         if data.get('addresses'):
#             db.query(Address).filter(Address.worker_id == db_worker.id).delete()
#             for i, addr in enumerate(worker.addresses):  # not data['addresses']
#                 db.add(Address(
#                     worker_id=db_worker.id,
#                     type='permanent' if i == 0 else 'current',
#                     **addr.model_dump(by_alias=False)
#                 ))

#         if data.get('emergencyContacts'):
#             db.query(EmergencyContact).filter(EmergencyContact.worker_id == db_worker.id).delete()
#             for ec in data['emergencyContacts']:
#                 db.add(EmergencyContact(worker_id=db_worker.id, **ec))

#         if data.get('localReferences'):
#             db.query(LocalReference).filter(LocalReference.worker_id == db_worker.id).delete()
#             for ref in data['localReferences']:
#                 db.add(LocalReference(worker_id=db_worker.id, **ref))

#         # if data.get('previousEmployer'):
#         #     db.query(PreviousEmployer).filter(PreviousEmployer.worker_id == db_worker.id).delete()
#         #     for emp in data['previousEmployer']:
#         #         db.add(PreviousEmployer(worker_id=db_worker.id, **emp))

#         for e in worker.employers:
#             db.add(PreviousEmployer(worker_id=db_worker.id, **e.model_dump(by_alias=False)))


#         # if data.get('education'):
#         #     db.query(Education).filter(Education.worker_id == db_worker.id).delete()
#         #     for edu in data['education']:
#         #         db.add(Education(worker_id=db_worker.id, **edu))

#         if worker.education:
#             db.query(Education).filter(Education.worker_id == db_worker.id).delete()
#             for edu in worker.education:
#                 db.add(Education(worker_id=db_worker.id, **edu.model_dump(by_alias=False)))


#         # if data.get('bankDetails'):
#         #     db.query(BankDetails).filter(BankDetails.worker_id == db_worker.id).delete()
#         #     db.add(BankDetails(worker_id=db_worker.id, **data['bankDetails']))

#         if worker.bank_details:
#             db.query(BankDetails).filter(BankDetails.worker_id == db_worker.id).delete()
#             db.add(BankDetails(worker_id=db_worker.id, **worker.bank_details.model_dump(by_alias=False)))


#         # if data.get('policeVerification'):
#         #     db.query(PoliceVerification).filter(PoliceVerification.worker_id == db_worker.id).delete()
#         #     db.add(PoliceVerification(worker_id=db_worker.id, **data['policeVerification']))

#         if worker.police_verification:
#             db.query(PoliceVerification).filter(PoliceVerification.worker_id == db_worker.id).delete()
#             db.add(PoliceVerification(
#                 worker_id=db_worker.id,
#                 **worker.police_verification.model_dump(by_alias=False)
#             ))


#         db.commit()
#         return {"status": "success", "worker_id": db_worker.id}

#     except Exception as e:
#         db.rollback()
#         raise HTTPException(status_code=500, detail=str(e))

@router.put("/update-worker/{worker_id}", response_model=dict)
async def update_worker(
    worker_id: int,
    worker: WorkerRegisterRequest,
    db: Session = Depends(get_db)
):
    db_worker = db.query(Worker).filter(Worker.id == worker_id).first()
    if not db_worker:
        raise HTTPException(status_code=404, detail="Worker not found")

    try:
        data = worker.model_dump(by_alias=True, exclude_unset=True)

        def should_update(value):
            return value not in (None, "", "string")

        # Update primitive fields conditionally
        if should_update(data.get('fullName')):
            db_worker.full_name = data['fullName']
        if should_update(data.get('gender')):
            db_worker.gender = data['gender']
        if should_update(data.get('age')):
            db_worker.age = data['age']
        if should_update(data.get('dob')):
            db_worker.dob = data['dob']
        if should_update(data.get('phone')):
            db_worker.phone = data['phone']
        if should_update(data.get('alternateMobile')):
            db_worker.alternate_phone = data['alternateMobile']
        if should_update(data.get('email')):
            db_worker.email = data['email']
        if should_update(data.get('city')):
            db_worker.city = data['city']
        if should_update(data.get('bloodGroup')):
            db_worker.blood_group = data['bloodGroup']
        if should_update(data.get('profilePhotoUrl')):
            db_worker.profile_photo_url = data['profilePhotoUrl']
        if should_update(data.get('electricityBillUrl')):
            db_worker.electricity_bill_url = data['electricityBillUrl']
        if should_update(data.get('status')):
            db_worker.status = data['status']
        if should_update(data.get('religion')):
            db_worker.religion = data['religion']
        if should_update(data.get('bio')):
            db_worker.bio = data['bio']
        if should_update(data.get('aadharNumber')):
            db_worker.aadhar_number = data['aadharNumber']
        if should_update(data.get('panNumber')):
            db_worker.pan_number = data['panNumber']

        # Handle primary service category
        psc = data.get('primaryServiceCategory')
        if should_update(psc):
            db_worker.primary_service_category = [psc] if isinstance(psc, str) else psc

        # Work experience
        work_exp = data.get('workExperience', {})
        if should_update(work_exp.get('years')):
            db_worker.experience_years = work_exp['years']
        if should_update(work_exp.get('months')):
            db_worker.experience_months = work_exp['months']

        # List fields
        if should_update(data.get('languagesSpoken')):
            db_worker.languages_spoken = data['languagesSpoken']
        if should_update(data.get('availability')):
            db_worker.availability = data['availability']

        # Addresses (full replace)
        if worker.addresses:
            db.query(Address).filter(Address.worker_id == db_worker.id).delete()
            for i, addr in enumerate(worker.addresses):
                db.add(Address(
                    worker_id=db_worker.id,
                    type='permanent' if i == 0 else 'current',
                    **addr.model_dump(by_alias=False)
                ))

        # Emergency Contacts
        if worker.emergency_contacts:
            db.query(EmergencyContact).filter(EmergencyContact.worker_id == db_worker.id).delete()
            for ec in worker.emergency_contacts:
                db.add(EmergencyContact(worker_id=db_worker.id, **ec.model_dump(by_alias=False)))

        # Local References
        if worker.references:
            db.query(LocalReference).filter(LocalReference.worker_id == db_worker.id).delete()
            for ref in worker.references:
                db.add(LocalReference(worker_id=db_worker.id, **ref.model_dump(by_alias=False)))

        # Previous Employers
        if worker.employers:
            db.query(PreviousEmployer).filter(PreviousEmployer.worker_id == db_worker.id).delete()
            for emp in worker.employers:
                db.add(PreviousEmployer(worker_id=db_worker.id, **emp.model_dump(by_alias=False)))

        # Education
        if worker.education:
            db.query(Education).filter(Education.worker_id == db_worker.id).delete()
            for edu in worker.education:
                db.add(Education(worker_id=db_worker.id, **edu.model_dump(by_alias=False)))

        # Bank Details
        if worker.bank_details:
            db.query(BankDetails).filter(BankDetails.worker_id == db_worker.id).delete()
            db.add(BankDetails(worker_id=db_worker.id, **worker.bank_details.model_dump(by_alias=False)))

        # Police Verification
        if worker.police_verification:
            db.query(PoliceVerification).filter(PoliceVerification.worker_id == db_worker.id).delete()
            db.add(PoliceVerification(
                worker_id=db_worker.id,
                **worker.police_verification.model_dump(by_alias=False)
            ))

        db.commit()
        return {"status": "success", "worker_id": db_worker.id}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))



@router.delete("/delete-worker/{worker_id}")
def delete_worker(worker_id: int = Path(...), db: Session = Depends(get_db)):
    try:
        db_worker = db.query(Worker).filter(Worker.id == worker_id).first()
        if not db_worker:
            raise HTTPException(status_code=404, detail="Worker not found")
        db.delete(db_worker)
        db.commit()
        return {"status": "success", "message": f"Worker {worker_id} deleted"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    


@router.post("/add-worker-documents")
async def add_worker_documents(
    worker_id: int = Form(..., description="ID of the worker to add documents for"),
    profile_photo: UploadFile = File(None),

    electricity_bill: UploadFile = File(None),
    live_capture: UploadFile = File(None),
    photoshoot: UploadFile = File(None),
    police_document: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    db_worker = db.query(Worker).filter(Worker.id == worker_id).first()
    if not db_worker:
        raise HTTPException(status_code=404, detail="Worker not found")
    
    # def save_file(upload: UploadFile, folder: str) -> str:
    #     if upload is None:
    #         return ''
    #     safe_filename = upload.filename.replace(' ', '_') if upload.filename else f'file_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
    #     filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{safe_filename}"
    #     path = os.path.join(folder, filename)
    #     os.makedirs(folder, exist_ok=True)
    #     with open(path, "wb") as buffer:
    #         shutil.copyfileobj(upload.file, buffer)
    #     return f"/{folder}/{filename}"

    def save_file(image: UploadFile, folder: str, URL: str) -> str:
        if image is None:
            return ''
        
        # Clean the original filename and timestamp it
        safe_orig = re.sub(r'\s+', '_', image.filename)
        image_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{safe_orig}"
        
        # Construct path and save the file
        image_path = os.path.join(folder, image_filename)
        os.makedirs(folder, exist_ok=True)
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        
        # URL-safe encoding
        image_filename = quote(image_filename)
        public_url = f"/{folder.replace(os.sep, '/')}/{image_filename}"
        full_url = URL + public_url

        return full_url
    
    if profile_photo is not None:
        setattr(db_worker, "profile_photo_url", save_file(profile_photo, PHOTOS_DIR) or '')
    if electricity_bill is not None:
        setattr(db_worker, "electricity_bill_url", save_file(electricity_bill, DOCS_DIR) or '')
    if live_capture is not None:
        setattr(db_worker, "live_capture_url", save_file(live_capture, LIVE_CAPTURE_DIR) or '')
    if photoshoot is not None:
        setattr(db_worker, "photoshoot_url", save_file(photoshoot, PHOTOSHOOT_DIR) or '')
    if police_document is not None:
        # Update police verification document_url
        pv = db.query(PoliceVerification).filter(PoliceVerification.worker_id == worker_id).first()
        if pv:
            setattr(pv, "document_url", save_file(police_document, DOCS_DIR) or '')
        else:
            db.add(PoliceVerification(worker_id=worker_id, document_url=save_file(police_document, DOCS_DIR) or ''))
    db.commit()
    return {"status": "success", "message": "Documents added for worker", "worker_id": worker_id}

# @router.put("/update-worker-documents")
# async def update_worker_documents(
#     worker_id: int = Form(..., description="ID of the worker to update documents for"),
#     profile_photo: UploadFile = File(None),
#     electricity_bill: UploadFile = File(None),
#     live_capture: UploadFile = File(None),
#     photoshoot: UploadFile = File(None),
#     police_document: UploadFile = File(None),
#     db: Session = Depends(get_db)
# ):
#     db_worker = db.query(Worker).filter(Worker.id == worker_id).first()
#     if not db_worker:
#         raise HTTPException(status_code=404, detail="Worker not found")
    
#     # def save_file(upload: UploadFile, folder: str) -> str:
#     #     if upload is None:
#     #         return ''
#     #     safe_filename = upload.filename.replace(' ', '_') if upload.filename else f'file_{datetime.now().strftime("%Y%m%d_%H%M%S")}'
#     #     filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{safe_filename}"
#     #     path = os.path.join(folder, filename)
#     #     os.makedirs(folder, exist_ok=True)
#     #     with open(path, "wb") as buffer:
#     #         shutil.copyfileobj(upload.file, buffer)
#     #     return f"/{folder}/{filename}"

#     def save_file(image: UploadFile, folder: str, URL: str) -> str:
#         if image is None:
#             return ''
        
#         # Clean the original filename and timestamp it
#         safe_orig = re.sub(r'\s+', '_', image.filename)
#         image_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{safe_orig}"
        
#         # Construct path and save the file
#         image_path = os.path.join(folder, image_filename)
#         os.makedirs(folder, exist_ok=True)
#         with open(image_path, "wb") as buffer:
#             shutil.copyfileobj(image.file, buffer)
        
#         # URL-safe encoding
#         image_filename = quote(image_filename)
#         public_url = f"/{folder.replace(os.sep, '/')}/{image_filename}"
#         full_url = URL + public_url

#         return full_url
    
#     if profile_photo is not None:
#         setattr(db_worker, "profile_photo_url", save_file(profile_photo, PHOTOS_DIR) or '')
#     if electricity_bill is not None:
#         setattr(db_worker, "electricity_bill_url", save_file(electricity_bill, DOCS_DIR) or '')
#     if live_capture is not None:
#         setattr(db_worker, "live_capture_url", save_file(live_capture, LIVE_CAPTURE_DIR) or '')
#     if photoshoot is not None:
#         setattr(db_worker, "photoshoot_url", save_file(photoshoot, PHOTOSHOOT_DIR) or '')
#     if police_document is not None:
#         pv = db.query(PoliceVerification).filter(PoliceVerification.worker_id == worker_id).first()
#         if pv:
#             setattr(pv, "document_url", save_file(police_document, DOCS_DIR) or '')
#         else:
#             db.add(PoliceVerification(worker_id=worker_id, document_url=save_file(police_document, DOCS_DIR) or ''))
#     db.commit()
#     return {"status": "success", "message": "Documents updated for worker", "worker_id": worker_id}


@router.put("/update-worker-documents")
async def update_worker_documents(
    worker_id: int = Form(..., description="ID of the worker to update documents for"),
    profile_photo: UploadFile = File(None),
    electricity_bill: UploadFile = File(None),
    live_capture: UploadFile = File(None),
    photoshoot: UploadFile = File(None),
    police_document: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    db_worker = db.query(Worker).filter(Worker.id == worker_id).first()
    if not db_worker:
        raise HTTPException(status_code=404, detail="Worker not found")

    def save_file(image: UploadFile, folder: str, URL: str) -> str:
        if image is None:
            return ''
        safe_orig = re.sub(r'\s+', '_', image.filename)
        image_filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{safe_orig}"
        image_path = os.path.join(folder, image_filename)
        os.makedirs(folder, exist_ok=True)
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)
        image_filename = quote(image_filename)
        public_url = f"/{folder.replace(os.sep, '/')}/{image_filename}"
        return URL + public_url

    # Upload and retain logic
    if profile_photo is not None:
        db_worker.profile_photo_url = save_file(profile_photo, PHOTOS_DIR, URL)
    if electricity_bill is not None:
        db_worker.electricity_bill_url = save_file(electricity_bill, DOCS_DIR, URL)
    if live_capture is not None:
        db_worker.live_capture_url = save_file(live_capture, LIVE_CAPTURE_DIR, URL)
    if photoshoot is not None:
        db_worker.photoshoot_url = save_file(photoshoot, PHOTOSHOOT_DIR, URL)

    if police_document is not None:
        doc_url = save_file(police_document, DOCS_DIR, URL)
        existing_pv = db.query(PoliceVerification).filter(PoliceVerification.worker_id == worker_id).first()
        if existing_pv:
            existing_pv.document_url = doc_url
        else:
            db.add(PoliceVerification(
                worker_id=worker_id,
                document_url=doc_url,
                status="pending",
                verification_date=datetime.now().strftime('%Y-%m-%d'),
                remarks=""
            ))

    db.commit()
    return {
        "status": "success",
        "message": "Documents updated for worker",
        "worker_id": worker_id
    }

from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'super_admin'
    
class IsHospitalAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'hospital_admin'
    
class IsDoctor(BasePermission):
    def has_permission(self, request, view):
        return request.user.role in['doctor', 'consultant']
    
class IsNurse(BasePermission):
    def has_permission(self, request, view):
       return request.user.role == 'nurse'

class IsPharmacist(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'pharmacist'

class IsLabTech(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'Lab_tech'

class IsRadiologist(BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'radiologist'

class IsHospitalStaff(BasePermission):
    def has_permission(self, request, view):
        return request.user.role in[
            'super_admin',
            'hospital_admin',
            'doctor',
            'consultant',
            'nurse',
            'lab_tech',
            'radiologist',
            'pharmacist',
            'receptionist',
        ] 
    
class IsSameHospital(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'super_admin':
            return True
        if hasattr(obj, 'hospital'):
            return obj.hospital == request.user.hospital
        if hasattr(obj, 'visit'):
            return obj.visit.hospital == request.user.hospital
        return False
    
class ReadOnlyForNonDoctors(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.role in['doctor', 'consultant']
    
class ConsentRequiredPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'super_admin':
            return True
        if obj.visit.hospital == request.user.hospital:
            return True
        from consent.models import AccessConsent

        return AccessConsent.objects.filter(
            patient=obj.visit.patient,
            requesting_hospital=request.user.hospital,
            is_verified=True
        ).exists()
    
class IsOwnerDoctor(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'super_admin':
            return True
        
        return obj.doctor.doctor_profile == request.user
    
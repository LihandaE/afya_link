from rest_framework.permissions import BasePermission, SAFE_METHODS


class RolePermission(BasePermission):
    """
    Base permission to check user roles safely.
    Prevents errors when request.user is AnonymousUser.
    """
    allowed_roles = []

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return getattr(request.user, "role", None) in self.allowed_roles


class IsSuperAdmin(RolePermission):
    allowed_roles = ["super_admin"]


class IsHospitalAdmin(RolePermission):
    allowed_roles = ["hospital_admin"]


class IsReceptionist(RolePermission):
    allowed_roles = ["receptionist"]


class IsDoctor(RolePermission):
    allowed_roles = ["doctor", "consultant"]


class IsNurse(RolePermission):
    allowed_roles = ["nurse"]


class IsPharmacist(RolePermission):
    allowed_roles = ["pharmacist"]


class IsLabTech(RolePermission):
    allowed_roles = ["lab_tech"]


class IsRadiologist(RolePermission):
    allowed_roles = ["radiologist"]


class IsHospitalStaff(RolePermission):
    allowed_roles = [
        "super_admin",
        "hospital_admin",
        "doctor",
        "consultant",
        "nurse",
        "lab_tech",
        "radiologist",
        "pharmacist",
        "receptionist",
    ]


class IsSameHospital(BasePermission):
    """
    Ensures the user belongs to the same hospital as the object.
    """

    def has_object_permission(self, request, view, obj):

        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.role == "super_admin":
            return True

        if hasattr(obj, "hospital"):
            return obj.hospital == request.user.hospital

        if hasattr(obj, "visit"):
            return obj.visit.hospital == request.user.hospital

        return False


class ReadOnlyForNonDoctors(BasePermission):
    """
    Only doctors/consultants can modify records.
    Others can only read.
    """

    def has_permission(self, request, view):

        if request.method in SAFE_METHODS:
            return True

        if not request.user or not request.user.is_authenticated:
            return False

        return request.user.role in ["doctor", "consultant"]


class ConsentRequiredPermission(BasePermission):
    """
    Allows access if:
    - Super admin
    - Same hospital
    - Verified patient consent exists
    """

    def has_object_permission(self, request, view, obj):

        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.role == "super_admin":
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
    """
    Only the doctor who created the record can modify it.
    """

    def has_object_permission(self, request, view, obj):

        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.role == "super_admin":
            return True

        return obj.doctor.doctor_profile == request.user
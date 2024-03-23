"""
Enums for Currency and Channels with predefined values.
"""

from enum import Enum


class AccountType(Enum):
    """Customer’s type of Account."""

    PERSONAL = "personal"
    BUSINESS = "business"


class Currency(Enum):
    """Currencies supported by Paystack."""

    # GHS = "GHS"
    # KES = "KES"
    NGN = "NGN"
    USD = "USD"
    # ZAR = "ZAR"


class PaymentMethods(Enum):
    """Channels supported by Paystack."""

    ACCOUNT_TRANSFER = "ACCOUNT_TRANSFER"
    CARD = "CARD"
    DIRECT_DEBIT = "DIRECT_DEBIT"
    PHONE_NUMBER = "PHONE_NUMBER"
    USSD = "USSD"


class DocumentType(Enum):
    """Customer’s mode of identity."""

    IDENTITY_NUMBER = "identityNumber"
    PASSPORT_NUMBER = "passportNumber"
    BUSINESS_REG_NUMBER = "businessRegistrationNumber"


class EventType(Enum):
    INVOICE = "invoice"
    TRANSACTION = "transaction"


class Interval(Enum):
    """Interval supported by Paystack."""

    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    BIANNUALLY = "biannually"
    ANNUALLY = "annually"


class MobileMoney(Enum):
    """Mobile Money supported by Paystack.
    Only available to businesses in Ghana and Kenya.
    """

    MTN = "mtn"
    AIRTEL_TIGO = "atl"
    VODAFONE = "vod"
    M_PESA = "mpesa"


class PWT(Enum):
    """PWT supported by Paystack."""

    ACCOUNT_EXPIRES_AT = "account_expires_at"


class QRCODE(Enum):
    """QR Codes supported by Paystack."""

    SCAN_TO_PAY = "scan-to-pay"
    VISA = "visa"


class RecipientType(Enum):
    BASE = "base"
    GHIPSS = "ghipss"
    MOBILE_MONEY = "mobile_money"
    NUBAN = "nuban"


class ResendOTP(Enum):
    RESEND_OTP = "resend_otp"
    TRANSFER = "transfer"


class Resolution(Enum):
    MERCHANT = ("merchant-accepted",)
    DECLINED = "declined"


class RiskAction(Enum):
    """Risk Action supported by Paystack."""

    ALLOW = "allow"
    DEFAULT = "default"
    DENY = "deny"


class SplitType(Enum):
    PERCENTAGE = "percentage"
    FLAT = "flat"


class STATUS(Enum):
    """Status supported by Paystack."""

    SUCCESS = "success"
    FAILED = "failed"
    PENDING = "pending"


class USSD(Enum):
    """USSD supported by Paystack."""

    GUARANTY_BANK = "737"
    UNITED_BANK_OF_AFRICA = "919"
    STERLING_BANK = "822"
    ZENITH_BANK = "966"

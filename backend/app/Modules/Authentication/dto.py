from dataclasses import dataclass
from typing import Optional


# ---------------- REGISTER ----------------
@dataclass
class RegisterDTO:
    name: str
    email: str
    password: str
    accept_terms: bool
    accept_popia: bool
    marketing_consent: bool = False


# ---------------- LOGIN ----------------
@dataclass
class LoginDTO:
    email: str
    password: str


# ---------------- VERIFY EMAIL ----------------
@dataclass
class VerifyEmailDTO:
    token: str


# ---------------- FORGOT PASSWORD ----------------
@dataclass
class ForgotPasswordDTO:
    email: str


# ---------------- RESET PASSWORD ----------------
@dataclass
class ResetPasswordDTO:
    token: str
    password: str
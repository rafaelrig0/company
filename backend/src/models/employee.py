import enum
from decimal import Decimal
from ..lib.database import Base
from sqlalchemy.orm import validates, Mapped, mapped_column, relationship
from sqlalchemy import Integer, DECIMAL, String, Enum, ForeignKey

class Role(enum.IntEnum):
    EMPLOYEE = 1
    LEADER = 2
    DIRECTOR = 3

class Employee(Base):
    __tablename__ = "employee"

    employee_id: Mapped[int] = mapped_column(Integer, primary_key=True, nullable=False)
    fullname: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    @validates("email")
    def validate_email(self, key, value):
        if "@" not in value or "." not in value.split("@")[-1]:
            raise ValueError("Invalid email!")
        return value
    
    phones: Mapped[list["Phones"]] = relationship(
        back_populates="employee", cascade="all, delete-orphan"
    )

    manager_id: Mapped[int | None] = mapped_column(
        ForeignKey("employee.employee_id", ondelete="SET NULL"), nullable=True
    )
    manager: Mapped["Employee | None "] = relationship(
        back_populates="subordinates", remote_side=[employee_id]
    )
    subordinates: Mapped[list["Employee"]] = relationship(
        back_populates="manager"
    )
    role: Mapped[Role] = mapped_column(
        Enum(Role, name="role"), nullable=False, default=Role.EMPLOYEE
    )
    password_hash: Mapped[str] = mapped_column(String(150), nullable=False)

    salary: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)

    department: Mapped[str] = mapped_column(String(100), nullable=False)
    
class Phones(Base):
    __tablename__ = "phones"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    phone_number: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)

    employee_id: Mapped[int] = mapped_column(ForeignKey("employee.employee_id", ondelete="CASCADE"), nullable=False)

    employee: Mapped["Employee"] = relationship(back_populates="phones")
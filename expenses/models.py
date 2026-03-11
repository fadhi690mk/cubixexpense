from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.contrib.auth import get_user_model

User = get_user_model()


# -----------------------
# Base Soft Delete Model
# -----------------------
class SoftDeleteModel(models.Model):
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# -----------------------
# Contributor Model
# -----------------------
class Contributor(SoftDeleteModel):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


# -----------------------
# Fund Model
# -----------------------
class Fund(SoftDeleteModel):
    contributor = models.ForeignKey(
        Contributor,
        on_delete=models.PROTECT,
        related_name="funds"
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    date = models.DateField(default=timezone.now)
    description = models.TextField(blank=True)

    added_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="funds_added"
    )

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.contributor.name} - {self.amount}"


# -----------------------
# Expense Category
# -----------------------
class ExpenseCategory(SoftDeleteModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


# -----------------------
# Expense Model
# -----------------------
class Expense(SoftDeleteModel):
    category = models.ForeignKey(
        ExpenseCategory,
        on_delete=models.PROTECT,
        related_name="expenses"
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    date = models.DateField(default=timezone.now)
    description = models.TextField(blank=True)

    paid_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="expenses_paid"
    )

    def __str__(self):
        return f"{self.category} - {self.amount}"


# -----------------------
# Expense Documents
# -----------------------
class ExpenseDocument(SoftDeleteModel):
    expense = models.ForeignKey(
        Expense,
        on_delete=models.CASCADE,
        related_name="documents"
    )
    file = models.FileField(upload_to="expense_documents/")
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return f"Document for Expense #{self.expense_id}"


# -----------------------
# User Activity Log (Immutable)
# -----------------------
class ActivityLog(models.Model):
    ACTION_CHOICES = (
        ("CREATE", "Create"),
        ("UPDATE", "Update"),
        ("DELETE", "Delete"),
        ("LOGIN", "Login"),
        ("LOGOUT", "Logout"),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=100)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.user} - {self.action} - {self.model_name}"


# -----------------------
# Todo Model (Planned Expenses)
# -----------------------
class Todo(SoftDeleteModel):
    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("COMPLETED", "Completed"),
        ("CANCELLED", "Cancelled"),
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.ForeignKey(
        ExpenseCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="todos"
    )
    estimated_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
        null=True,
        blank=True
    )
    target_date = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="todos_created"
    )

    class Meta:
        ordering = ["-target_date"]

    def __str__(self):
        return self.title

    def is_overdue(self):
        """Check if todo is overdue"""
        from django.utils import timezone
        return self.status == "PENDING" and self.target_date < timezone.now().date()

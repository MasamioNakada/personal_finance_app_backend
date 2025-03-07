from django.contrib.auth.models import User
from django.db import models

CURRENCY_CHOICES = [
    ('PEN', 'Peruvian Sol'),
    ('USD', 'US Dollar'),
    ('EUR', 'Euro'),
]

# Modelo de Presupuestos
class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    month = models.CharField(max_length=7)  # YYYY-MM
    total_budget = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='PEN')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Presupuesto {self.month} - {self.user.username}"

# Presupuesto asignado por categoría
class Category(models.Model):
    CATEGORY_TYPES = [('income', 'Ingreso'), ('expense', 'Gasto')]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="categories")
    name = models.CharField(max_length=255)
    category_type = models.CharField(max_length=10, choices=CATEGORY_TYPES)
    
    class Meta:
        unique_together = ('user', 'name', 'category_type')

    def __str__(self):
        return f"{self.name} ({self.get_category_type_display()}) - {self.user.username}"

# Etiquetas para transacciones
class Tag(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tags")
    name = models.CharField(max_length=255)
    
    class Meta:
        unique_together = ('user', 'name')
    
    def __str__(self):
        return f"{self.name} - {self.user.username}"


# Transacciones con etiquetas
class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="transactions")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='PEN')
    description = models.TextField()
    transaction_date = models.DateTimeField()
    TRANSACTION_TYPES = [('income', 'Ingreso'), ('expense', 'Gasto')]
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    tags = models.ManyToManyField(Tag, blank=True, related_name="transactions")

    def __str__(self):
        return f"{self.transaction_type} - {self.amount} ({self.category.name})"

# Metas financieras
class FinancialGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    goal_name = models.CharField(max_length=255)
    target_amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, choices=CURRENCY_CHOICES, default='PEN')
    deadline = models.DateField()
    STATUS_CHOICES = [('pending', 'Pendiente'), ('completed', 'Completado')]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.goal_name} - {self.target_amount} {self.currency} - {self.status}"

# Historial de cambios
class ChangeLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    entity_type = models.CharField(max_length=50)  # Ej: "budget", "transaction"
    entity_id = models.PositiveIntegerField()  # ID del objeto afectado
    field_changed = models.CharField(max_length=255)
    old_value = models.TextField(null=True, blank=True)
    new_value = models.TextField(null=True, blank=True)
    changed_at = models.DateTimeField(auto_now_add=True)
    changed_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="changes_made")

    def __str__(self):
        return f"Change in {self.entity_type} ({self.entity_id}) by {self.changed_by.username}"
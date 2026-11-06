from django.db import models

class LostItem(models.Model):
    student_name = models.CharField(max_length=100)
    item_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    # Priority: 1 = High, 2 = Medium, 3 = Low
    priority = models.IntegerField(default=2)
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "lost_items"

    def __str__(self):
        return f"[Lost] {self.item_name} - {self.student_name}"

class FoundItem(models.Model):
    student_name = models.CharField(max_length=100)
    item_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    # Priority: 1 = High, 2 = Medium, 3 = Low
    priority = models.IntegerField(default=2)
    is_resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "found_items"

    def __str__(self):
        return f"[Found] {self.item_name} - {self.student_name}"

class ActivityLog(models.Model):
    action_type = models.CharField(max_length=20)
    category = models.CharField(max_length=10, default="Lost")  # 'Lost' or 'Found'
    item_id = models.IntegerField()
    description = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "activity_logs"

    def __str__(self):
        return self.description

class ClaimProcessing(models.Model):
    student_name = models.CharField(max_length=100)
    item_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    # Priority: 1 = High, 2 = Medium, 3 = Low
    priority = models.IntegerField(default=2)
    lost_item = models.ForeignKey(LostItem, on_delete=models.CASCADE, null=True, blank=True, related_name="processing_claims")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "claim_processing"

    def __str__(self):
        return f"[Processing] {self.item_name} - {self.student_name}"

class ClaimDone(models.Model):
    student_name = models.CharField(max_length=100)
    item_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    priority = models.IntegerField(default=2)
    lost_item = models.ForeignKey(LostItem, on_delete=models.SET_NULL, null=True, blank=True, related_name="done_claims")
    claimed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "claim_done"

    def __str__(self):
        return f"[Claim Done] {self.item_name} - {self.student_name}"

import heapq
from django.shortcuts import render, redirect
from django.db import connection, models
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import LostItem, FoundItem, ActivityLog, ClaimProcessing, ClaimDone

# Stack implementation for Activity History & Undo
class Stack:
    def __init__(self):
        self.items = []
    def push(self, item):
        self.items.append(item)
    def pop(self):
        return self.items.pop() if self.items else None
    def is_empty(self):
        return len(self.items) == 0


def login_view(request):
    """Simple, neat login & registration view for Students, Faculty, and Admin"""
    if request.user.is_authenticated:
        return redirect("claim_scheduler")

    error_message = None
    active_tab = "login"

    if request.method == "POST":
        mode = request.POST.get("mode", "login").strip().lower()

        # --- REGISTRATION FLOW FOR NEW USERS & FACULTY ---
        if mode == "register":
            active_tab = "register"
            reg_username = request.POST.get("reg_username", "").strip()
            reg_password = request.POST.get("reg_password", "").strip()
            reg_confirm_password = request.POST.get("reg_confirm_password", "").strip()
            reg_role = request.POST.get("reg_role", "user").strip().lower()

            if not reg_username or not reg_password:
                error_message = "Please enter both username and password."
                return render(request, "login.html", {"error": error_message, "active_tab": active_tab})

            if reg_password != reg_confirm_password:
                error_message = "Passwords do not match. Please verify your password."
                return render(request, "login.html", {"error": error_message, "active_tab": active_tab})

            if User.objects.filter(username__iexact=reg_username).exists():
                error_message = f"Username '{reg_username}' is already registered. Please login instead."
                return render(request, "login.html", {"error": error_message, "active_tab": active_tab})

            # Create standard account (staff/admin cannot be registered through public form)
            new_user = User.objects.create_user(username=reg_username, password=reg_password)
            new_user.is_staff = False
            new_user.is_superuser = False
            new_user.save()

            if reg_role == "faculty":
                request.session["user_role"] = "Faculty"
            else:
                request.session["user_role"] = "Student"

            authenticated_user = authenticate(request, username=reg_username, password=reg_password)
            if authenticated_user:
                login(request, authenticated_user)
                return redirect("claim_scheduler")
            else:
                return redirect("login")

        # --- SIGN IN FLOW ---
        else:
            active_tab = "login"
            username = request.POST.get("username", "").strip()
            password = request.POST.get("password", "").strip()
            role = request.POST.get("role", "").strip().lower()

            if not username or not password:
                error_message = "Please enter both username and password."
                return render(request, "login.html", {"error": error_message, "active_tab": active_tab})

            is_admin_req = (role == "admin") or (username.lower() == "admin")
            is_faculty_req = (role == "faculty") or ("faculty" in username.lower())

            if is_admin_req:
                admin_obj = User.objects.filter(username__iexact=username).first()
                if not admin_obj:
                    admin_obj = User.objects.create_superuser(username=username, email="admin@campus.edu", password=password)
                else:
                    admin_obj.is_staff = True
                    admin_obj.is_superuser = True
                    admin_obj.set_password(password)
                    admin_obj.save()
                user = authenticate(request, username=admin_obj.username, password=password)
                if user:
                    request.session["user_role"] = "Admin"

            elif is_faculty_req:
                fac_obj = User.objects.filter(username__iexact=username).first()
                if not fac_obj:
                    fac_obj = User.objects.create_user(username=username, password=password)
                else:
                    fac_obj.is_staff = False
                    fac_obj.is_superuser = False
                    fac_obj.set_password(password)
                    fac_obj.save()
                user = authenticate(request, username=fac_obj.username, password=password)
                if user:
                    request.session["user_role"] = "Faculty"

            else:
                std_obj = User.objects.filter(username__iexact=username).first()
                if not std_obj:
                    std_obj = User.objects.create_user(username=username, password=password)
                else:
                    std_obj.is_staff = False
                    std_obj.is_superuser = False
                    std_obj.set_password(password)
                    std_obj.save()
                user = authenticate(request, username=std_obj.username, password=password)
                if user:
                    request.session["user_role"] = "Student"

            if user is not None:
                login(request, user)
                next_url = request.GET.get("next") or "claim_scheduler"
                return redirect(next_url)
            else:
                error_message = "Invalid username or password."

    return render(request, "login.html", {"error": error_message, "active_tab": active_tab})


def logout_view(request):
    """Logout view redirecting back to login page"""
    logout(request)
    return redirect("login")


@login_required(login_url="login")
def claim_scheduler_view(request):
    message = None
    is_admin = request.user.is_staff or request.user.is_superuser
    is_faculty = (request.session.get("user_role") == "Faculty") or ("faculty" in request.user.username.lower())

    if request.method == "POST":
        action = request.POST.get("action")

        # 1. Add Item to respective table (LostItem or FoundItem) - Accessible to all users
        if action == "add":
            category = request.POST.get("category", "Lost")
            student_name = request.POST.get("student_name")
            item_name = request.POST.get("item_name")
            location = request.POST.get("location", "Campus")
            priority = int(request.POST.get("priority", 2))

            if student_name and item_name:
                if category == "Lost":
                    item = LostItem.objects.create(
                        student_name=student_name,
                        item_name=item_name,
                        location=location,
                        priority=priority,
                    )
                    ClaimProcessing.objects.create(
                        student_name=student_name,
                        item_name=item_name,
                        location=location,
                        priority=priority,
                        lost_item=item,
                    )
                else:
                    item = FoundItem.objects.create(
                        student_name=student_name,
                        item_name=item_name,
                        location=location,
                        priority=priority,
                    )

                ActivityLog.objects.create(
                    action_type="ADD",
                    category=category,
                    item_id=item.id,
                    description=f"Added {category} Item: {item_name} ({student_name})",
                )
                message = f"Successfully registered {category} item: '{item_name}'."
            return redirect("claim_scheduler")

        # 2. Process Next Highest Priority Item from the Min-Heap - Admin Only
        elif action == "process_next":
            if not is_admin:
                message = "Access Denied: Only administrators have permission to process priority items."
            else:
                pq = []
                for item in LostItem.objects.filter(is_resolved=False):
                    heapq.heappush(pq, (item.priority, item.id, "Lost", item))
                for item in FoundItem.objects.filter(is_resolved=False):
                    heapq.heappush(pq, (item.priority, item.id, "Found", item))

                if pq:
                    _, _, cat, next_item = heapq.heappop(pq)
                    next_item.is_resolved = True
                    next_item.save()

                    if cat == "Lost":
                        ClaimProcessing.objects.filter(lost_item=next_item).delete()
                        ClaimDone.objects.create(
                            student_name=next_item.student_name,
                            item_name=next_item.item_name,
                            location=next_item.location,
                            priority=next_item.priority,
                            lost_item=next_item,
                        )

                    ActivityLog.objects.create(
                        action_type="PROCESS",
                        category=cat,
                        item_id=next_item.id,
                        description=f"Claim Done: {next_item.item_name} ({next_item.student_name})" if cat == "Lost" else f"Resolved Found Item: {next_item.item_name}",
                    )
                    message = f"Processed {cat} Item (Claim Done): {next_item.item_name} ({next_item.student_name})" if cat == "Lost" else f"Processed Found Item: {next_item.item_name} ({next_item.student_name})"
                else:
                    message = "No pending items to process!"

        # 3. Process Specific Item / Claim Directly - Admin Only
        elif action == "process_item":
            if not is_admin:
                message = "Access Denied: Only administrators have permission to process claims or handovers."
            else:
                item_id = request.POST.get("item_id")
                category = request.POST.get("category", "Lost")
                model_class = LostItem if category == "Lost" else FoundItem
                item = model_class.objects.filter(id=item_id, is_resolved=False).first()
                if not item and category == "Lost":
                    # Fallback: check if item_id matches ClaimProcessing
                    cp = ClaimProcessing.objects.filter(id=item_id).first()
                    if cp and cp.lost_item:
                        item = cp.lost_item

                if item:
                    item.is_resolved = True
                    item.save()

                    if category == "Lost":
                        ClaimProcessing.objects.filter(lost_item=item).delete()
                        ClaimDone.objects.create(
                            student_name=item.student_name,
                            item_name=item.item_name,
                            location=item.location,
                            priority=item.priority,
                            lost_item=item,
                        )

                    desc = (
                        f"Claim Done: {item.item_name} ({item.student_name})"
                        if category == "Lost"
                        else f"Resolved Found Item: {item.item_name}"
                    )
                    ActivityLog.objects.create(
                        action_type="PROCESS",
                        category=category,
                        item_id=item.id,
                        description=desc,
                    )
                    message = (
                        f"Claim Processed & Done: {item.item_name} ({item.student_name})"
                        if category == "Lost"
                        else f"Resolved Found Item: {item.item_name}"
                    )
                else:
                    message = "Item not found or already processed!"

        # 4. Undo Last Action (Stack LIFO) - Admin Only
        elif action == "undo":
            if not is_admin:
                message = "Access Denied: Only administrators have permission to undo actions."
            else:
                logs = list(ActivityLog.objects.order_by("id"))
                stack = Stack()
                for log in logs:
                    stack.push(log)

                last_action = stack.pop()
                if last_action:
                    model_class = LostItem if last_action.category == "Lost" else FoundItem
                    if last_action.action_type == "PROCESS":
                        obj = model_class.objects.filter(id=last_action.item_id).first()
                        if obj:
                            obj.is_resolved = False
                            obj.save()
                            if last_action.category == "Lost":
                                ClaimDone.objects.filter(lost_item=obj).delete()
                                ClaimProcessing.objects.get_or_create(
                                    lost_item=obj,
                                    defaults={
                                        "student_name": obj.student_name,
                                        "item_name": obj.item_name,
                                        "location": obj.location,
                                        "priority": obj.priority,
                                    },
                                )
                    elif last_action.action_type == "ADD":
                        if last_action.category == "Lost":
                            obj = LostItem.objects.filter(id=last_action.item_id).first()
                            if obj:
                                ClaimProcessing.objects.filter(lost_item=obj).delete()
                                obj.delete()
                        else:
                            FoundItem.objects.filter(id=last_action.item_id).delete()

                    last_action.delete()
                    message = f"Undo successful: {last_action.description}"
                else:
                    message = "Nothing to undo!"

    # Search Query Handling for Users (Search when & where a lost item was found)
    search_q = request.GET.get("q", "").strip()
    search_loc = request.GET.get("loc", "").strip()

    found_search_qs = FoundItem.objects.all().order_by("-created_at")
    if search_q:
        found_search_qs = found_search_qs.filter(
            models.Q(item_name__icontains=search_q) |
            models.Q(student_name__icontains=search_q)
        )
    if search_loc:
        found_search_qs = found_search_qs.filter(location__icontains=search_loc)

    search_performed = bool(search_q or search_loc)
    found_search_results = list(found_search_qs)

    # Distinct locations for search dropdown / quick filter
    unique_locations = (
        FoundItem.objects.values_list("location", flat=True)
        .distinct()
        .exclude(location__isnull=True)
        .exclude(location__exact="")
    )

    # 1. Lost Item Claim Processing Queue (Min-Heap Priority Queue from claim_processing table)
    lost_pq = []
    for claim in ClaimProcessing.objects.all():
        heapq.heappush(lost_pq, (claim.priority, claim.id, claim))
    lost_pending = []
    while lost_pq:
        _, _, claim = heapq.heappop(lost_pq)
        lost_pending.append(claim)

    # 2. Found Items Pending Queue (Min-Heap Priority Queue from found_items table)
    found_pq = []
    for item in FoundItem.objects.filter(is_resolved=False):
        heapq.heappush(found_pq, (item.priority, item.id, item))
    found_pending = []
    while found_pq:
        _, _, item = heapq.heappop(found_pq)
        found_pending.append(item)

    # 3. Combined pending items in Priority Queue order
    pq = []
    for claim in ClaimProcessing.objects.all():
        heapq.heappush(pq, (claim.priority, claim.id, "Lost", claim.lost_item if claim.lost_item else claim))
    for item in FoundItem.objects.filter(is_resolved=False):
        heapq.heappush(pq, (item.priority, item.id, "Found", item))

    scheduled_items = []
    while pq:
        _, _, cat, item = heapq.heappop(pq)
        scheduled_items.append({"category": cat, "item": item})

    # 4. Claim Done (Resolved from claim_done table)
    lost_resolved = ClaimDone.objects.order_by("-id")[:5]

    # 5. Resolved Found Items
    found_resolved = FoundItem.objects.filter(is_resolved=True).order_by("-id")[:5]

    # Recent resolved items from both tables
    resolved = []
    for cd in ClaimDone.objects.order_by("-id")[:3]:
        resolved.append({"category": "Lost", "item": cd})
    for item in FoundItem.objects.filter(is_resolved=True).order_by("-id")[:3]:
        resolved.append({"category": "Found", "item": item})

    activities = ActivityLog.objects.order_by("-id")[:6]
    db_name = connection.settings_dict.get("NAME", "data_structure")

    return render(request, "index.html", {
        "lost_pending": lost_pending,
        "found_pending": found_pending,
        "lost_resolved": lost_resolved,
        "found_resolved": found_resolved,
        "items": scheduled_items,
        "resolved_items": resolved,
        "activities": activities,
        "message": message,
        "db_info": f"MySQL Tables: lost_items, found_items, claim_processing, claim_done ({db_name})",
        "is_admin": is_admin,
        "is_faculty": is_faculty,
        "search_q": search_q,
        "search_loc": search_loc,
        "search_performed": search_performed,
        "found_search_results": found_search_results,
        "unique_locations": unique_locations,
    })

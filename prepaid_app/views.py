from django.shortcuts import render
from .models import Prepaid, TopUp, History
from django.contrib.auth.decorators import login_required
from .utils import generate_qr
from django.contrib.auth import login
from .forms import RegisterForm
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

@login_required
def dashboard(request):
    prepaid = Prepaid.objects.filter(user=request.user).first()

    # 🔥 HANDLE ERROR kalau prepaid belum ada
    if not prepaid:
        messages.error(request, "Data prepaid belum ada")
        return redirect('/login/')

    qr_image = generate_qr(prepaid.prepaid_no)

    return render(request, "prepaid_app/dashboard.html", {
        "data": prepaid,
        "qr_image": qr_image
    })

@login_required
def view_qr(request):
    prepaid = Prepaid.objects.filter(user=request.user).first()

    qr_image = generate_qr(prepaid.prepaid_no)

    return render(request, "prepaid_app/qr.html", {
        "qr_image": qr_image
    })

from django.contrib.auth.models import User

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('/register/')

        user = User.objects.create_user(username=username, password=password)

        # auto create prepaid
        Prepaid.objects.create(
            user=user,
            prepaid_no="1234567890",
            current_balance=0,
            expired_date="2030-01-01"
        )

        messages.success(request, "Register success! Please login")
        return redirect('/login/')

    return render(request, 'prepaid_app/register.html')

@csrf_exempt
@login_required
def topup(request):
    prepaid = Prepaid.objects.get(user=request.user)

    if request.method == 'POST':
        amount = int(request.POST.get('amount'))

        prepaid.current_balance += amount
        prepaid.save()

        # ✅ sekarang aman karena tabel sudah ada
        TopUp.objects.create(prepaid=prepaid, amount=amount)
        History.objects.create(prepaid=prepaid, action=f"Topup {amount}")

        # ✅ notif sukses
        messages.success(request, f"Top up berhasil +{amount}")

        return redirect('/')  # balik ke dashboard

    return render(request, 'prepaid_app/topup.html')

@login_required
def history(request):
    prepaid = Prepaid.objects.get(user=request.user)
    histories = History.objects.filter(prepaid=prepaid)

    return render(request, 'prepaid_app/history.html', {'histories': histories})
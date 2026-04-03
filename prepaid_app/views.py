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

    qr_filename = generate_qr(prepaid.prepaid_no)

    return render(request, "prepaid_app/dashboard.html", {
        "data": prepaid,
        "qr_path": qr_filename
    })

@login_required
def view_qr(request):
    prepaid = Prepaid.objects.filter(user=request.user).first()

    qr_filename = generate_qr(prepaid.prepaid_no)

    return render(request, "prepaid_app/qr.html", {
        "qr_path": qr_filename
    })

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
    else:
        form = RegisterForm()

    return render(request, 'prepaid_app/register.html', {'form': form})


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
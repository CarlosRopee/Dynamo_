from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as django_login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import logging
from .forms import CustomUserCreationForm
from .models import UserProfile, DadosUsuario
from django.http import JsonResponse

logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'menu.html')

def menu_views(request):
    return render(request, 'menu.html')

def cadastro(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'cadastro.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            user = form.get_user()
            django_login(request, user)
            messages.success(request, "Login realizado com sucesso.")
            return redirect('menu')
        else:
            messages.error(request, "Usuário ou senha incorretos.")
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def item1_view(request):
    return render(request, 'item1.html')

def item2_view(request):
    return render(request, 'item2.html')

def item3_view(request):
    return render(request, 'item3.html')

def item4_view(request):
    return render(request, 'item4.html')

def item5_view(request):
    return render(request, 'item5.html')

def novo1_view(request):
    return render(request, 'novo1.html')

def novo2_view(request):
    return render(request, 'novo2.html')

def novo3_view(request):
    return render(request, 'novo3.html')

def novo4_view(request):
    return render(request, 'novo4.html')

def novo5_view(request):
    return render(request, 'novo5.html')

from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from .models import UserProfile
from django.contrib.auth.decorators import login_required

@method_decorator(login_required, name='dispatch')
class MeusDadosView(TemplateView):
    template_name = 'dados.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        context['user_profile'] = user_profile
        return context

@login_required
def minhas_compras(request):
    # Lógica para exibir as compras do usuário aqui
    return render(request, 'minhas_compras.html')

def sucesso(request):
    return render(request, 'sucesso.html')

def falha(request):
    return render(request, 'falha.html')

from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import stripe

stripe.api_key = "sk_test_51OIaNcFVm1TF86fp47xAdFyuN9L08AxPYZB0FYlMbGRC2ESsULwWTUcIO2hL4yzOLJSh8YIzKcJkCEwiwXqyn1PU00uXCvPTrM"
endpoint_secret = 'whsec_a405ca5981b0441e497b494eb20add74335f49503c11c19c67c53c6feba80c43'

@require_POST
@csrf_exempt
def webhook(request):
    payload = request.body
    sig_header = request.headers.get('Stripe-Signature')

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        logger.error('Invalid payload: {}'.format(str(e)))
        return JsonResponse({'success': False}, status=400)
    except stripe.error.SignatureVerificationError as e:
        logger.error('Invalid signature: {}'.format(str(e)))
        return JsonResponse({'success': False}, status=400)
    except Exception as e:
        logger.error('Error handling webhook: {}'.format(str(e)))
        return JsonResponse({'success': False}, status=500)

    logger.info('Received event of type: {}'.format(event['type']))

    if event['type'] == 'payment_intent.succeeded':
        logger.info('Redirecting to success')
        return redirect('sucesso')
    elif event['type'] == 'payment_intent.payment_failed':
        logger.info('Redirecting to failure')
        return redirect('falha')

    return JsonResponse({'success': True})

from django.contrib.auth import logout

def custom_logout(request):
    logout(request)
    return redirect('menu')

def enderecos_cadastrados(request):
    # Sua lógica para endereços cadastrados aqui
    return render(request, 'enderecos_cadastrados.html')

@login_required
def enderecos_cadastrados(request):
    # Sua lógica para endereços cadastrados aqui
    return render(request, 'enderecos_cadastrados.html')

import json

def atualizar_informacoes(request):
    if request.method == 'POST':
        try:
            dados = json.loads(request.body)
            nome = dados.get('nome')
            email = dados.get('email')
            
            user = request.user
            user.username = nome
            user.email = email
            user.save()

            return JsonResponse({'mensagem': 'Informações atualizadas com sucesso!'})
        except json.JSONDecodeError:
            return JsonResponse({'erro': 'Erro ao analisar os dados JSON'}, status=400)

    return JsonResponse({'erro': 'Método de requisição não permitido'}, status=405)

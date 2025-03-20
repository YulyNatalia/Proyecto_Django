# solicitudes/views.py
from django.http import JsonResponse
from django.views import View
import requests
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login
from solicitudes.forms import RegistroForm  # Importa desde el módulo actual
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import SolicitudMaterial  # Asegúrate de importar el modelo

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()  # Guarda el nuevo usuario
            login(request, user)  # Inicia sesión automáticamente después del registro
            return redirect('home')  # Redirige a la página de inicio
    else:
        form = RegistroForm()
    return render(request, 'solicitudes/registro.html', {'form': form})

@login_required
def home(request):
    return render(request, 'solicitudes/home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirige a la vista de inicio
        else:
            return render(request, 'solicitudes/login.html', {'error': 'Credenciales inválidas'})
    return render(request, 'solicitudes/login.html')

class ObtenerDatosView(View):
    def get(self, request):
        try:
            response = requests.get('https://api.ejemplo.com/datos')  # Cambia esta URL por la API que desees
            response.raise_for_status()  # Lanza un error si la respuesta no es 200
            datos = response.json()  # Procesar la respuesta JSON
            return JsonResponse(datos, safe=False)  # Devuelve los datos como JSON
        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)

class EnviarDatosView(View):
    def post(self, request):
        data = {'clave': 'valor'}  # Cambia esto por los datos que deseas enviar
        try:
            response = requests.post('https://api.ejemplo.com/datos', json=data)  # Cambia esta URL por la API que desees
            response.raise_for_status()  # Lanza un error si la respuesta no es 200
            return JsonResponse({'mensaje': 'Datos enviados correctamente'}, status=201)
        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt  # Permite enviar datos sin el token CSRF (solo para desarrollo, no usar en producción)
def solicitar_material(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        tipo_material = request.POST.get('tipo_material')
        cantidad = request.POST.get('cantidad')
        comentarios = request.POST.get('comentarios')

        # Crear y guardar la solicitud en la base de datos
        solicitud = SolicitudMaterial(
            nombre_solicitante=nombre,
            tipo_material=tipo_material,
            cantidad=cantidad,
            comentarios=comentarios
        )
        solicitud.save()

        # Retornar una respuesta JSON
        return JsonResponse({'mensaje': 'Tu solicitud se ha enviado correctamente.'})
    
    # Si no es una solicitud POST, renderizar la plantilla
    return render(request, 'solicitudes/solicitar_material.html')


def inventario(request):
    solicitudes = SolicitudMaterial.objects.all().order_by('-fecha_creacion')  # Ordenar por fecha descendente
    return render(request, 'solicitudes/inventario.html', {'solicitudes': solicitudes})


from django.shortcuts import render, get_object_or_404, redirect
from .models import SolicitudMaterial
from .forms import SolicitudMaterialForm

def editar_solicitud(request, id):
    # Obtener la solicitud específica por su ID
    solicitud = get_object_or_404(SolicitudMaterial, id=id)
    
    if request.method == 'POST':
        # Si el formulario se envía, procesar los datos
        form = SolicitudMaterialForm(request.POST, instance=solicitud)
        if form.is_valid():
            form.save()  # Guardar los cambios en la base de datos
            return redirect('inventario')  # Redirigir a la página principal
    else:
        # Si es una solicitud GET, mostrar el formulario con los datos actuales
        form = SolicitudMaterialForm(instance=solicitud)
    
    # Renderizar la plantilla de edición con el formulario
    return render(request, 'solicitudes/home.html', {'solicitudes': SolicitudMaterial.objects.all()})
def eliminar_solicitud(request, id):
    solicitud = get_object_or_404(SolicitudMaterial, id=id)
    if request.method == 'POST':
        solicitud.delete()
        return redirect('inventario')
    return render(request, 'solicitudes/confirmar_eliminar.html', {'solicitud': solicitud})
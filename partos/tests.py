
from django.test import TestCase, Client
from django.urls import reverse
from .models import Madre, Parto, RN

class FlujoPartosTestCase(TestCase):
	def setUp(self):
		self.client = Client()
		self.madre_data = {
			'nombre': 'Juana Perez',
			'rut': '12345678-9',
			'fecha_nacimiento': '1990-01-01',
			'direccion': 'Calle Falsa 123',
			'telefono': '912345678',
			'antecedentes_obstetricos': 'Ninguno',
			'atenciones_clinicas': 'Ninguna',
			'acompañante': 'Pedro Perez',
		}
		self.parto_data = {
			'fecha_hora': '2025-12-04T10:00',
			'tipo_parto': 'vaginal',
			'tipo_parto_clasificado': 'Normal',
			'complicaciones': '',
			'parto_distocico': False,
			'parto_vacuum': False,
			'rem_a24': False,
		}
		self.rn_data = {
			'apellido_paterno_rn': 'Perez',
			'fecha_nacimiento': '2025-12-04',
			'hora_nacimiento': '10:30',
			'peso': 3500,
			'talla': 50,
			'cc': 34.5,
			'semanas_gestacion': 39,
			'dias_gestacion': 0,
			'sexo': 'F',
			'apego': True,
			'lactancia_antes_60': True,
			'profilaxis_ocular': True,
			'vacuna_hepatitis_b': True,
			'vacuna_bcg': True,
			'profesional_vhb': 'Matrona',
			'apgar_1': 8,
			'apgar_5': 9,
			'anomalia_congenita': False,
			'reanimacion_basica': False,
			'reanimacion_avanzada': False,
			'ehi_grado_ii_iii': False,
		}

	def test_ingreso_madre_post_redirecciona_a_form_madre(self):
		url = reverse('ingreso_madre')
		response = self.client.post(url, {'rut': self.madre_data['rut']})
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'partos/form_madre.html')

	def test_guardar_madre_post_redirecciona_a_ingreso_parto(self):
		# Primero crear la madre en sesión
		self.client.post(reverse('ingreso_madre'), {'rut': self.madre_data['rut']})
		url = reverse('guardar_madre')
		response = self.client.post(url, self.madre_data)
		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, reverse('ingreso_parto'))

	def test_ingreso_parto_post_redirecciona_a_ingreso_rn(self):
		# Crear madre y guardar en sesión
		self.client.post(reverse('ingreso_madre'), {'rut': self.madre_data['rut']})
		self.client.post(reverse('guardar_madre'), self.madre_data)
		url = reverse('ingreso_parto')
		response = self.client.post(url, self.parto_data)
		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, reverse('ingreso_rn'))

	def test_ingreso_rn_post_redirecciona_a_listado_rn(self):
		# Crear madre y parto y guardar en sesión
		self.client.post(reverse('ingreso_madre'), {'rut': self.madre_data['rut']})
		self.client.post(reverse('guardar_madre'), self.madre_data)
		self.client.post(reverse('ingreso_parto'), self.parto_data)
		url = reverse('ingreso_rn')
		response = self.client.post(url, self.rn_data)
		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, reverse('listado_rn'))

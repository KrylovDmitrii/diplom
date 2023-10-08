from django.shortcuts import render
import requests
from bs4 import BeautifulSoup
import requests
import math


def visibility():
    url = 'https://meteoinfo.ru/pogoda/russia/moscow-area/moscow'
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    td_element = soup.find('td', string='Горизонтальная видимость, км')
    visibility_element = td_element.find_next('td')
    mdv = 9
    if visibility_element is None:
        return mdv
    return float(visibility_element.text.strip())


def attenuation(from_mdv, wave):
    wave = float(wave)
    qs = {
        '0.1': -0.129,
        '0.2': 0.129,
        '0.3': 0.2,
        '0.4': 0.3,
        '0.5': 0.34,
        '0.6': 0.39,
        '0.7': 0.41,
        '0.8': 0.45,
        '0.9': 0.49,
        '1.0': 0.53,
        '2.0': 0.72,
        '3.0': 0.85,
        '4.0': 0.94,
        '5.0': 1.05,
        '6.0': 1.1,
        '7.0': 1.15,
        '8.0': 1.2,
        '9.0': 1.25,
        '10.0': 1.3,
        '11.0': 1.35,
        '12.0': 1.4,
        '13.0': 1.45,
        '14.0': 1.50,
        '15.0': 1.55,
        '16.0': 1.6,
        '17.0': 1.65,
        '18.0': 1.7,
        '19.0': 1.75,
        '20.0': 1.8,

    }
    q = qs.get(str(from_mdv))
    wave = wave / 1000
    c = 13
    result = str((c / from_mdv) * pow((wave / 0.55), -q))
    return float(result[:result.find('.') + 3])


def distance(eqpwave, diametr, energy, degree, from_mdv1):
    temp = attenuation(from_mdv1, eqpwave)
    x = 0.001
    while 20 * math.log10((x * degree / diametr)) + temp * x < -energy:
        x += 0.01
    return x * 1000


def calc(request):
    equipments = {
        'M1-10GE ARTOLINK': {'lenwave': 1550, 'diametr': 0.87, 'energy': 30, 'degree': 0.01},
        'M1-FE-L ARTOLINK': {'lenwave': 785, 'diametr': 0.96, 'energy': 14, 'degree': 0.15},
        'M1-GE ARTOLINK': {'lenwave': 1550, 'diametr': 0.84, 'energy': 6, 'degree': 0.15},
        '1000М-АС1 ЛАНтастИКа': {'lenwave': 780, 'diametr': 1.08, 'energy': 20, 'degree': 0.6},
        '1000М-АС2 ЛАНтастИКа': {'lenwave': 780, 'diametr': 1.08, 'energy': 14, 'degree': 0.5},
        '1000М-АС3 ЛАНтастИКа': {'lenwave': 780, 'diametr': 1.08, 'energy': 7, 'degree': 0.4}
    }
    lenwave = {
        '785 нм': 785,
        '1550 нм': 1550,
    }
    if request.method == 'GET':
        context = {
            'equipment': equipments,
            'waveslen': lenwave
        }
        return render(request=request, template_name='calc_FSO/index.html', context=context)

    if request.method == 'POST' and 'waveslen' in str(request.POST):
        from_wave = request.POST.get('waveslen')
        wave = float(lenwave.get(from_wave))
        from_mdv = request.POST.get('from_mdv')
        try:
            from_mdv = float(from_mdv)
        except (TypeError, ValueError):
            from_mdv = visibility()
        result = attenuation(from_mdv, wave)
        context = {
            'from_mdv': from_mdv,
            'from_wave': from_wave,
            'waveslen': lenwave,
            'equipment': equipments,
            'result': result
        }
        return render(request=request, template_name='calc_FSO/index.html', context=context)

    else:
        from_equip = request.POST.get('equipment')
        eqpwave = float(equipments[from_equip].get('lenwave'))
        diametr = float(equipments[from_equip].get('diametr'))
        energy = float(equipments[from_equip].get('energy'))
        degree = float(equipments[from_equip].get('degree'))
        from_mdv1 = request.POST.get('from_mdv1')
        try:
            from_mdv1 = float(from_mdv1)
        except (TypeError, ValueError):
            from_mdv1 = visibility()
        result1 = int(distance(eqpwave, diametr, energy, degree, from_mdv1))
        context1 = {
            'form_active': 'form1',
            'from_mdv1': from_mdv1,
            'waveslen': lenwave,
            'from_equip': from_equip,
            'equipment': equipments,
            'result1': result1
        }
        return render(request=request, template_name='calc_FSO/index.html', context=context1)

# два калькулятора, расчет потерь на линии (2 параметра) и расчет макс расстояния линии (то что есть + аппаратура)

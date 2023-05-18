from django.shortcuts import render
import requests


def calc(request):
    response = {
        'Утро': 1,
        'День': 10,
        'Вечер': 5,
        'Ночь': 0,
    }
    if request.method == 'GET':
        context = {
            'daytime': response
        }
        return render(request=request, template_name='calc_FSO/index.html', context=context)

    if request.method == 'POST':
        from_pout = float(request.POST.get('from_pout'))
        from_pin = float(request.POST.get('from_pin'))
        from_day = request.POST.get('daytime')
        day = float(response.get(from_day))

        result = (from_pout - from_pin) * day
        context = {
            'from_pout': from_pout,
            'from_pin': from_pin,
            'from_day': from_day,
            'daytime': response,
            'result': result
        }
        return render(request=request, template_name='calc_FSO/index.html', context=context)
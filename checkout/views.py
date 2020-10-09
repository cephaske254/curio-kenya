from django.shortcuts import render

# Create your views here.
def cart(request):
    context = {
        'title':'Cart Summary'
    }
    return render(request,'checkout/summary.html',context=context)
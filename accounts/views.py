from django.shortcuts import render
from .models import Rule, CustomUser

# Create your views here.


def login(request):
    # new_user = CustomUser(username="poon3", card_id="7654321")
    # new_user.set_password("1234")
    # new_user.save()

    new_rule = Rule(rule_name="rule6")
    new_rule.fine_per_day = 1.5
    new_rule.borrow_limit = 20
    new_rule.reserve_limit = 20
    new_rule.borrow_period =200
    new_rule.save()
    return render(request, 'accounts/login.html')


def logout(request):
    return render(request, 'pages/index.html')


def dashboard(request):
    return render(request, 'accounts/dashboard.html')


def register(request):
    allrules_queryset = Rule.objects.all()
    allusers_queryset = CustomUser.objects.all()

    filterrule_queryset = Rule.objects.filter(borrow_limit=14)
    selected_rule = Rule.objects.get(rule_name="default")
    filteruser_queryset = CustomUser.objects.filter(rule=selected_rule)
    length = len(filteruser_queryset)
    print("number of user using this rule is " + str(length))
    
    # change borrow_limit of rule2 = 18
    select_rule5 = Rule.objects.get(rule_name="rule5", fine_per_day=1.5)
    select_rule5.rule_name = "rule 7"
    select_rule5.save()
    
    context = {'myvariable': 3, 
               'allrules_queryset': allrules_queryset,
               'allusers_queryset': allusers_queryset,
               'filterrule_queryset': filterrule_queryset,
               'filteruser_queryset': filteruser_queryset,
               }
    return render(request, 'accounts/register.html', context)


def forgotpass(request):
    return render(request, 'accounts/forgotpass.html')


def changepass(request):
    return render(request, 'accounts/changepass.html')

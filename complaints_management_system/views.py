from django.shortcuts import render,redirect
# from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
from django.db.models import Count,Max
from django.db.models.functions import TruncMonth,TruncDate,TruncYear
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout,get_user_model
from django.contrib.auth.decorators import login_required
from .utils import render_to_pdf
from .models import *
from .forms import *
from .decorator import restricted_path
from datetime import datetime,date

# Auth
def loginPage(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == "POST":
            username = request.POST.get("username")
            password = request.POST.get("password")

            user = authenticate(request, username=username,password=password)

            if user is not None:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.warning(request, "Your username or password is incorrect")

        return render(request,"authentication/login.html")

def registerPage(request):
    form = CreateUserForm()

    if request.user.is_authenticated:
        return redirect('dashboard')
    else:
        if request.method == "POST":
            form = CreateUserForm(request.POST)

            if form.is_valid():
                form.save()
                messages.success(request, "Your account has been successfully created")
                return redirect('login')

        context = {'form':form}
        return render(request,"authentication/register.html",context)

def logoutPage(request):
    logout(request)
    return redirect('login')

# Dashboard
@login_required(login_url="login")
def Dashboard(request):
    NewUser = get_user_model()

    count_entity   = Entities.objects.all().count()
    count_complaints = Complaints.objects.all().count()
    count_purok      = Purok.objects.all().count()
    count_user       = NewUser.objects.all().count()

    # condition = 'YEAR(date_complaint) = '
    # year  = date.today().year
    # where = f"{condition}{year}"

    latest_complaint = Complaints.objects.annotate(date=TruncDate('date_complaint')).values('date').filter(date = date.today()).count()

    context = {"count_entity":count_entity,"count_complaints":count_complaints,"count_purok":count_purok,"latest_count":latest_complaint,"count_user":count_user}

    return render(request,"dashboard/dashboard.html",context)

@login_required(login_url="login")
def complaint_chart(request):
    if request.method == "GET":
        amount = []
        month  = []

        # condition = 'YEAR(date_complaint) = '

        condition = "strftime('%Y',date_complaint) = "
        year  = date.today().year
        where = f"{condition}{year}"

        # complaintsChart = Complaints.objects.annotate(month=TruncMonth('date_complaint')).values('month').annotate(count=Count('complaint_id')).values('month','count').extra(where=[where]).order_by("month")


        complaintsChart = Complaints.objects.annotate(month=TruncMonth('date_complaint')).values('month').annotate(count=Count('complaint_id')).values('month','count').filter().order_by("month")

        for data in complaintsChart:
            month.append(datetime.strftime(data['month'],"%b"))
            amount.append(data['count'])

        return JsonResponse(data={"amount":amount,"month":month},safe=True)
    else:
        return JsonResponse(data={"status":"bad_request"})

@login_required(login_url="login")
def purok_chart(request):

    if request.method == "GET":
        
        no_complaints = []
        purok_name    = []

        #  sql = Complaints.objects.select_related('respondent','purok').values_list('respondent__respondent_purok').annotate(total=Count('complaint_id')).values('respondent__respondent_purok','total')

        purokComplaints = Complaints.objects.select_related('respondent').values_list('respondent__respondent_purok').annotate(total=Count('complaint_id')).values('respondent__respondent_purok','total')

        for info in purokComplaints:
            selectAllPurok = Purok.objects.filter(purok_id=info['respondent__respondent_purok'])
            for j in list(selectAllPurok):
                purok_name.append(j.purok_name)
            no_complaints.append(info['total'])

        return JsonResponse(data={"no_complaints":no_complaints,"purok_name":purok_name},safe=True)
    else:
        return JsonResponse(data={"status":"bad_request"})

# Purok
@login_required(login_url="login")
@restricted_path
def PurokPage(request):
    purok_instance = Purok.objects.all().order_by("date_added")
    FormInstance = PurokForm()
    context = {"puroks":purok_instance,"form":FormInstance}
    return render(request, "purok/purok.html",context)


@login_required(login_url="login")
def AddPurokPage(request):
    if request.method == "POST":
        purok_name = request.POST["purok_name"]

        purok_info = Purok(purok_name=purok_name)
        purok_info.save()

        return HttpResponseRedirect('/add_purok/')
    else:
        return render(request,"purok/add_purok.html")


@login_required(login_url="login")
def UpdatePurokPage(request):
    if request.method == "POST":
        PurokInstance = list(Purok.objects.values().filter(pk=request.POST.get("purok_id")))
        return JsonResponse({"status":"success","info":PurokInstance})
    else:
        return JsonResponse({"status":"bad_request"})


@login_required(login_url="login")
def execute_update_purok(request):
    if request.method == "POST":
        PurokInstance = Purok.objects.get(pk=request.POST.get("purok_id"))
        execute = PurokForm(request.POST,instance=PurokInstance)

        if execute.is_valid():
            execute.save()
            return JsonResponse({"status":"success"})
        else:
            return HttpResponse(execute.errors.as_json())
    else:
        return JsonResponse({"status":"bad_request"})

@login_required(login_url="login")
def DeletePurokPage(request):
    if request.method == "POST":
        PurokInstance = Purok.objects.get(pk=request.POST.get('purok_id'))
        PurokInstance.delete()
        return JsonResponse({"status":"success"})
    else:
        return JsonResponse({"status":"bad_request"})

# Complaints

@login_required(login_url="login")
def ComplaintsPage(request):
    complaints = Complaints.objects.all().order_by("date_complaint","case_no")
    complaintsForm = ComplaintsForm()

    context = {"complaints":complaints,"form" : complaintsForm}

    return render(request, "complaint/complaint.html",context)

@login_required(login_url="login")
def AddComplaintsPage(request):
    form = ComplaintsForm()
    if request.method == "POST":
        complaints_info = ComplaintsForm(request.POST)
        print(request.POST.get("purok"))
        if complaints_info.is_valid():
            complaints_info.save()
            return JsonResponse({"status":"success"})
        else:
            return HttpResponse(complaints_info.errors.as_json())
    else:
        context = {"form":form}
        return render(request, "complaint/add_complaint.html",context)


@login_required(login_url="login")
def UpdateComplaintsPage(request):
    complaint_info = list(Complaints.objects.values().filter(pk=request.POST["complaint_id"]))
    return JsonResponse({"status":"success","info":complaint_info},safe=True)


@login_required(login_url="login")
def execute_update_complaint(request):
    if request.method == "POST":

        complaint_instance = Complaints.objects.get(pk=request.POST['complaint_id'])
        execute = ComplaintsForm(request.POST,instance=complaint_instance)

        if execute.is_valid():
            execute.save()

            return JsonResponse({"status":"success"},safe=True)

        else:
            return HttpResponse(execute.errors.as_json())

    return JsonResponse({"status":"bad_request"},safe=True)



@login_required(login_url="login")
def DeleteComplaintsPage(request):

    if request.method == "POST":
        DeleteComplaintInstance = Complaints.objects.get(pk=request.POST.get("complaint_id"))
        DeleteComplaintInstance.delete()
        return JsonResponse({"status":"success"})
    else:
        return JsonResponse({"status":"bad_request"})

# Position
@login_required(login_url="login")
@restricted_path
def PositionPage(request):
    form = PositionForm()
    PositionInstance = Position.objects.all().order_by("date_added")
    context = {"form":form,"positions":PositionInstance}
    return render(request, "position/position.html",context)

@login_required(login_url="login")
def AddPositionPage(request):
    if request.method == "POST":

        position_info = PositionForm(request.POST)
        position_info.save()

        return HttpResponseRedirect('/position/')
    else:
        context = {"form":PositionForm()}
        return render(request,"position/add_position.html",context)

@login_required(login_url="login")
def execute_update_position(request):
    if request.method == "POST":
        position_instance = Position.objects.get(pk=request.POST['position_id'])
        execute = PositionForm(request.POST,instance=position_instance)

        if execute.is_valid():
            execute.save()

            return JsonResponse({"status":"success"},safe=True)

        else:
            return HttpResponse(execute.errors.as_json())
    else:
        return JsonResponse({"status":"bad_request"})

@login_required(login_url="login")
def UpdatePositionPage(request):
    if request.method == "POST":
        PositionInstance = list(Position.objects.values().filter(pk=request.POST.get("position_id")))
        return JsonResponse({"status":"success","info":PositionInstance})
    else:
        return JsonResponse({"status":"bad_request"})

@login_required(login_url="login")
def DeletePositionPage(request):
    if request.method == "POST":
        PositionInstance = Position.objects.get(pk=request.POST.get("position_id"))
        PositionInstance.delete()
        return JsonResponse({"status":"success"})
    else:
        return JsonResponse({"status":"bad_request"})

# Respondent
@login_required(login_url="login")
@restricted_path
def RespodentPage(request):
    RespondentInstance = Respondents.objects.all().order_by("respondent_purok")
    form = RespondentForm()
    context = {"respondent_info":RespondentInstance,"form":form}
    return render(request,"respondent/respondent.html",context)

def AddRespondentPage(request):
    form = RespondentForm()
    if request.method == "POST":
        respondent_info = RespondentForm(request.POST)
        respondent_info.save()
        return HttpResponseRedirect('/respondent/')
    else:
        context = {"form":form}
        return render(request,"respondent/add_respondent.html",context)

@login_required(login_url="login")
def UpdateRespondentPage(request):
    respondent_info = list(Respondents.objects.values().filter(pk=request.POST["respondent"]))

    return JsonResponse({"status":"success","info":respondent_info},safe=True)

@login_required(login_url="login")
def execute_update_respondent(request):
    if request.method == "POST":

        respondent_instance = Respondents.objects.get(pk=request.POST['respondent_id'])
        execute = RespondentForm(request.POST,instance=respondent_instance)

        if execute.is_valid():
            execute.save()
            return JsonResponse({"status":"success"},safe=True)
        else:
            return HttpResponse("Error")
    else:
        return JsonResponse({"status":"bad_request"},safe=True)

@login_required(login_url="login")
def DeleteRespondentPage(request):

    if request.method == "POST":
        RespondentInstance = Respondents.objects.get(pk=request.POST['respondent'])
        RespondentInstance.delete()
        return JsonResponse({"status":"success"})
    else:
        return JsonResponse({"status":"bad_request"})

# Government Entity
@login_required(login_url="login")
@restricted_path
def GovernmentEntityPage(request):
    entity_info = Entities.objects.all().order_by("date_added")
    form = EntitiesForm()
    context = {"entity_info":entity_info,"form":form}
    return render(request,"entity/entity.html",context)


@login_required(login_url="login")
def AddGovernmentEntityPage(request):

    if request.method == "POST":
        name = request.POST["entity_name"]

        entity_info = Entities(entity_name=name)
        entity_info.save()
        return HttpResponseRedirect('/add_entity/')
    else:
        return render(request,"entity/add_entity.html")


@login_required(login_url="login")
def UpdateGovernmentEntityPage(request):
    entity_info = list(Entities.objects.values().filter(pk=request.POST["entity_id"]))
    return JsonResponse({"status":"success","info":entity_info},safe=True)

@login_required(login_url="login")
def execute_update_entity(request):
    if request.method == "POST":

        entity_instance = Entities.objects.get(pk=request.POST['entity_id'])
        execute = EntitiesForm(request.POST,instance=entity_instance)

        if execute.is_valid():
            execute.save()

            return JsonResponse({"status":"success"},safe=True)

        else:
            return HttpResponse(execute.errors.as_json())

    else:
        return JsonResponse({"status":"bad_request"},safe=True)


@login_required(login_url="login")
def DeleteGovernmentEntityPage(request):
    if request.method == "POST":
        EntityInstance = Entities.objects.get(pk=request.POST['entity_id'])
        EntityInstance.delete()
        return JsonResponse({"status":"success"})
    else:
        return JsonResponse({"status":"bad_request"})


# Complainants
@login_required(login_url="login")
@restricted_path
def ComplainantsPage(request):
    complainant = Complainant.objects.all().order_by("date_added")
    form = ComplainantForm()
    context = {"complainants":complainant,"form":form}
    return render(request, "complainants/complainants.html",context)

@login_required(login_url="login")
def AddComplainantsPage(request):
    form = ComplainantForm()

    if request.method == "POST":
        complainant_info = ComplainantForm(request.POST)
        complainant_info.save()
        return HttpResponseRedirect('/complainant/')
    else:
        context = {"form":form}
        return render(request, "complainants/add_complainants.html",context)


@login_required(login_url="login")
def UpdateComplainantsPage(request):
    complaintInstance = list(Complainant.objects.values().filter(pk=request.POST["complainant_id"]))
    return JsonResponse({"status":"success","info":complaintInstance},safe=True)


@login_required(login_url="login")
def execute_update_complainant(request):
    if request.method == "POST":

        complainant_instance = Complainant.objects.get(pk=request.POST['complainant_id'])
        execute = ComplainantForm(request.POST,instance=complainant_instance)

        if execute.is_valid():
            execute.save()

            return JsonResponse({"status":"success"},safe=True)

        else:
            return HttpResponse(execute.errors.as_json())

    else:
        return JsonResponse({"status":"bad_request"},safe=True)

@login_required(login_url="login")
def DeleteComplainantsPage(request):
    if request.method == "POST":
        ComplainantInstance = Complainant.objects.get(pk=request.POST['complainant_id'])
        ComplainantInstance.delete()
        return JsonResponse({"status":"success"})
    else:
        return JsonResponse({"status":"bad_request"})

@login_required(login_url="login")
def generate_complainant_form(request,id):
    if request.method == "GET":
        complaintInstance = Complaints.objects.all().filter(pk=id)
        context = {"information":complaintInstance}
        pdf = render_to_pdf('pdf/complainant_form.html',context)
        return HttpResponse(pdf, content_type='application/pdf')
    else:
        return HttpResponseRedirect('/complaint/')

@login_required(login_url="login")
def generate_summon(request,id):
    if request.method == "GET":
        complaintInstance = Complaints.objects.all().filter(pk=id)
        context = {"information":complaintInstance}
        pdf = render_to_pdf('pdf/sumon_form.html',context)
        return HttpResponse(pdf,content_type="application/pdf")
    else:
        return HttpResponseRedirect('/complaint/')

@login_required(login_url="login")
def generate_amicable_settlement(request,id):
    if request.method == "GET":
        complaintInstance = Complaints.objects.all().filter(pk=id)
        context = {"information":complaintInstance,"current_date": datetime.now().date()}
        pdf = render_to_pdf('pdf/amicable_settlement.html',context)
        return HttpResponse(pdf,content_type="application/pdf")
    else:
        return HttpResponseRedirect('/complaint/')

@login_required(login_url="login")
def generate_officer_return(request,id):
    if request.method == "GET":
        complaintInstance = Complaints.objects.all().filter(pk=id)
        context = {"information":complaintInstance,"current_date": datetime.now().date()}
        pdf = render_to_pdf('pdf/officer_return.html',context)
        return HttpResponse(pdf,content_type="application/pdf")
    else:
        return HttpResponseRedirect('/complaint/')

@login_required(login_url="login")
def generate_complaints_report(request):
    complaints = Complaints.objects.all()
    context = {"information":complaints}
    pdf = render_to_pdf('pdf/complaints_report.html',context)
    return HttpResponse(pdf,content_type="application/pdf")


@login_required(login_url="login")
def generate_complaintsbypurok_report(request):
    pdf = render_to_pdf('pdf/complaints_graph_report.html')
    return HttpResponse(pdf,content_type="application/pdf")

@login_required(login_url="login")
def generate_fileaction_report(request,id):
    ComplaintInstance = Complaints.objects.all().filter(pk=id)
    context = {"complaint":ComplaintInstance,"user_entity":request.user.entity}
    pdf = render_to_pdf('pdf/fileaction_report.html',context)
    return HttpResponse(pdf,content_type="application/pdf")

def error_404_view(request,exception=None):
    return render(request,"dashboard/404.html")

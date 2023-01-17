from django.urls import path
from . import views

urlpatterns = [
    # authentication
    path('',views.loginPage,name="login"),
    path('register/',views.registerPage,name="register"),
    path('logout/',views.logoutPage,name="logout"),
    
    # dashboard
    path('dashboard/',views.Dashboard,name="dashboard"),
    path('purok_chart/',views.purok_chart,name="purok_chart"),
    path('complaint_chart/',views.complaint_chart,name="complaint_chart"),
    # path('pagenotfound/',views.error_404_view, name="pagenotfound"),

    # entities
    path('entities/',views.GovernmentEntityPage,name="entities"),
    path('add_entity/',views.AddGovernmentEntityPage,name="add_entity"),
    path('update_entity/',views.UpdateGovernmentEntityPage,name="update_entity"),
    path('delete_entity/',views.DeleteGovernmentEntityPage,name="delete_entity"),
    path('execute_update_entity/',views.execute_update_entity,name="execute_update_entity"),

    # position
    path('position/',views.PositionPage,name="position"),
    path('add_position/',views.AddPositionPage,name="add_position"),
    path('update_position/',views.UpdatePositionPage,name="update_position"),
    path('delete_position/',views.DeletePositionPage,name="delete_position"),
    path('execute_update_position/',views.execute_update_position,name="execute_update_position"),

    # purok
    path('purok/',views.PurokPage,name="purok"),
    path('add_purok/',views.AddPurokPage,name="add_purok"),
    path('update_purok/',views.UpdatePurokPage,name="update_purok"),
    path('delete_purok/',views.DeletePurokPage,name="delete_purok"),
    path('execute_update_purok/',views.execute_update_purok,name="execute_update_purok"),

    #complainant
    path('complainant/',views.ComplainantsPage,name="complainant"),
    path('add_complainant/', views.AddComplainantsPage, name="add_complainant"),
    path('update_complainant/', views.UpdateComplainantsPage, name="update_complainant"),
    path('delete_complainant/', views.DeleteComplainantsPage, name="delete_complainant"),
    path('execute_update_complainant/', views.execute_update_complainant, name="execute_update_complainant"),

    #complaint
    path('complaint/',views.ComplaintsPage,name="complaint"),
    path('add_complaint/', views.AddComplaintsPage, name="add_complaint"),
    path('update_complaint/', views.UpdateComplaintsPage, name="update_complaint"),
    path('delete_complaint/', views.DeleteComplaintsPage, name="delete_complaint"),
    path('execute_update_complaint/', views.execute_update_complaint, name="execute_update_complaint"),


    #respondent
    path('respondent/',views.RespodentPage,name="respondent"),
    path('add_respondent/', views.AddRespondentPage, name="add_respondent"),
    path('update_respondent/', views.UpdateRespondentPage, name="update_respondent"),
    path('delete_respondent/', views.DeleteRespondentPage, name="delete_respondent"),
    path('execute_update_respondent/', views.execute_update_respondent, name="execute_update_respondent"),
    
    # generate pdf
    path('generate_complainant_form/<int:id>',views.generate_complainant_form,name="generate_complainant_form"),
    path('generate_summon/<int:id>',views.generate_summon,name="generate_summon"),
    path('generate_amicable_settlement/<int:id>',views.generate_amicable_settlement,name="generate_amicable_settlement"),
    path('generate_officer_return/<int:id>',views.generate_officer_return,name="generate_officer_return"),
    
    path('generate_complaints_report/',views.generate_complaints_report,name="generate_complaints_report"),
    path('generate_complaintsbypurok_report/',views.generate_complaintsbypurok_report,name="generate_complaintsbypurok_report"),
    path('generate_fileaction_report/<int:id>',views.generate_fileaction_report,name="generate_fileaction_report")

]

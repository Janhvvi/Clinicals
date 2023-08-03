from django.shortcuts import render,redirect
from clinicalsApp.models import Patient,ClinicalData
from clinicalsApp.forms import ClinicalDataForm
from django.views.generic import ListView,CreateView,UpdateView,DeleteView
from django.urls import reverse_lazy

# Create your views here.
class PatientListView(ListView):
    model=Patient                      
    #patient_list
    
class PatientCreateView(CreateView):
    model=Patient
    success_url=reverse_lazy('index')
    fields=('firstName','lastName','age')
    #patient_form
    
class PatientUpdateView(UpdateView):
    model=Patient
    success_url=reverse_lazy('index')
    fields=('firstName','lastName','age')
    
class PatientDeleteView(DeleteView):
    model=Patient
    success_url=reverse_lazy('index')
    
def AddData(request,**kwargs):
    form=ClinicalDataForm()
    patient=Patient.objects.get(id=kwargs['pk'])
    if request.method=='POST':
        form=ClinicalDataForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('/')
    return render(request,'clinicalsApp/clinicaldata_form.html',{'form':form,'patient':patient})

def analyze(request,**kwargs):
    data=ClinicalData.objects.filter(patient_id=kwargs['pk'])
    responseData=[]
    for eachEntry in data:
        if eachEntry.componentName=='hw':
            heightAndWeight=eachEntry.componentValue.split('/')
            if len(heightAndWeight)>1:
                feetToMetres=float(heightAndWeight[0]) * 0.4536
                BMI=(float(heightAndWeight[1])) / (feetToMetres*feetToMetres)
                bmiEntry=ClinicalData()
                bmiEntry.componentName='BMI'
                bmiEntry.componentValue=BMI
                responseData.append(bmiEntry)
        responseData.append(eachEntry)
    return render(request,'clinicalsApp/generateReport.html',{'data':responseData})
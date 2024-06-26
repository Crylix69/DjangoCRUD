from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm, CreateRecordForm, UpdateRecordForm, BICSetupForm, MCRegisterForm, PesoNetForm

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

from .models import  Record, BICSetup, MCRegister, PesoNet, UserProfile
 
from django.contrib import messages



#Homepage 
def home(request):
    return render(request, 'webapp/index.html')


# Register
def register(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Get additional fields from the form
            user_type = form.cleaned_data.get('user_type')
            branch_type = form.cleaned_data.get('branch_type')

            # Set staff status based on user_type
            if user_type == 'admin':
                user.is_staff = True
            else:
                user.is_staff = False
            
            user.save()  # Save the updated user status
            
            # Create the related UserProfile with the additional fields
            UserProfile.objects.create(
                user=user,
                user_type=user_type,
                branch_type=branch_type
            )
            
            # Display a success message
            messages.success(request, "Account created successfully!")
            
            # Redirect to the dashboard or another desired location
            return redirect("dashboard")
    else:
        form = CreateUserForm()  # If not a POST request, initialize a new form
    
    # Render the registration template with the form
    context = {'form': form}
    return render(request, 'webapp/register.html', context)



# Login
def my_login(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_staff:
                    return redirect("dashboard")
                else:
                    return redirect("mc_register")
    else:
        form = LoginForm()
    context = {'form':form}
    return render(request, 'webapp/my-login.html', context=context)



# Admin 
@login_required(login_url='my-login')
def admin_dashboard(request):

    user_profile = UserProfile.objects.get(user=request.user)
    branch_type = user_profile.branch_type

    filtered_records = Record.objects.filter(branch=branch_type) 

    context = {
        'branch_type': branch_type,
        'records': filtered_records,
    }

    return render(request, 'webapp/admin/branch/dashboard.html', context)


# Dashboard ADD RECORD
@login_required(login_url='my-login')
def add_record(request):

    user_profile = UserProfile.objects.get(user=request.user)
    form = CreateRecordForm(request.POST or None)
    
    if request.method == "POST" and form.is_valid():
        new_record = form.save(commit=False)
        new_record.branch = user_profile.branch_type 
        new_record.save()
        
        messages.success(request, "Your record was created!")
        return redirect("dashboard")
    
    context = {'form': form}
    return render(request, 'webapp/admin/branch/create-record.html', context)


#Admin EDIT
@login_required(login_url='my-login')
def update_record(request, pk):

    record = Record.objects.get(id=pk)
    form = UpdateRecordForm(instance=record)
    if request.method == 'POST':
        form = UpdateRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, "Your record was updated!")
            return redirect("dashboard")
    context = {'form':form}
    return render(request, 'webapp/admin/branch/update-record.html', context=context)


#Admin Delete
@login_required(login_url='my-login')
def delete_record(request, pk):

    record = Record.objects.get(id=pk)
    record.delete()
    messages.success(request, "Your record was deleted!")
    return redirect("dashboard")


# BIC SETUP
@login_required(login_url='my-login')
def bic_setup(request):

    user_profile = UserProfile.objects.get(user=request.user)
    branch_type = user_profile.branch_type

    filtered_records = BICSetup.objects.filter(branch=branch_type) 

    context = {
        'branch_type': branch_type,
        'bic_setups': filtered_records,
    }

    return render(request, 'webapp/admin/bic/bic_setup.html', context)


@login_required(login_url='my-login')
def bic_setup_create(request):
    
    user_profile = UserProfile.objects.get(user=request.user)
    form = BICSetupForm(request.POST or None)
    
    if request.method == "POST" and form.is_valid():
        new_record = form.save(commit=False)
        new_record.branch = user_profile.branch_type 
        new_record.save()
        
        messages.success(request, "Your record was created!")
        return redirect("bic_setup")
    
    context = {'form': form}
    return render(request, 'webapp/admin/bic/bic_setup_create.html', context)

@login_required(login_url='my-login')
def bic_setup_update(request, bic_setup_id):
    bic_setup = BICSetup.objects.get(pk=bic_setup_id)
    if request.method == 'POST':
        form = BICSetupForm(request.POST, instance=bic_setup)
        if form.is_valid():
            form.save()
            messages.success(request, "Your record was updated!")
            return redirect('bic_setup')
    else:
        form = BICSetupForm(instance=bic_setup)
        
    return render(request, 'webapp/admin/bic/bic_setup_update.html', {'form': form})


@login_required(login_url='my-login')
def bic_setup_delete(request, pk):

    bic_setup = BICSetup.objects.get(id=pk)
    bic_setup.delete()
    messages.success(request, "Your record was deleted!")
    return redirect('bic_setup')











# Cashier Dashboard
@login_required(login_url='my-login')
def cashier_dashboard(request):

    user_profile = UserProfile.objects.get(user=request.user)
    branch_type = user_profile.branch_type

    filtered_records = MCRegister.objects.filter(branch=branch_type) 

    context = {
        'branch_type': branch_type,
        'mc_registers': filtered_records,
    }

    return render(request, 'webapp/cashier/mcregister/cashier.html', context=context)


#cashier add
@login_required(login_url='my-login')
def mc_register_create(request):
    user_profile = UserProfile.objects.get(user=request.user)
    form = MCRegisterForm(request.POST or None)
    
    if request.method == "POST" and form.is_valid():
        new_record = form.save(commit=False)
        new_record.branch = user_profile.branch_type 
        new_record.save()
        
        messages.success(request, "Your record was created!")
        return redirect("mc_register")
    
    context = {'form': form}
    return render(request, 'webapp/cashier/mcregister/mc_create.html', {'form': form})

#edit
@login_required(login_url='my-login')
def mc_register_update(request, mc_register_id):
    mc_register = MCRegister.objects.get(pk=mc_register_id)
    if request.method == 'POST':
        form = MCRegisterForm(request.POST, instance=mc_register)
        if form.is_valid():
            form.save()
            messages.success(request, "Your record was updated!")
            return redirect('mc_register')
    else:
        form = MCRegisterForm(instance=mc_register)
        
    return render(request, 'webapp/cashier/mcregister/mc_update.html', {'form': form})








#PESOT
@login_required(login_url='my-login')
def peso_net(request):

    user_profile = UserProfile.objects.get(user=request.user)
    branch_type = user_profile.branch_type

    filtered_records = PesoNet.objects.filter(branch=branch_type) 

    context = {
        'branch_type': branch_type,
        'peso_nets': filtered_records,
    }

    return render(request, 'webapp/cashier/pesonet/peso_net.html', context=context)


@login_required(login_url='my-login')
def peso_create(request):

    user_profile = UserProfile.objects.get(user=request.user)
    form = PesoNetForm(request.POST or None)
    
    if request.method == "POST" and form.is_valid():
        new_record = form.save(commit=False)
        new_record.branch = user_profile.branch_type
        new_record.save()
        
        messages.success(request, "Your record was created!")
        return redirect("peso_net")
    
    context = {'form': form}
    return render(request, 'webapp/cashier/pesonet/peso_create.html', {'form': form})

#edit
@login_required(login_url='my-login')
def peso_update(request, peso_net_id):
    peso_net = PesoNet.objects.get(pk=peso_net_id)
    if request.method == 'POST':
        form = PesoNetForm(request.POST, instance=peso_net)
        if form.is_valid():
            form.save()
            messages.success(request, "Your record was updated!")
            return redirect('peso_net')
    else:
        form = PesoNetForm(instance=peso_net)
        
    return render(request, 'webapp/cashier/pesonet/peso_update.html', {'form': form})



#BIC cashier
@login_required(login_url='my-login')
def bic_cashier(request):

    user_profile = UserProfile.objects.get(user=request.user)
    branch_type = user_profile.branch_type

    filtered_records = BICSetup.objects.filter(branch=branch_type) 

    context = {
        'branch_type': branch_type,
        'bic_setups': filtered_records,
    }

    return render(request, 'webapp/cashier/bic/bic_cashier.html', context=context)





#logout
def user_logout(request):
    auth.logout(request)
    messages.success(request, "Logout success!")
    return redirect("my-login")





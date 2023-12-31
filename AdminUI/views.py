from datetime import datetime

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.utils.datastructures import MultiValueDictKeyError

from AdminUI.models import DepartmentDB, CourseDB, StudentDB, FacultyEnrollmentDB, JobsDB, JobApplications
from FacultyUI.models import FacultyDB


# Create your views here.
def admin_indexpage(request):
    return render(request, "adminindex.html")


def add_dept(request):
    return render(request, "AddDepartment.html")


def submit_dept(request):
    if request.method == "POST":
        dep = request.POST.get("deptname")
        obj = DepartmentDB(DeptName=dep)
        obj.save()
        return redirect(view_dept)


def view_dept(request):
    data = DepartmentDB.objects.all()
    return render(request, "ViewDepartments.html", {"data": data})


def edit_dept(request, dataid):
    data = DepartmentDB.objects.get(DeptId=dataid)
    return render(request, "EditDepartment.html", {"data": data})


def update_dept(request, dataid):
    if request.method == "POST":
        dep = request.POST.get("deptname")
        DepartmentDB.objects.filter(DeptId=dataid).update(DeptName=dep)
        return redirect(view_dept)


def delete_dept(request, dataid):
    data = DepartmentDB.objects.filter(DeptId=dataid)
    data.delete()
    return redirect(view_dept)


def add_course(request):
    data = DepartmentDB.objects.all()
    return render(request, "AddCourse.html", {'data': data})


def submit_course(request):
    if request.method == "POST":
        course = request.POST.get("coursename")
        dep = request.POST.get("deptname")
        dept_data = DepartmentDB.objects.get(DeptName=dep)
        dept = dept_data.DeptId
        print(dept)
        desc = request.POST.get("course_desc")
        print(dep)
        obj = CourseDB(CourseName=course, DeptId=dept_data, Description=desc)
        obj.save()
        return redirect(add_course)


def view_course(request):
    data = CourseDB.objects.all()
    return render(request, "ViewCourse.html", {"data": data})


def edit_course(request, dataid):
    data = CourseDB.objects.get(CourseId=dataid)
    dep_data = DepartmentDB.objects.all()
    print(data)
    # return redirect(add_course)
    return render(request, "EditCourse.html", {"data": data, "dep_data": dep_data})


def update_course(request, dataid):
    if request.method == "POST":
        course = request.POST.get("coursename")
        dep = request.POST.get("deptname")
        dept_data = DepartmentDB.objects.get(DeptName=dep)
        print(dept_data)
        dept = dept_data.DeptId
        desc = request.POST.get("course_desc")
        CourseDB.objects.filter(CourseId=dataid).update(CourseName=course, DeptId=dept, Description=desc)
        return redirect(view_course)


def delete_course(request, dataid):
    data = CourseDB.objects.filter(id=dataid)
    data.delete()
    return redirect(view_course)


def add_student(request):
    data = CourseDB.objects.all()
    return render(request, "AddStudent.html", {"data": data})


def submit_student(request):
    if request.method == "POST":
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        enid = request.POST.get("enid")
        endate = request.POST.get("endate")
        course = request.POST.get("course")
        course_data = CourseDB.objects.get(CourseName=course)
        coursee = course_data.CourseId
        dob = request.POST.get("dob")
        gender = request.POST.get("gender")
        email = request.POST.get("email")
        contact = request.POST.get("contact")
        address = request.POST.get("address")
        gname = request.POST.get("gname")
        gcontact = request.POST.get("gcontact")
        im = request.FILES['img']
        obj = StudentDB(FirstName=fname, LastName=lname, EnrollmentID=enid, EnrollDate=endate, CourseId=course_data,
                        DateOfBirth=dob, Gender=gender, Email=email, ContactNo=contact, Address=address,
                        GuardianName=gname, GuardianContact=gcontact, Image=im)
        obj.save()
        return redirect(add_student)


def view_students(request):
    data = CourseDB.objects.all()
    stud_data = StudentDB.objects.all()
    years = []
    for i in stud_data:
        year = i.EnrollDate.year
        years.append(year)
    print(years)
    return render(request, "ViewStudents.html", {"data": data, "years": years})


def search_students(request):
    if request.method == "POST":
        course = request.POST.get("course")
        course_data = CourseDB.objects.get(CourseName=course)
        print(course_data)
        cours = course_data.CourseId
        year = request.POST.get("year")
        data = StudentDB.objects.filter(CourseId=cours, EnrollDate__year=year)
        print(course)
        return render(request, "ViewStudentsCourseWise.html", {"data": data, "course": course})


def view_single_student(request, dataid):
    data = StudentDB.objects.get(StudentId=dataid)
    course_data = CourseDB.objects.all()
    return render(request, "ViewSingleStudent.html", {"data": data, "course_data": course_data})


def update_student(request, dataid):
    if request.method == "POST":
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        enid = request.POST.get("enid")
        endate = request.POST.get("endate")
        date_obj = datetime.strptime(endate, "%b. %d, %Y")
        formatted_endate = date_obj.strftime("%Y-%m-%d")
        course = request.POST.get("course")
        course_data = CourseDB.objects.get(CourseName=course)
        coursee = course_data.CourseId
        dob = request.POST.get("dob")
        date_objj = datetime.strptime(dob, "%b. %d, %Y")
        formatted_dob = date_objj.strftime("%Y-%m-%d")
        gender = request.POST.get("gender")
        email = request.POST.get("email")
        contact = request.POST.get("contact")
        address = request.POST.get("address")
        gname = request.POST.get("gname")
        gcontact = request.POST.get("gcontact")
        try:
            im = request.FILES['img']
            fs = FileSystemStorage()
            file = fs.save(im.name, im)
        except MultiValueDictKeyError:
            file = StudentDB.objects.get(StudentId=dataid).Image
        StudentDB.objects.filter(StudentId=dataid).update(FirstName=fname, LastName=lname, EnrollmentID=enid,
                                                          EnrollDate=formatted_endate, CourseId=course_data,
                                                          DateOfBirth=formatted_dob, Gender=gender, Email=email,
                                                          ContactNo=contact, Address=address, GuardianName=gname,
                                                          GuardianContact=gcontact, Image=file)
        return redirect(view_students)


def delete_student(request, dataid):
    data = StudentDB.objects.filter(StudentId=dataid)
    data.delete()
    return redirect(view_students)


def add_faculty(request):
    data = DepartmentDB.objects.all()
    return render(request, "AddFaculty.html", {"data": data})


def submit_faculty(request):
    if request.method == "POST":
        name = request.POST.get("name")
        endate = request.POST.get("date")
        dept = request.POST.get("dept")
        dept_data = DepartmentDB.objects.get(DeptName=dept)
        deptt = dept_data.DeptId
        contact = request.POST.get("contact")
        desig = request.POST.get("designation")
        status = request.POST.get("admin_status")
        if status:
            obj = FacultyEnrollmentDB(Name=name, Joined=endate, DeptId=dept_data, Designation=desig, Contact=contact,
                                      is_admin="True")
            obj.save()
        else:
            obj = FacultyEnrollmentDB(Name=name, Joined=endate, DeptId=dept_data, Designation=desig, Contact=contact,
                                      is_admin="False")
            obj.save()

        return redirect(add_faculty)


def view_faculties(request):
    data = FacultyEnrollmentDB.objects.all()
    return render(request, "ViewFaculties.html", {"data": data})


def search_faculties(request):
    if request.method == "POST":
        dept = request.POST.get("dept")
        dept_data = DepartmentDB.objects.get(DeptName=dept)
        dep = dept_data.DeptId
        data = FacultyEnrollmentDB.objects.filter(DeptId=dep)
        return render(request, "ViewFacultyDepWise.html", {"data": data, "dept": dept})


def view_single_faculty(request, dataid):
    data = FacultyEnrollmentDB.objects.get(FacultyID=dataid)
    try:
        dat = FacultyDB.objects.get(FacultyID=dataid)
    except FacultyDB.DoesNotExist:
        dat = None
    dep_data = DepartmentDB.objects.all()
    return render(request, "ViewSingleFaculty.html", {"data": data, "dep_data": dep_data, "dat": dat})


def admin_signin(request):
    if request.method == "POST":
        uname = request.POST.get('login-username')
        pw = request.POST.get('login-password')
        # print(uname)
        # print(pw)
        if User.objects.filter(username__contains=uname).exists():

            user = authenticate(username=uname, password=pw)
            if user is not None:
                login(request, user)
                request.session['username'] = uname
                request.session['password'] = pw
                # messages.success(request, "Logined successfully")
                return redirect(admin_indexpage)
            else:
                # messages.error(request, "Check the credentials")
                return redirect(admin_login)
        elif User.objects.filter(username=uname, password=pw).exists():
            request.session['username'] = uname
            request.session['password'] = pw
            # messages.success(request, "Logined successfully")
            return redirect(admin_indexpage)
        else:
            # messages.error(request, "Check the credentials")
            return redirect(admin_login)


def admin_login(request):
    return render(request, "AdminLogin.html")


def add_job(request):
    return render(request, "AddJobOpenings.html")


def job_save(request):
    if request.method == "POST":
        title = request.POST.get("title")
        company = request.POST.get("cname")
        location = request.POST.get("location")
        qualification = request.POST.get("qualification")
        description = request.POST.get("description")
        email = request.POST.get("email")
        obj = JobsDB(Title=title, Company=company, Location=location, Qualification=qualification,
                     Description=description, Email=email)
        obj.save()
        return redirect(add_job)


def view_jobs(request):
    job_data = JobsDB.objects.all()
    return render(request, "ViewJobs.html", {'job_data': job_data})


def job_delete(request, data_id):
    job_data = JobsDB.objects.filter(JobId=data_id)
    job_data.delete()
    return redirect(view_jobs)


def view_job_single(request, data_id):
    job_data = JobsDB.objects.get(JobId=data_id)
    return render(request, "ViewJobSingle.html", {'job_data': job_data})


def update_job(request, job_id):
    if request.method == "POST":
        title = request.POST.get("title")
        company = request.POST.get("cname")
        location = request.POST.get("location")
        qualification = request.POST.get("qualification")
        description = request.POST.get("description")
        email = request.POST.get("email")
        JobsDB.objects.filter(JobId=job_id).update(Title=title, Company=company, Location=location,
                                                   Qualification=qualification,
                                                   Description=description, Email=email)
        return redirect(view_jobs)


def job_applications(request, job_id):
    job_data = JobsDB.objects.get(JobId=job_id)
    applications = JobApplications.objects.filter(JobId=job_data)
    return render(request, "JobApplications.html", {'applications': applications})


def resume_download(request, stud_id, job_id):
    data = JobApplications.objects.filter(JobId=job_id)
    pdf_file = get_object_or_404(data, StudentId=stud_id)
    response = FileResponse(pdf_file.Resume, as_attachment=True)
    return response



def application_single(request, dataid):
    data = StudentDB.objects.get(StudentId=dataid)
    course_data = CourseDB.objects.all()
    return render(request, "ApplicationDetail.html", {"data": data, "course_data": course_data})


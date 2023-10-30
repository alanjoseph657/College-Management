from django.db import models


# Create your models here.


class DepartmentDB(models.Model):
    DeptId = models.AutoField(primary_key=True)
    DeptName = models.CharField(max_length=100)


class CourseDB(models.Model):
    CourseId = models.AutoField(primary_key=True)
    CourseName = models.CharField(max_length=20)
    DeptId = models.ForeignKey(DepartmentDB, on_delete=models.CASCADE)
    Description = models.TextField()


class StudentDB(models.Model):
    StudentId = models.AutoField(primary_key=True)
    FirstName = models.CharField(max_length=200, null=True, blank=True)
    LastName = models.CharField(max_length=200, null=True, blank=True)
    DateOfBirth = models.DateField(null=True, blank=True)
    Gender = models.CharField(max_length=1, null=True, blank=True)
    Email = models.EmailField(max_length=200, null=True, blank=True)
    ContactNo = models.IntegerField(blank=True, null=True)
    Address = models.TextField(null=True, blank=True)
    GuardianName = models.CharField(max_length=200, null=True, blank=True)
    GuardianContact = models.IntegerField(null=True, blank=True)
    Image = models.ImageField(upload_to="StudentsImage")
    EnrollmentID = models.CharField(max_length=20, null=True, blank=True)
    EnrollDate = models.DateField(null=True, blank=True)
    CourseId = models.ForeignKey(CourseDB, on_delete=models.CASCADE, null=True, blank=True)


class FacultyEnrollmentDB(models.Model):
    FacultyID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=50)
    Joined = models.DateField(null=True, blank=True)
    DeptId = models.ForeignKey(DepartmentDB, on_delete=models.CASCADE)
    Designation = models.CharField(max_length=100, null=True, blank=True)
    Contact = models.CharField(max_length=20, null=True, blank=True)
    is_admin = models.BooleanField(default=False, null=True, blank=True)


class JobsDB(models.Model):
    JobId = models.AutoField(primary_key=True)
    Title = models.CharField(max_length=100,null=True,blank=True)
    Company = models.CharField(max_length=100,null=True,blank=True)
    Location = models.CharField(max_length=100,null=True,blank=True)
    Qualification = models.CharField(max_length=500,null=True,blank=True)
    Description = models.CharField(max_length=1000,null=True,blank=True)
    Email = models.EmailField(max_length=100,null=True,blank=True)


class JobApplications(models.Model):
    JobId = models.ForeignKey(JobsDB, on_delete=models.CASCADE)
    StudentId = models.ForeignKey(StudentDB, on_delete=models.CASCADE)
    Resume = models.FileField(upload_to="Resume")
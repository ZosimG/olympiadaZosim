from schools.models import Subdivision, School
from users.models import Employee, Person, ROLES
from .models import Student, Country, Application, sex
from olymp.models import Olympiada
from openpyxl import load_workbook
from openpyxl.styles import Border, Side, Alignment, Font

class ApplicationGen():
    wb_font = Font(name='Times New Roman', size=11, color='00000000')
    wb_border = Border(left=Side(style='thin', color='00000000'), right=Side(style='thin', color='00000000'),
                       top=Side(style='thin', color='00000000'), bottom=Side(style='thin', color='00000000'))
    wb_alignment = Alignment(horizontal='center', vertical='center', wrapText=True)

    @classmethod
    def generate(cls, olymp_id):
        wb = load_workbook(filename="./excel_templates/app_template.xlsx")
        ws = wb.active
        application_list = Application.objects.filter(olymp__id=olymp_id)
        cls.generate_application_file(ws, application_list)
        return wb

    @classmethod
    def generate_application_file(cls, worksheet, application_list):
        row = 5

        for i, application in enumerate(application_list):
            cls.fill_application_info(row+i, application, worksheet)
            cls.fill_school_info(row+i, application.school, worksheet)
            cls.fill_subdivision_info(row+i, application.subdivision, worksheet)
            cls.fill_student_info(row+i, application.student, worksheet)
            cls.fill_employee_info(row+i, application.employee, worksheet)

            for j in range(0, 14):
                worksheet[chr(ord('A') + j) + str(row + i)].font = cls.wb_font
                worksheet[chr(ord('A') + j) + str(row + i)].border = cls.wb_border
                worksheet[chr(ord('A') + j) + str(row + i)].alignment = cls.wb_alignment

                worksheet.row_dimensions[row+i].height = 36.8511

            worksheet[chr(ord('A')) + str(row + i)] = str(i+1)

    @classmethod
    def fill_application_info(cls, row, application, worksheet):
        participate = application.participate
        worksheet[chr(ord('A')+11) + str(row)] = str(participate)

    @classmethod
    def fill_school_info(cls, row, school, worksheet):
        school_name = school.school_name
        worksheet[chr(ord('A') + 9) + str(row)] = str(school_name)

    @classmethod
    def fill_subdivision_info(cls, row, subdivision, worksheet):
        subdivision_name = subdivision.subdivision_name
        worksheet[chr(ord('A') + 8) + str(row)] = str(subdivision_name)

    @classmethod
    def fill_student_info(cls, row, student, worksheet):
        student_name_full = student.name.split()
        worksheet[chr(ord('A') + 1) + str(row)] = str(student_name_full[0])
        worksheet[chr(ord('A') + 2) + str(row)] = str(student_name_full[1])
        if len(student_name_full) == 3:
            worksheet[chr(ord('A') + 3) + str(row)] = str(student_name_full[2])

        student_sex = student.sex
        worksheet[chr(ord('A') + 4) + str(row)] = str(sex[student_sex][1][0])

        student_birthday = student.birthday
        worksheet[chr(ord('A') + 5) + str(row)] = str(student_birthday)

        student_country = student.country.country_name
        worksheet[chr(ord('A') + 6) + str(row)] = str(student_country)

        student_special_needs = student.special_needs
        worksheet[chr(ord('A') + 7) + str(row)] = "Да" if student_special_needs else "Нет"

        student_course = student.course_study
        worksheet[chr(ord('A') + 10) + str(row)] = str(student_course)

        student_phone = student.contact_phone
        worksheet[chr(ord('A') + 13) + str(row)] = str(student_phone)

    @classmethod
    def fill_employee_info(cls, row, employee, worksheet):
        employee_name = employee.name
        worksheet[chr(ord('A') + 12) + str(row)] = str(employee_name)
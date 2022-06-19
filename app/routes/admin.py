from app import app, db, UPLOAD_FOLDER
from flask import render_template, request, redirect
from app.models import User, Course, Module, Class
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from secrets import token_hex
from datetime import datetime
import os


message = [{"message": "A entrada de usuário viola nossos padrões de segurança", "error":True},  # Mensagem para possível SQL Injection
            {"message": "Login ou senha não conferem.", "error": True},  # Mensagem para login ou senha inválidos
            {"message": "Nome, e-mail e login devem ter entre 8 e 45 caracteres", "error": True},  # Entrada inválida
            {"message": "CPF inválido", "error": True},  # CPF inválido
            {"message": "Senha inválida", "error": True},  # CPF inválido
            {"message": "Já existe um usuário com o mesmo e-mail, CPF ou login", "error": True},  # CPF inválido
            {"error": False},  # Caso login e senha estejam ok, error será False
            {"message": "Entrada inválida", "error": True}]  # Entrada inválida

@app.route('/admin-panel')
@login_required
def admin_panel():
    try:
        if current_user.is_admin == False:
            return redirect('/panel')
    except AttributeError:
        return render_template("login.html", message=message[6])
    except:
        return 'Erro Inesperado'
    
    return render_template('admin_panel.html')


@app.route('/admin-panel/courses')
@login_required
def adm_courses():
    try:
        if current_user.is_admin == False:
            return redirect('/panel')
    except AttributeError:
        return render_template("login.html", message=message[6])
    except:
        return 'Erro Inesperado'
    
    courses = Course.query.all()
    modules = Module.query.all()
    classes = Class.query.all()

    return render_template('courses_adm.html', courses=courses, modules=modules, classes=classes)


@app.route('/admin-panel/courses/add-course', methods=['GET', 'POST'])
@login_required
def add_course():
    if request.method == 'POST':
        name = request.form.get('name')
        price = request.form.get('price')
        level = request.form.get('flexRadioDefault')
        description = request.form.get('description')
        is_active = False
        if request.form.get('is_active'):
            is_active = True
        video_1 = request.form.get('video_1')
        
        image_1 = request.files.get('image_1')
        image_2 = request.files.get('image_2')

        if image_1:
            image_1_name = token_hex(20) + '.png'  # Criando o nome da imagem em um token hexadecimal
            file_path = os.path.join(UPLOAD_FOLDER, image_1_name)
            image_1.save(file_path)
        if image_2:
            image_2_name = token_hex(20) + '.png'  # Criando o nome da imagem em um token hexadecimal
            file_path = os.path.join(UPLOAD_FOLDER, image_2_name)
            image_2.save(file_path)

        
        datetime_now = datetime.utcnow()
            
        course = Course(name, price, description, level, datetime_now, is_active, image_1_name, image_2_name, video_1)
        db.session.add(course)
        db.session.commit()

        return redirect('/admin-panel/courses')

    else:

        return render_template('add_course.html', message=message[6])


@app.route('/admin-panel/courses/add-module', methods=['GET', 'POST'])
@login_required
def add_module():
    
    if request.method == 'POST':            
        if request.form.get('courseofmoduleid') and request.form.get('courseofmodulename'):
            courseofmodule = {'id': request.form.get('courseofmoduleid'), 'name': request.form.get('courseofmodulename')}
            return render_template('add_module.html', course=courseofmodule, message=message[6])

        course_id = request.form.get('course_id')
        name = request.form.get('name')
        description = request.form.get('description')
        teacher = request.form.get('teacher')
        image_1 = request.files.get('image_1')
        video_1 = request.form.get('video_1')

        for input in [course_id, name, description, teacher, video_1]:
            if input == None:
                pass
        
        if image_1:
            image_1_name = token_hex(20) + '.png'
            file_path = os.path.join(UPLOAD_FOLDER, image_1_name)
            image_1.save(file_path)
        

        # Query para pegar index
        index = 1
        modules = Module.query.filter(Module.course_id == course_id).all()
        index_list = []
        if modules != None:
            if len(modules) > 0:
                for module in modules:
                    index_list.append(module.index)
                index = max(index_list) + 1
        
        
        datetime_now = datetime.utcnow()
        
        module = Module(course_id, name, description, teacher, datetime_now, image_1_name, video_1, index)
        db.session.add(module)
        db.session.commit()

        return redirect('/admin-panel/courses')
        

    else:

        return redirect('/admin-panel/courses')


@app.route('/admin-panel/courses/add-class', methods=['GET', 'POST'])
@login_required
def add_class():
    if request.method == 'POST':
        if request.form.get('courseofmoduleid') and request.form.get('courseofmodulename') and request.form.get('moduleofclassid') and request.form.get('moduleofclassname'):
            courseofmodule = {'id': request.form.get('courseofmoduleid'), 'name': request.form.get('courseofmodulename')}
            moduleofclass = {'id': request.form.get('moduleofclassid'), 'name': request.form.get('moduleofclassname')}
            return render_template('add_class.html', course=courseofmodule, module=moduleofclass, message=message[6])

        course_name = request.form.get('course_name')
        module_name = request.form.get('module_name')
        course_id = request.form.get('course_id')
        module_id = request.form.get('module_id')
        name = request.form.get('name')
        description = request.form.get('description')
        teacher = request.form.get('teacher')
        hours = request.form.get('hours')
        minutes = request.form.get('minutes')
        image_1 = request.files.get('image_1')
        video_1 = request.form.get('video_1')

        # Verificando entradas de usuário
        
        # Arrays para render_template
        courseofmodule = {'id': course_id, 'name': course_name}
        moduleofclass = {'id': module_id, 'name': module_name}


        if len(name) > 50 or len(teacher) > 50:
            return render_template('add_class.html', course=courseofmodule, module=moduleofclass, message=message[7])
        if len(description) > 200:
            return render_template('add_class.html', course=courseofmodule, module=moduleofclass, message=message[7])
        if len(video_1) > 600:
            return render_template('add_class.html', course=courseofmodule, module=moduleofclass, message=message[7])
        

        # Formatando as entradas para inserir no banco de dados

        decimal_duration = time_to_decimal(hours, minutes)
        # Inserindo imagem no banco de dados
        if image_1:
            image_1_name = token_hex(20) + '.png'
            file_path = os.path.join(UPLOAD_FOLDER, image_1_name)
            image_1.save(file_path)

        # Query para pegar index
        index = 1
        classes = Class.query.filter((Class.course_id == course_id) & (Class.module_id == module_id)).all()
        index_list = []
        if classes != None:
            if len(classes) > 0:
                for classs in classes:
                    index_list.append(classs.index)
                index = max(index_list) + 1

        
        datetime_now = datetime.utcnow()

        # Adicionando aula ao banco de dados
        class_add = Class(module_id, course_id, name, str(decimal_duration), teacher, datetime_now, description, image_1_name, video_1, index)
        db.session.add(class_add)
        db.session.commit()

        # Alterando last_update e workload da tabela courses
        course_alter = Course.query.filter(Course.id == course_id).first()
        course_workload = str(round((float(course_alter.workload) + decimal_duration), 2))
        course_alter.workload = course_workload
        course_alter.last_update = datetime_now
        db.session.add(course_alter)
        db.session.commit()

        # Alterando last_update e workload da tabela modules
        module_alter = Module.query.filter(Module.id == module_id).first()
        module_workload = str(round((float(module_alter.workload) + decimal_duration), 2))
        module_alter.workload = module_workload
        module_alter.last_update = datetime_now
        db.session.add(module_alter)
        db.session.commit()

        return redirect('/admin-panel/courses')

    else:

        return redirect('/admin-panel/courses')


@app.route('/admin-panel/courses/delete', methods=['GET', 'POST'])
@login_required
def delete():
    if request.method == 'POST':
        class_del = request.form.get('class_del_classid')
        module_del = request.form.get('module_del_moduleid')
        course_del = request.form.get('course_del_courseid')

        if class_del:
            classs = Class.query.filter(Class.id == class_del).all()
            if classs:
                for clas in classs:  # O nome 'class' foi escrito com um 's' a mais porque o original é um termo reservado por Python
                    module_alter_workload = Module.query.filter(Module.id == clas.module_id).first()
                    module_workload = 0
                    if float(module_alter_workload.workload) > float(clas.duration):
                        module_workload = float(module_alter_workload.workload) - float(clas.duration)
                    module_alter_workload.workload = str(module_workload)
                    db.session.add(module_alter_workload)
                    db.session.commit()

                    course_alter_workload = Course.query.filter(Course.id == clas.course_id).first()
                    course_workload = 0
                    if float(course_alter_workload.workload) > float(clas.duration):
                        course_workload = float(course_alter_workload.workload) - float(clas.duration)
                    course_alter_workload.workload = str(course_workload)
                    db.session.add(course_alter_workload)
                    db.session.commit()

                    db.session.delete(clas)
                    db.session.commit()

        if module_del:
            # Para deletar o módulo, primeiro tem que deletar as aulas do módulo por causa das ForeignKeys
            modules = Module.query.filter(Module.id == module_del).all()
            classes_for_del = Class.query.filter(Class.module_id == module_del).all()
            if classes_for_del:
                for clas in classes_for_del:
                    db.session.delete(clas)
                    db.session.commit()
            if modules:
                for module in modules:
                    course_alter_workload = Course.query.filter(Course.id == module.course_id).first()
                    workload = 0
                    if float(course_alter_workload.workload) - float(module.workload):
                        workload = float(course_alter_workload.workload) - float(module.workload)
                    course_alter_workload.workload = str(workload)
                    db.session.add(course_alter_workload)
                    db.session.commit()

                    db.session.delete(module)
                    db.session.commit()


        if course_del:
            # Para deletar o curso, primeiro tem que deletar as aulas e módulos, por causa das ForeignKeys
            courses = Course.query.filter(Course.id == course_del).all()
            modules = Module.query.filter(Module.id == module_del).all()
            classes_for_del = Class.query.filter(Class.module_id == module_del).all()
            if classes_for_del:
                for clas in classes_for_del:
                    db.session.delete(clas)
                    db.session.commit()
            if modules:
                for module in modules:
                    db.session.delete(module)
                    db.session.commit()
            if courses:
                for course in courses:
                    db.session.delete(course)
                    db.session.commit()

        return redirect("/admin-panel/courses")

    else:

        return redirect("/admin-panel/courses")


@app.route('/admin-panel/courses/edit', methods=['GET', 'POST'])
@login_required
def edit():
    if request.method == 'POST':
        
        # Os inputs 'edit' identificam se a form vem da página de cursos do botão editar
        class_edit = request.form.get('class_edit')
        module_edit = request.form.get('module_edit')
        course_edit = request.form.get('course_edit')

        if class_edit:
            class_data = Class.query.filter(Class.id == class_edit).first()
            temp = decimal_to_time(class_data.duration)
            class_data.duration = temp
            data = {'type':'class', 'type_ptbr':'Aula'}
            return render_template('/edit.html', message=message[6], data_db=class_data, data=data)
        if module_edit:
            module_data = Module.query.filter(Module.id == module_edit).first()
            data = {'type':'module', 'type_ptbr':'Módulo'}
            return render_template('/edit.html', message=message[6], data_db=module_data, data=data)
        if course_edit:
            course_data = Course.query.filter(Course.id == course_edit).first()
            data = {'type':'course', 'type_ptbr':'Curso'}
            return render_template('/edit.html', message=message[6], data_db=course_data, data=data)

        # O input type define o tipo de dado a ser alterado (curso, módulo ou aula)
        edit_type = request.form.get('type')

        if edit_type == 'course':
            course_data_columns = ['name', 'price', 'flexRadioDefault', 'description', 'is_active', 'video_1']
            course_file_columns = ['image_1', 'image_2']

            course_data_query = Course.query.filter(Course.id == request.form.get('id')).first()

            course_data_query.last_update = datetime.utcnow()
            course_data_query.is_active = False

            for column in course_data_columns:
                form_data = request.form.get(column)
                if form_data:
                    if column == 'name':
                        course_data_query.name = form_data
                    elif column == 'price':
                        course_data_query.price = form_data
                    elif column == 'flexRadioDefault':
                        course_data_query.level = form_data
                    elif column == 'description':
                        course_data_query.description = form_data
                    elif column == 'is_active':
                        course_data_query.is_active = True
                    elif column == 'video_1':
                        course_data_query.video_1 = form_data
            
            for column in course_file_columns:
                form_file = request.files.get(column)
                if form_file:
                    if column == 'image_1':
                        try:
                            os.remove(f'app/static/media/{course_data_query.banner_1}')
                            file_path = os.path.join(UPLOAD_FOLDER, course_data_query.banner_1)
                            form_file.save(file_path)
                        except:
                            return 'Erro ao salvar arquivo de imagem'
                    if column == 'image_2':
                        try:
                            os.remove(f'app/static/media/{course_data_query.banner_2}')
                            file_path = os.path.join(UPLOAD_FOLDER, course_data_query.banner_2)
                            form_file.save(file_path)
                        except:
                            return 'Erro ao salvar arquivo de imagem'
            
            db.session.add(course_data_query)
            db.session.commit()

            return redirect('/admin-panel/courses')


        if edit_type == 'module':
            module_data_columns = ['name', 'description', 'teacher', 'video_1']

            module_data_query = Module.query.filter(Module.id == request.form.get('id')).first()
            
            # Atualizando o last_update do curso
            course_of_module = Course.query.filter(Course.id == module_data_query.course_id).first()
            course_of_module.last_update = datetime.utcnow()
            db.session.add(course_of_module)
            db.session.commit()

            module_data_query.last_update = datetime.utcnow()

            for column in module_data_columns:
                form_data = request.form.get(column)
                if form_data:
                    if column == 'name':
                        module_data_query.name = form_data
                    if column == 'description':
                        module_data_query.description = form_data
                    if column == 'teacher':
                        module_data_query.teacher = form_data
                    if column == 'video_1':
                        module_data_query.video_1 = form_data

            form_file = request.files.get('image_1')
            if form_file:
                try:
                    os.remove(f'app/static/media/{module_data_query.banner_1}')
                    file_path = os.path.join(UPLOAD_FOLDER, module_data_query.banner_1)
                    form_file.save(file_path)
                except:
                    return 'Erro ao salvar arquivo de imagem'

            db.session.add(module_data_query)
            db.session.commit()

            return redirect('/admin-panel/courses')            

        if edit_type == 'class':
            class_data_columns = ['name', 'description', 'teacher', 'video_1']

            module_data_query = Module.query.filter(Module.id == request.form.get('id')).first()
            
            # Atualizando o last_update do curso
            course_of_module = Course.query.filter(Course.id == module_data_query.course_id).first()
            course_of_module.last_update = datetime.utcnow()
            db.session.add(course_of_module)
            db.session.commit()

            module_data_query.last_update = datetime.utcnow()


        return redirect('/admin-panel/courses')

        
    else:

        return redirect('admin-panel/courses')

def time_to_decimal(hours, minutes):
    decimal_minutes = str(round((minutes * 10) / 6))
    if len(decimal_minutes) < 2:
        temp = f"0{decimal_minutes}"
        decimal_minutes = temp
    
            
    return float(f"{str(hours)}.{decimal_minutes}")

def decimal_to_time(time_in_decimal):
    
    dot_check = False
    integer_list = []
    decimal_list = []
    for caractere in time_in_decimal:
        if caractere == '.':
            dot_check = True
            continue
        if dot_check == False:
            integer_list.append(caractere)
        else:
            decimal_list.append(caractere)

    minutes = str(round(float(f'0.{"".join(decimal_list)}') * 60))

    return (f'{"".join(integer_list)} horas e {minutes} minutos')
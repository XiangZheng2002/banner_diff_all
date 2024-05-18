import os
import shutil
import math
import sys
import json
import ast

sys.path.append('/usr/src/app/backend')
sys.stdout = sys.stderr
from flask import Flask, request, jsonify, send_from_directory, session, url_for
from flask_cors import CORS
from collage_diffusion.collage_generation import collage_process
from model import db, OriginalImage, User, ProcessedImage, Project, OutputImage, Image_Type, Image_Style
from flask_migrate import Migrate
from PIL import Image
from sqlalchemy import or_
from celery import Celery
from celery.result import AsyncResult
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp', 'bmp'}  # 允许上传的图片格式
app = Flask(__name__, static_url_path="/backend/static")
app.config['STATIC_FOLDER'] = 'backend/static'
app.config['PROCESSED_FOLDER'] = app.config['STATIC_FOLDER'] + '/' + 'processed'
app.config['OUTPUT_FOLDER'] = app.config['STATIC_FOLDER'] + '/' + 'output'
app.config['INPUT_FOLDER'] = app.config['STATIC_FOLDER'] + '/' + 'input'
app.config['AVATAR_FOLDER'] = app.config['STATIC_FOLDER'] + '/' + 'avatar'  # 头像存放路径
app.config['TEMP_INPUT_FOLDER'] = app.config['STATIC_FOLDER'] + '/' + 'tmp_input'
app.config['TEMP_PROCESS_FOLDER'] = app.config['STATIC_FOLDER'] + '/' + 'tmp_process'
app.config['TEMP_OUTPUT_FOLDER'] = app.config['STATIC_FOLDER'] + '/' + 'tmp_output'
app.config['DEFAULT_AVATAR_URL'] = app.config['AVATAR_FOLDER'] + "/1.jpg"  # 默认头像
app.config['THUMBNAIL_FOLDER'] = app.config['STATIC_FOLDER'] + '/' + 'thumbnail'  # 工程缩略图保存路径
app.config['TEMP_INPUT_IMAGE'] = app.config['STATIC_FOLDER'] + '/' + 'tmp_raw'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'

app.config['SECRET_KEY'] = os.urandom(24)
app.config['ADMIN_ID'] = 1
app.app_context().push()

# 初始化celery 异步处理
app.config['CELERY_BROKER_URL'] = 'redis://redis:6379/1'
app.config['CELERY_RESULT_BACKEND'] = 'redis://redis:6379'
CORS(app)
# 连接mysql数据库
# HOSTNAME = 'host.docker.internal'  # mysql:docker
# PORT = 3306
HOSTNAME = 'host.docker.internal'
PORT = 3306
DATABASE = 'banner_diffusion'
# USERNAME = 'admin'
# PASSWORD = 'admin'
USERNAME = 'root'
PASSWORD = 'root'
DB_URL = 'mysql+pymysql://{}:{}@{}:{}/{}'.format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
# 是否追踪数据库修改，一般不开启, 会影响性能
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# 是否显示底层执行的SQL语句
app.config['SQLALCHEMY_ECHO'] = True

# 初始化数据库
db.init_app(app)
# migrate = Migrate(app, db)  # 初始化迁移

db.session.expire_all()


def make_celery(app):  # 将flask app当作参数传递给celery 的make函数
    celery_app = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'],
                        backend=app.config['CELERY_RESULT_BACKEND'])
    celery_app.conf.update(app.config)
    TaskBase = celery_app.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery_app.Task = ContextTask
    return celery_app


celery = make_celery(app)


def restful_result(code, message="", data=None):
    return jsonify({"code": code, "message": message, "data": data or {}})


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    # Use os.getenv("key") to get environment variables
    # 此处获取环境变量
    # 相关环境变量配置后面会说
    app_name = os.getenv("APP_NAME")

    if app_name:
        return f"Hello from {app_name} running in a Docker container behind Nginx!"
    return "Hello from Flask"


@app.route('/testsql', methods=['POST'])
def testsql():
    # image = OriginalImage(img_url='/input/dog.jpg', name="dog", style="可爱风", type="鞋子")
    # db.session.add(image)
    # db.session.commit()
    # image = OriginalImage(img_url='/input/OIP-C.jpg', name="OIP-C", style="商务风", type="装饰")
    # db.session.add(image)
    # db.session.commit()
    user = User(name="admin", password="admin", avatar_url=app.config['DEFAULT_AVATAR_URL'], is_admin=1)
    db.session.add(user)
    db.session.commit()
    return 'commit success'


# 根据style和type从数据库中读取原始素材
@app.route('/get_files', methods=['GET'])
def get_files():
    user_id = request.args.get('user_id')
    current_id = session.get('user_id')
    use_admin = request.args.get('use_admin')
    if not use_admin:
        use_admin = 0
    if not current_id:
        return restful_result(401, '您尚未登录')
    if not int(user_id) == current_id:
        return restful_result(403, '您无权查看该用户的上传素材信息')
    styles = request.args.getlist("style")
    types = request.args.getlist("type")
    categories = request.args.getlist("category")
    db.session.commit()
    if int(use_admin):
        images = db.session.query(OriginalImage).join(Image_Style).join(Image_Type).filter(
            OriginalImage.user_id == app.config['ADMIN_ID'])
    else:
        images = db.session.query(OriginalImage).join(Image_Style).join(Image_Type).filter(
            or_(OriginalImage.user_id == user_id))

    style_filters = [Image_Style.style.in_(styles)] if styles else []
    type_filters = [Image_Type.type.in_(types)] if types else []
    category_filters = [Image_Type.category.in_(categories)] if categories else []

    filtered_images = images.filter(or_(or_(*style_filters), or_(*type_filters), or_(*category_filters))).all()

    images = [{"id": image.id, "img_url": image.img_url, "name": image.name, "last_mod": image.last_mod} for image in
              filtered_images]
    return restful_result(200, '列出所有符合要求的素材', {'images': images})


# 从图片id获取原始素材数据
@app.route('/image', methods=['GET'])
def image():
    user_id = request.args.get('user_id')
    current_id = session.get('user_id')
    if not current_id:
        return restful_result(401, '您尚未登录')
    if not int(user_id) == current_id:
        return restful_result(403, '您无权查看该用户的上传素材信息')
    img_id = request.args.get("img_id")
    db.session.commit()
    image = OriginalImage.query.filter_by(id=img_id).first()
    if not image:
        return restful_result(400, 'id为{}的原始素材不存在'.format(img_id))
    if image.user_id != int(user_id):
        return restful_result(403, 'id为{}的原始素材不属于您的账户，您无法操作'.format(img_id))
    return restful_result(200, '列出id为{}的原始素材'.format(img_id), {'image_url': image.img_url})


# 图片生成任务
@celery.task(name='main.task', bind=True)
def task(self, user_id, project_id, result_count=3):
    db.session.commit()
    project = Project.query.filter_by(id=project_id).first()
    x = project.width
    y = project.height
    processed_images = ProcessedImage.query.filter_by(project_id=project_id).all()
    if os.path.exists(app.config['TEMP_INPUT_FOLDER']):
        shutil.rmtree(app.config['TEMP_INPUT_FOLDER'])
    os.mkdir(app.config['TEMP_INPUT_FOLDER'])
    if os.path.exists(app.config['TEMP_OUTPUT_FOLDER']):
        shutil.rmtree(app.config['TEMP_OUTPUT_FOLDER'])
    os.mkdir(app.config['TEMP_OUTPUT_FOLDER'])
    n = len(processed_images)
    w_poss = [0 for _ in range(n)]
    w_negs = [0 for _ in range(n)]
    t_is = [0 for _ in range(n)]
    for processed_image in processed_images:
        db.session.commit()
        original_image = OriginalImage.query.filter_by(id=processed_image.img_id).first()
        img_url = original_image.img_url
        name = original_image.name
        layer = int(processed_image.layer)
        pos_x = processed_image.pos_x
        pos_y = processed_image.pos_y
        rotate_deg = processed_image.rotate_deg
        width = processed_image.width
        height = processed_image.height
        w_pos = float(processed_image.w_pos)
        w_neg = float(processed_image.w_neg)
        t_i = float(processed_image.t_i)
        _x, _y, _w, _h, _r = map(
            lambda x: math.ceil(x),
            (
                pos_x,
                pos_y,
                width,
                height,
                rotate_deg,
            ),
        )  # 浮点数转换为整数
        file = Image.open(img_url)
        file = file.resize((_w, _h)).rotate(_r)  # 放缩和旋转
        # 获取到所有信息，进行处理
        canvas = Image.new('RGBA', (int(x), int(y)), (255, 255, 255, 0))
        canvas.paste(file, (_x, _y))
        filename = project_id + "_" + str(layer) + "_" + name + ".png"
        canvas.save(app.config['TEMP_INPUT_FOLDER'] + "/" + filename)
        print("layer #: " + str(processed_image.layer))
        w_poss[layer] = w_pos
        w_negs[layer] = w_neg
        t_is[layer] = t_i
    input_temp_dir = app.config['TEMP_INPUT_FOLDER']  # 模型的输入暂时放到这里
    process_temp_dir = app.config['TEMP_PROCESS_FOLDER']  # 模型在处理前的临时输入，具体不用管
    output_temp_dir = app.config['TEMP_OUTPUT_FOLDER']  # 模型的输出暂时放到这里，然后再统一存到output里面
    output_dir = app.config['OUTPUT_FOLDER']
    collage_process(input_temp_dir, process_temp_dir, output_temp_dir, project.id, project.name, w_poss, w_negs, t_is,
                    result_count)
    # invert_images(w_poss, w_negs, t_is, project_id, input_temp_dir, output_temp_dir, result_count)  # 模型生成的函数，之后将替换
    output_files = os.listdir(output_temp_dir)
    output_img_urls = []
    for output_file in output_files:
        img = Image.open(output_temp_dir + "/" + output_file)
        output_url = output_dir + "/" + output_file
        img.save(output_url)
        output_img_urls.append(output_url)
        new_output = OutputImage(name=output_file[:output_file.rindex('.')], img_url=output_dir + "/" + output_file,
                                 project_id=project_id, user_id=user_id)
        db.session.add(new_output)
        db.session.commit()
    return output_img_urls, project.name


# 用户点击生成以后，将前端的数据返回后端，后端运行模型生成结果，返回生成结果的url给前端
@app.route('/process', methods=['POST'])
def process():
    user_id = request.args.get('user_id')
    project_id = request.args.get('project_id')
    current_id = session.get('user_id')
    if not current_id:
        return restful_result(401, "您尚未登录")
    if not int(user_id) == current_id:
        return restful_result(403, "您无权处理该用户的工程")
    db.session.commit()
    user = db.session.query(User).join(Project).filter(User.id == user_id).first()
    if not user:
        return restful_result(403, "此工程id不属于此用户，您无权操作")
    result_count = int(request.args.get('result_count'))
    task_ = task.delay(user_id, project_id, result_count)
    return restful_result(200, "海报生成已开始", {'task_id': task_.id})


@app.route("/process_result", methods=['GET'])
def process_result():
    task_id = request.args.get('task_id')
    # 根据任务ID获取任务结果
    task = AsyncResult(id=task_id, app=celery)
    if task.state == 'PENDING':
        return restful_result(503, "正在生成中", {"status": "PROCESSING"})
    elif task.state == 'FAILURE':
        return restful_result(503, "生成任务出现错误", {"status": "FAILURE", "error": str(task.info)})
    elif task.state != 'SUCCESS':
        return restful_result(503, "生成任务还未结束", {"status": "PROCESSING"})
    else:
        return restful_result(200, "生成已完成",
                              {"status": "SUCCESS", "image_urls": task.result[0], "project_name": task.result[1]})


# 后端将输出的图片发送到前端
@app.route('/output/<filename>', methods=['GET'])
def output_file(filename):
    return send_from_directory(app.config['OUTPUT_FOLDER'], filename)  # 从后端图片目录中读取并显示图片


# 用户登录
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data['username']
    password = data['password']
    db.session.commit()
    user = User.query.filter_by(name=username).first()
    if user:
        if user.password == password:
            session['user_id'] = user.id
            return restful_result(200, "登录成功", {'user_id': user.id, 'username': user.name,
                                                    'is_admin': user.is_admin, 'avatar_url': user.avatar_url})
        else:
            return restful_result(401, "登录失败，密码不正确")
    else:
        return restful_result(401, "登录失败，用户名不存在")


# 用户注册
@app.route('/register', methods=['POST'])
def register():
    avatar = request.files.get('avatar', default=None)  # 用户上传头像
    username = request.form.get('username')
    password = request.form.get('password')
    if not username:
        return restful_result(400, "用户名不能为空")
    if username == 'admin':
        return restful_result(400, "不能以admin作为用户名")
    if not password:
        return restful_result(400, "密码不能为空")

    db.session.commit()
    existing_user = User.query.filter_by(name=username).first()

    if existing_user:
        return restful_result(400, "注册失败，用户名已存在")
    else:
        if not avatar:
            avatar_url = app.config['DEFAULT_AVATAR_URL']
        elif allowed_file(avatar.filename):
            filename = avatar.filename  # 获取安全的文件名
            avatar_url = app.config['AVATAR_FOLDER'] + "/" + filename  # 图像文件保存路径
            avatar.save(avatar_url)  # 保存图像文件
        else:
            return restful_result(400, "您输入的头像图片格式不支持，请选择jpg, jpeg, png, bmp, webp等格式")
        new_user = User(name=username, password=password, avatar_url=avatar_url, is_admin=0)
        db.session.add(new_user)
        db.session.commit()
        return restful_result(200, "注册成功", {'user_id': new_user.id, 'username': new_user.name,
                                                'avatar_url': new_user.avatar_url})


# 用户登出
@app.route('/logout', methods=['GET'])
def logout():
    session.pop('user_id', None)  # 登出时清除session中的用户ID
    return restful_result(200, "您已成功登出")


# 创建新project
@app.route("/create", methods=['POST'])
def create():
    user_id = request.args.get('user_id')
    current_id = session.get('user_id')
    if not current_id:
        return restful_result(401, "您尚未登录")
    if not int(user_id) == current_id:
        return restful_result(403, "您无权操作该用户的数据")
    data = request.get_json()
    name = data["name"]
    width = data["width"]
    height = data["height"]
    style = data.get("style")
    type = data.get("type")
    new_project = Project(name=name, width=width, height=height, user_id=user_id, style=style, type=type)
    db.session.add(new_project)
    db.session.commit()
    # 把新project返回到数据库
    return restful_result(200, "工程创建成功", {'name': name, 'project_id': new_project.id})


# 列出一个用户的所有project
@app.route("/projects", methods=['GET'])
def projects():
    user_id = request.args.get('user_id')
    current_id = session.get('user_id')
    if not current_id:
        return restful_result(401, "您尚未登录")
    if not int(user_id) == current_id:
        return restful_result(403, "您无权操作该用户的数据")
    db.session.commit()
    projects = Project.query.filter_by(user_id=user_id).all()
    project_data = [project.to_json() for project in projects]
    return restful_result(200, "列出用户的所有工程", {"projects": project_data})


# 打开一个用户的某个project
@app.route("/project", methods=['GET'])
def project():
    user_id = request.args.get('user_id')
    project_id = request.args.get('project_id')
    current_id = session.get('user_id')
    if not current_id:
        return restful_result(401, "您尚未登录")
    if not int(user_id) == current_id:
        return restful_result(403, "您无权操作该用户的数据")
    db.session.commit()
    user = db.session.query(User).join(Project).filter(User.id == user_id, Project.id == project_id).first()
    if not user:
        return restful_result(403, "此工程id不属于此用户")
    db.session.commit()
    processed_images = db.session.query(ProcessedImage).join(Project).filter(
        ProcessedImage.project_id == project_id).order_by(ProcessedImage.layer).all()
    processed_images_json = []
    for processed_image in processed_images:
        processed_images_json.append(processed_image.to_json())
        print(processed_image.to_json())
        print("layer is: " + str(processed_image.layer))
    project = Project.query.filter_by(id=project_id).first()
    return restful_result(200, '获取到id为{}的工程信息'.format(project_id), {'project': project.to_json(),
                                                                             'processed_images': processed_images_json})


# 保存一个用户的工程
@app.route("/save", methods=['POST'])
def save():
    user_id = request.args.get('user_id')
    project_id = request.args.get('project_id')
    current_id = session.get('user_id')
    if not current_id:
        return restful_result(401, "您尚未登录")
    if not int(user_id) == current_id:
        return restful_result(403, "您无权操作该用户的数据")
    db.session.commit()
    user = db.session.query(User).join(Project).filter(User.id == user_id, Project.id == project_id).first()
    if not user:
        return restful_result(403, "此工程id不属于此用户")
    project = Project.query.filter_by(id=project_id).first()
    datas = request.get_json()
    datalist = datas.get('processed_images')
    width = datas.get('width')
    height = datas.get('height')
    style = datas.get('style')
    type = datas.get('type')
    if width:
        project.width = width
        db.session.commit()
    if height:
        project.height = height
        db.session.commit()
    if style:
        project.style = style
        db.session.commit()
    if type:
        project.type = type
        db.session.commit()
    processed_image_ids = []
    original_ids = set()
    processed_images = ProcessedImage.query.filter_by(project_id=project_id).all()
    for processed_image in processed_images:
        original_ids.add(processed_image.id)
    # 先读出所有原始的id，如果有原始的id在这次更新中没有出现，则删除掉它们
    thumbnail = Image.new('RGBA', (int(width), int(height)), (255, 255, 255, 0))
    img_ids = []
    for data in datalist:
        img_id = data["original_image_id"]
        img_ids.append(img_id)
        layer = data["layer"]
        pos_x = data["pos_x"]
        pos_y = data["pos_y"]
        rotate_deg = data["rotate_deg"]
        width = data["width"]
        height = data["height"]
        w_pos = data["w_pos"]
        w_neg = data["w_neg"]
        t_i = data["t_i"]
        # 获取到所有信息，进行处理
        image = ProcessedImage.query.filter_by(img_id=img_id, project_id=project_id).first()
        if image:
            ProcessedImage.query.filter_by(img_id=img_id, project_id=project_id).update({
                "pos_x": pos_x,
                "pos_y": pos_y,
                "rotate_deg": rotate_deg,
                "width": width,
                "height": height,
                "w_pos": w_pos,
                "w_neg": w_neg,
                "t_i": t_i,
                "layer": layer,
                "project_id": project_id
            })
            db.session.commit()
            original_ids.remove(image.id)  # 删除上一次有但这次没有的id
            processed_image_ids.append(image.id)
        else:
            processed_image = ProcessedImage(img_id=img_id, pos_x=pos_x, pos_y=pos_y, layer=layer,
                                             rotate_deg=rotate_deg, width=width, height=height, w_pos=w_pos,
                                             w_neg=w_neg, t_i=t_i, project_id=project_id)
            db.session.add(processed_image)
            db.session.commit()
            processed_image_ids.append(processed_image.id)
            # 把该图信息添加到数据库
    # 获取到所有信息，进行缩略图
    images = db.session.query(OriginalImage, ProcessedImage).join(ProcessedImage).filter(
        OriginalImage.id.in_(img_ids)).order_by(
        ProcessedImage.layer).all()
    for original_image, processed_image in images:
        _x, _y, _w, _h, _r = map(
            lambda x: math.ceil(x),
            (
                processed_image.pos_x,
                processed_image.pos_y,
                width,
                height,
                processed_image.rotate_deg,
            ),
        )

        file = Image.open(original_image.img_url).convert('RGBA')
        file = file.resize((_w, _h)).rotate(_r)  # 放缩和旋转
        thumbnail.alpha_composite(file, (_x, _y))
        thumbnail.save(app.config['THUMBNAIL_FOLDER'] + "/" + project_id + str(processed_image.id) + ".png")
    thumbnail_url = app.config['THUMBNAIL_FOLDER'] + "/" + project_id + ".png"
    thumbnail.save(thumbnail_url)
    project.thumbnail_url = thumbnail_url
    db.session.commit()
    if original_ids:  # 原始id非空
        for id in original_ids:
            db.session.query(ProcessedImage).filter_by(id=id).delete()
            db.session.commit()

    return restful_result(200, "工程已保存",
                          {"processed_image_ids": processed_image_ids})


# 打开一个用户的所有输出
@app.route("/output", methods=['GET'])
def output():
    user_id = request.args.get('user_id')
    current_id = session.get('user_id')
    if not current_id:
        return restful_result(401, "您尚未登录")
    if not int(user_id) == current_id:
        return restful_result(403, "您无权操作该用户的数据")
    db.session.commit()
    images = db.session.query(OutputImage).join(User).filter(User.id == user_id).all()
    images_json = []
    for image in images:
        images_json.append(image.to_json())
    return restful_result(200, "输出读取完成", {'images': images_json})


@app.route("/uploadimage", methods=['POST'])
def uploadimage():
    # 请求中获取到上传的图片
    a = request.files.get('image')
    if os.path.exists(app.config['TEMP_INPUT_IMAGE']):
        shutil.rmtree(app.config['TEMP_INPUT_IMAGE'])
    os.mkdir(app.config['TEMP_INPUT_IMAGE'])
    a.save(app.config['TEMP_INPUT_IMAGE']+ "/" + a.filename)  # 保存
    return restful_result(200, '素材上传完成')



# 上传素材
@app.route("/upload", methods=['POST'])
def upload():
    user_id = request.args.get('user_id')
    current_id = session.get('user_id')
    if not current_id:
        return restful_result(401, "您尚未登录")
    if not int(user_id) == current_id:
        return restful_result(403, "您无权操作该用户的数据")
    data = request.get_json()
    type = data.get('type')  # request.form.get()
    # images = request.files.get('images')
    styles = data.get('styles')
    category = data.get('category')
    if not os.path.exists(app.config['INPUT_FOLDER'] + "/" + user_id):
        os.mkdir(app.config['INPUT_FOLDER'] + "/" + user_id)
    # print("images: {}".format(images))
    print("styles: {}".format(styles))
    print("type: {}".format(type))
    db.session.commit()
    filename = os.listdir(app.config['TEMP_INPUT_IMAGE'])[0]
    print("filename:"+str(filename))
    image = Image.open(app.config['TEMP_INPUT_IMAGE']+"/"+filename)
    img_url = app.config['INPUT_FOLDER'] + "/" + user_id + "/" + filename  # 图像文件保存路径
    img = OriginalImage.query.filter_by(img_url=img_url).first()
    if img:
        return restful_result(400, '您的{}素材已经上传过同名素材了，请更改文件名，或删除原素材'.format(img.name))
    image.save(img_url)  # 保存图像文件

    new_img = OriginalImage(name=filename.split('.')[0], img_url=img_url,
                            user_id=user_id)
    db.session.add(new_img)
    db.session.commit()
    if styles:
        styles = json.loads(styles)
        print(styles)
        for style in styles:
            img_style = Image_Style(img_id=new_img.id, style=style)
            db.session.add(img_style)
            db.session.commit()
    if type:
        type = str(type)
        if category and type == "主体物":
            category = json.loads(category)
            img_type = Image_Type(img_id=new_img.id, type=type, category=category)
        else:
            img_type = Image_Type(img_id=new_img.id, type=type)
        db.session.add(img_type)
        db.session.commit()
    return restful_result(200, '素材上传完成')


# 列出给定素材的类型（type,tag）
@app.route("/tag", methods=['GET'])
def tag():
    user_id = request.args.get('user_id')
    current_id = session.get('user_id')
    if not current_id:
        return restful_result(401, "您尚未登录")
    if not int(user_id) == current_id:
        return restful_result(403, "您无权操作该用户的数据")
    img_id = request.args.get('img_id')
    db.session.commit()
    img = OriginalImage.query.filter_by(id=img_id).first()
    if not img:
        return restful_result(404, "该id的素材不存在")
    img = OriginalImage.query.filter_by(id=img_id, user_id=user_id).first()
    if not img:
        return restful_result(403, "该id的素材不属于您的账户，您无权操作")
    types = Image_Type.query.filter_by(img_id=img_id).all()
    types_list = []
    for type in types:
        types_list.append(type.to_json())
    return restful_result(200, "列出该素材的所有类别", {'types': types_list})


# 管理员更新素材/用户信息
@app.route("/update", methods=['PATCH'])
def update():
    user_id = request.args.get('user_id')
    current_id = session.get('user_id')
    if not current_id:
        return restful_result(401, "您尚未登录")
    if not int(user_id) == current_id:
        return restful_result(403, "您无权操作该用户的数据")
    db.session.commit()
    user = User.query.filter_by(id=user_id)
    datalist = request.get_json()
    original_image = datalist.get("original_image")
    if original_image:
        id = original_image.get("id")
        img = OriginalImage.query.filter_by(id=id).first()
        if not img:
            return restful_result(404, "该id的素材不存在")
        img = OriginalImage.query.filter_by(id=id, user_id=user_id).first()
        if not img:
            return restful_result(403, "该id的素材不属于您的账户，您无权操作")
        name = original_image.get("name")
        styles = original_image.get("style")
        types = original_image.get("type")
        category = original_image.get("category")
        if name:
            img.name = name
            db.session.commit()
        if styles:  # 如果修改后的styles个数小于原来的，则删除多余的Image_Style项；如果大于原来的，则添加额外的Image_Style项
            image_styles = Image_Style.query.filter_by(img_id=id).all()
            for image_style in image_styles:
                if styles:
                    image_style.style = styles.pop()  # 每次取出最后一个style来赋值
                else:
                    db.session.delete(image_style)
                    db.session.commit()
            while styles:
                image_style = Image_Style(img_id=id, style=styles.pop())
                db.session.add(image_style)
                db.session.commit()
        if types:  # 如果修改后的styles个数小于原来的，则删除多余的Image_Style项；如果大于原来的，则添加额外的Image_Style项
            image_types = Image_Type.query.filter_by(img_id=id).all()
            for image_type in image_types:
                if types:
                    type_ = types.pop()
                    if image_type.type == "主体物" and type_ != "主体物":
                        image_type.category = None
                        db.session.commit()
                    elif type_ == "主体物":
                        image_type.category = category
                        db.session.commit()
                    image_type.type = type_  # 每次取出最后一个type来赋值
                else:
                    db.session.delete(image_type)
                    db.session.commit()
            while types:
                type_ = types.pop()
                if type_ != "主体物":
                    image_type = Image_Type(img_id=id, type=type_)
                    db.session.add(image_type)
                    db.session.commit()
                elif type_ == "主体物":
                    image_type = Image_Type(img_id=id, type=type_, category=category)
                    db.session.add(image_type)
                    db.session.commit()
    if datalist.get("user"):
        if not user.is_admin:
            return restful_result(403, "非管理员无法修改用户信息")
        data = datalist["user"]
        id = data["id"]
        tmp = dict()
        for k, v in data.items():
            if v:
                tmp[k] = v
        User.query.filter_by(id=id).update(tmp)
        db.session.commit()
    return restful_result(200, "更新完成")


# 管理员删除素材/用户信息
@app.route("/delete", methods=['DELETE'])
def delete():
    user_id = request.args.get('user_id')
    current_id = session.get('user_id')
    if not current_id:
        return restful_result(401, "您尚未登录")
    if not int(user_id) == current_id:
        return restful_result(403, "您无权操作该用户的数据")
    data = request.get_json()
    db.session.commit()
    user = User.query.filter_by(id=user_id).first()
    original_image_id = data.get("original_image_id")
    processed_image_id = data.get("processed_image_id")
    output_image_id = data.get("output_image_id")
    project_id = data.get("project_id")
    user_id_ = data.get("user_id")
    # 处理
    if original_image_id:
        img = OriginalImage.query.filter_by(id=original_image_id).first()
        if not img:
            return restful_result(404, "该id的素材不存在")
        img = OriginalImage.query.filter_by(id=original_image_id, user_id=user_id).first()
        if not img:
            return restful_result(403, "该id的素材不属于您的账户，您无权操作")
        os.remove(img.img_url)
        db.session.delete(img)
    if user_id_:
        if not user.is_admin:
            return restful_result(403, "非管理员无法删除用户信息")
        user = User.query.filter_by(id=user_id_).first()
        if not user:
            return restful_result(404, "该id对应的用户不存在")
        db.session.delete(user)
    if processed_image_id:
        img = ProcessedImage.query.filter_by(id=processed_image_id).first()
        if not img:
            return restful_result(404, "该id对应的已处理素材不存在")
        user = db.session.query(User).join(Project).join(ProcessedImage).filter(
            ProcessedImage.id == processed_image_id).first()
        if not user.id == current_id:
            return restful_result(403, "该id的素材不属于您的账户，您无权操作")
        os.remove(img.img_url)
        db.session.delete(img)
    if output_image_id:
        img = OutputImage.query.filter_by(id=output_image_id).first()
        if not img:
            return restful_result(404, "该id对应的输出图片不存在")
        user = db.session.query(User).join(OutputImage).filter(OutputImage.id == output_image_id).first()
        if not user.id == current_id:
            return restful_result(403, "该id的输出图片不属于您的账户，您无权操作")
        os.remove(img.img_url)
        db.session.delete(img)
    if project_id:
        project = Project.query.filter_by(id=project_id).first()
        if not project:
            return restful_result(404, "该id对应的工程不存在")
        user = db.session.query(User).join(Project).filter(Project.id == project_id).first()
        if not user.id == current_id:
            return restful_result(403, "该id的工程不属于您的账户，您无权操作")
        processed_images = ProcessedImage.query.filter_by(project_id=project_id).all()
        for img in processed_images:
            os.remove(img.img_url)
            db.session.delete(img)
        db.session.delete(project)
    db.session.commit()
    return restful_result(200, "删除完成")


@app.route('/recommend', methods=['GET'])
def recommend():
    db.session.commit()
    types = OriginalImage.query.with_entities(OriginalImage.type).distinct().all()
    types = [type[0] for type in types]
    return restful_result(200, "列出所有类别", {
        'categories': types})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

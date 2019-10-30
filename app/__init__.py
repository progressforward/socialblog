from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask import Blueprint
from flask_login import LoginManager
from flask_pagedown import PageDown

#创建扩展，因为要使用工厂函数，所以无法传入程序实例参数，需要在工厂函数中进行初始化
#扩展不能定义在工厂函数中，否则其他函数无法引用
bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
login_manager.login_message = u'登录之后，才能进入哦！'  #登录认证提示语

def create_app(config_name):
    """
    create_app为工厂函数，该函数可以延长创建程序实例，便于动态修改配置
    使用蓝本Blueprint，便于路由定义，同时可以使得设计更加结构化
    使用init_app方法初始化扩展
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)  #需要最开始初始化配置，否则可能会影响flask-mail等扩展的初始化

    bootstrap.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    pagedown.init_app(app)

    #使用app.register_blueprint方法注册蓝本
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    
    from .api_1_0 import api as api_1_0_blueprint
    app.register_blueprint(api_1_0_blueprint, url_prefix='/api/v1.0')

    return app



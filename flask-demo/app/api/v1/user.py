from . import api
from app.api.common.resp import Success, NotFoundError, ParameterErrorMethod, DuplicateErrorMethod
from app.utils import token
from app.models.user import User
from app.models import db
from flask import current_app, request


@api.get('/get_user_list')
def users():
    """v1 user 获取用户列表"""
    page = request.args.get('page', 1, type = int)
    size = request.args.get('size', 10, type = int)
    pagination = User.query.paginate(page=page, per_page=size, error_out=False)
    users = pagination.items
    total = pagination.total
    pages = pagination.pages
    return Success(dict(list=[user.serialized for user in users], total=total, pages=pages))

@api.post('/add_user')
def userAdd():
    """v1 user 添加用户"""
    data = request.get_json()
    if not data:
        return ParameterErrorMethod('请传入正确的参数！')
    if 'name' not in data or 'gender' not in data:
        return ParameterErrorMethod('请传入正确的参数！')
    
    name = data['name']
    gender = '1' if data['gender'] == 'male' else '2'
    checkUser = User.query.filter(User.name == name).first()
    current_app.logger.info(checkUser)
    if checkUser:
        return DuplicateErrorMethod('用户已存在！')
    
    user = User(name=name, gender=gender)
    db.session.add(user)
    db.session.commit()
    return Success(dict(data=user.serialized))

@api.post('/edit_user')
def userEdit():
    """v1 user 编辑用户"""
    data = request.get_json()
    if not data:
        return ParameterErrorMethod('请传入正确的参数！')
    if 'name' not in data or 'gender' not in data or 'originName' not in data:
        return ParameterErrorMethod('请传入正确的参数！')
    
    originName = data['originName']
    name = data['name']
    gender = '1' if data['gender'] == 'male' else '2'
    checkUser = User.query.filter(User.name == originName).first()
    if not checkUser:
        return DuplicateErrorMethod('编辑用户不存在！')
    
    checkUser.name = name
    checkUser.gender = gender
    db.session.commit()
    return Success(dict(data=checkUser.serialized))


@api.get('/user_not_found')
def user_not_found():
    """v1 返回 404 测试路由"""
    raise NotFoundError('没有找到 user')


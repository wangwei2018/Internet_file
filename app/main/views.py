from . import main
import time
from flask import render_template, request, flash, redirect, url_for,session
from ..models import User, Memo, Message, File
from app import db
from flask_login import login_required, current_user, login_user, logout_user
import urllib
import os


@main.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form.get("username")).first()
        if user and user.verify_password(request.form.get("password")):
            flash("登录成功")
            login_user(user)
            return render_template("info.html")
        flash("用户名或密码错误")
    return render_template("index.html")


@main.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        name = request.form.get("name")
        sex = request.form.get("sex")
        email = request.form.get("email")
        info = request.form.get("info")
        form = {
            "username": username,
            "name": name,
            "sex": sex,
            "email": email,
            "info": info
        }
        user1 = User.query.filter_by(username=username).first()
        user2 = User.query.filter_by(email=email).first()
        if user1:
            flash("用户名已被注册")
            return render_template("register.html", form=form)
        if user2:
            flash("邮箱已被注册")
            return render_template("register.html", form=form)

        if password and username and email:
            flash("注册成功,可以登录了")
            user = User()
            user.username = username
            user.password = password
            user.name = name
            if sex == "女":
                user.sex = False
            else:
                user.sex = True
            user.email = email
            user.info = info
            db.session.add(user)
            db.session.commit()
            return render_template("index.html")
        flash("请将必填项填写完整")
    return render_template("register.html")


@main.route("/logout")
@login_required
def logout():
    logout_user()
    session.clear()
    flash("注销成功，请重新登录")
    return render_template("index.html")


@main.route("/info", methods=["GET", "POST"])
@login_required
def info():
    return render_template("info.html")


@main.route("/edit", methods=["GET", "POST"])
@login_required
def edit():
    if request.method == "POST":
        name = request.form.get("name")
        sex = request.form.get("sex")
        info = request.form.get("info")
        current_user.name = name
        current_user.info = info
        if sex == "男":
            current_user.sex = True
        else:
            current_user.sex = False
        db.session.commit()
        flash("个人资料修改成功")
        return render_template("info.html")
    return render_template("edit.html")


@main.route("/memo")
@login_required
def memo():
    list_memo = current_user.memos
    list_memo.reverse()
    return render_template("memos.html", memoes=list_memo)


@main.route("/add_memo", methods=["GET", "POST"])
@login_required
def add_memo():
    if request.method == "POST":
        theme = request.form.get("theme")
        content = request.form.get("content")
        memo = Memo()
        memo.user_id = current_user.id
        memo.theme = theme
        memo.content = content
        memo.time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        db.session.add(memo)
        db.session.commit()
        flash("备忘录添加成功")
        return redirect(url_for(".memo"))
    return render_template("add_memo.html")


@main.route("/delete_memo/<id>")
@login_required
def delete_demo(id):
    id = int(id)
    memo = Memo.query.filter_by(id=id).first()
    print(memo.id)
    print(memo.theme)
    print(memo.content)
    if memo:
        db.session.delete(memo)
        db.session.commit()
        flash("删除成功")
    return redirect(url_for(".memo"))


@main.route("/message")
@login_required
def message():
    list_msgs = current_user.receive_messages
    list_msgs.reverse()
    return render_template("messages.html", msgs=list_msgs)


@main.route("/send_message", methods=["GET", "POST"])
@login_required
def send_message():
    if request.method == "POST":
        username = request.form.get("username")
        content = request.form.get("content")
        user = User.query.filter_by(username=username).first()
        if user:
            msg = Message()
            msg.sender = current_user.username
            msg.receiver_id = user.id
            msg.content = content
            msg.time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
            db.session.add(msg)
            db.session.commit()
            flash("发送成功")
            return redirect(url_for(".message"))
        flash("不存在此用户")
    return render_template("send_message.html")


@main.route("/delete_msg/<id>")
@login_required
def delete_msg(id):
    id = int(id)
    msg = Message.query.filter_by(id=id).first()
    if msg:
        db.session.delete(msg)
        db.session.commit()
        flash("删除成功")
        return redirect(url_for(".message"))
    return render_template("messages.html")


@main.route("/reply/<username>", methods=["GET", "POST"])
@login_required
def reply(username):
    user = User.query.filter_by(username=username).first()
    content = request.form.get("content")
    if request.method == "POST":
        msg = Message()
        msg.sender = current_user.username
        msg.receiver_id = user.id
        msg.content = content
        msg.time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        db.session.add(msg)
        db.session.commit()
        flash("回复成功")
        return redirect(url_for(".message"))
    return render_template("reply.html", username=username)


@main.route("/file")
@login_required
def file():
    list_file = current_user.files
    list_file.reverse()
    return render_template("file.html", files=list_file)


@main.route("/upload_file", methods=["GET", "POST"])
@login_required
def upload_file():
    if request.method == "POST":
        file = request.files.get("file")
        if file:
            size=len(file.read())
            file.seek(0)
            file.save("/home/ww/save/" + file.filename)
            demo = File()
            demo.sender_id = current_user.id
            demo.filename = file.filename
            demo.filesize =size
            demo.time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
            share = request.form.get("share")
            file.close()
            if share == "yes":
                demo.share = True
            else:
                demo.share = False
            file.close()
            db.session.add(demo)
            db.session.commit()
            flash("上传成功")
            return redirect(url_for(".file"))
        flash("上传失败")
    return render_template("upload_file.html")


@main.route("/delete_file/<file_id>")
@login_required
def delete_file(file_id):
    file = File.query.filter_by(id=file_id).first()
    if file:
        db.session.delete(file)
        db.session.commit()
        os.remove("/home/ww/save/"+file.filename)
        flash("删除成功")
        return redirect(url_for(".file"))
    flash("删除失败")
    return render_template("file.html")


@main.route("/share_file/<file_id>")
@login_required
def share_file(file_id):
    file = File.query.filter_by(id=file_id).first()
    if file:
        if file.share:
            file.share = False
            db.session.commit()
            flash("已取消共享")
        else:
            file.share = True
            db.session.commit()
            flash("共享成功")
        return redirect(url_for(".file"))
    flash("设置失败")
    return render_template("file.html")


@main.route("/allfiles")
@login_required
def all_file():
    files = File.query.filter_by(share=True).order_by(db.desc(File.time))

    return render_template("allfile.html", files=files)


@main.route("/download_file/<file_id>")
@login_required
def download_file(file_id):
    file = File.query.filter_by(id=file_id).first()
    filename=file.filename
    if file:
        path = "/home/ww/save/" +filename
        try:
            file = open(path,"rb")
            content=file.read()
            print(content)
            file.close()
            f = open("/home/ww/下载/" + filename, "wb")
            f.write(content)
            f.close()
            flash("下载完成")

        except:
            print("不存在此文件")
            flash("下载失败")
    else:
        flash("下载失败")
    return redirect(url_for(".all_file"))



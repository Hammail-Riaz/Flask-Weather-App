from flask import render_template, request, redirect, url_for, session, flash
from models import Blog_posts
from datetime import datetime
from app import database
import secrets
import string

def generate_token(length=16):
    """Generate a random alphanumeric token string."""
    alphabet = string.ascii_letters + string.digits  # A-Z, a-z, 0-9
    return ''.join(secrets.choice(alphabet) for _ in range(length))

def register_routes(app):
    app.secret_key = "mysupersecretkey123"
    
    @app.route("/", methods=["GET", "POST"])
    def home():
        if request.method == "POST":
            name = request.form.get("name").strip()
            title = request.form.get("title").strip()
            content = request.form.get("content").strip()
            
            if title and content and name:
                post_token = generate_token()
                new_post = Blog_posts(name=name, post_title=title, post_content=content, date_and_time=datetime.now().replace(microsecond=0), post_token = post_token)
                database.session.add(new_post)
                database.session.commit()
                

                return redirect(url_for("post_token", post_token = post_token))
                
                
        return render_template("index.html")

    @app.route("/post-token")
    def post_token():
        token = request.args.get('post_token')
        post = Blog_posts.query.filter_by(post_token=token).first()
        
        return render_template("post_token.html", post_token= token, post=post)
    
    @app.route("/view_posts")
    def view_posts():
        posts = Blog_posts.query.all()        
        return render_template("view_posts.html", posts= posts)
    
    @app.route("/post-del-page", methods=["GET", "POST"])
    def post_del_page():
        if request.method == "POST":
            # token comes from form
            token = request.form.get("token")
            post = Blog_posts.query.filter_by(post_token=token).first()
            if post:
                database.session.delete(post)
                database.session.commit()
                flash("✅ Post deleted successfully!", "success")

            else:
                flash("❌ Invalid token! No post found.", "danger")

            return redirect(url_for("view_posts"))
        return render_template("post_del_page.html")

    
    @app.route("/admin")
    def admin():
        if not session.get("admin_logged_in"):
            return redirect(url_for("admin_login"))
    

        posts = Blog_posts.query.all()
        return render_template("admin.html", posts=posts)
    
    @app.route('/admin-login', methods=["GET", "POST"])
    def admin_login():
        if session.get("admin_logged_in") == True:
            return redirect(url_for("admin"))
        else:
            if request.method == "POST":
                admin_name = request.form.get("admin-name").strip()
                admin_password = request.form.get("admin-password").strip()
                
                if admin_name == "Hammail Riaz" and admin_password == "246813579":
                    flash("✅ Admin Login Succesfully!", "success")
                    session['admin_logged_in'] = True
                    return redirect(url_for("admin"))
                else:
                    flash("❌ Wrong Admin Details!", "danger")
                    return render_template("admin_login.html")
        
        return render_template("admin_login.html")
    
    @app.route("/admin-logout")
    def admin_logout():
        session.pop("admin_logged_in", None)  # remove session
        flash("✅ Admin Logout Successfully!", "danger")
        
        return redirect(url_for("admin_login"))
    
    
        
    @app.route("/delete/<int:post_id>")
    def delete_post(post_id):
        if session.get("admin_logged_in"):
            post = Blog_posts.query.get_or_404(post_id)
            database.session.delete(post)
            database.session.commit()
            return redirect(url_for("admin"))
        else:
            return redirect(url_for("admin_login"))
    
    
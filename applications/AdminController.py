from flask import Flask, render_template, request, redirect, url_for
from flask import current_app as app

@app.route("/admin/101/home", methods=["GET", "POST"])
def Admin_page():
    if(request.method=="GET"):
        #temp:
        AdminPro = {"Id":101, "name":"Admin1"}
        return render_template('AdminHomePage.html', AdminPro = AdminPro)
    
  


from flask import Flask,request,url_for,render_template,session,g,jsonify,abort
from blog import app
import MySQLdb as mysql
import config
#@app.before_request
#def connect_db():
#    g.db=mysql.connect(
#        host=config.dbhost,user=config.dbuser,
#        passwd=config.dbpass,db=config.dbname
#    )
@app.route('/pharmaadmin/create_article')
def create_article():
    if request.method=='POST':
        return jsonify(message='message')
    return render_template('create_article.html')

@app.route('/ajax_submit_article_info')   
def submit_article_info():
    title=request.args.get('title','')
    desc=request.args.get('description','')
    cat=request.args.get('cat','')
    success=0
    article_id=0
    if title !='' and desc!='' and  cat!='':
        try:
            cur=g.db.cursor()
            cur.connection.autocommit(True)
            params=[title, desc ,cat]
            result=cur.callproc('create_article',(params))
            rows=cur.fetchone()
            session['article_id']=str(rows[0])
            article_id=rows[0]
            session['article_id']=article_id
            cur.close()
            #g.db.close()
            success=1
        except:
            success=0
            #g.db.close()            
        return jsonify(success=success)
    else:
        return abort(404)

@app.route('/ajax_upload_article_docs',methods=['POST'])
def upload_docs():
    if request.method=='POST':
        try:        
            from werkzeug import secure_filename
            import os
            import uuid
            file=request.files['name_doc_upload_file']
            filename=secure_filename(file.filename)
            file_extention=filename.rsplit('.',1)[1]
            file_name=str(uuid.uuid4())+'.'+file_extention
            root_path=os.path.dirname(__file__)
            upload_dir_path=os.path.join(root_path,'uploads')
            file_path=os.path.join(upload_dir_path,file_name)
            file.save(file_path)
            cur=g.db.cursor()
            cur.connection.autocommit(True)
            params=[int(session['article_id']),file_path,filename]
            result=cur.callproc('upload_doc',params)
            cur.close()
            return filename
        except:
            #import sys
            #e = sys.exc_info()[0]
            return '1'
        

   
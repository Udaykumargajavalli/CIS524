from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import sys
from datetime import datetime



app = Flask(__name__)

app.config["UPLOAD_FOLDER"] = "static/"

@app.route('/')
def upload_file():
    return render_template('index.html')
 
    
@app.route('/display', methods = ['GET', 'POST'])
def parse():  
    if request.method == 'POST':
        def replace1(s1, s2, s3):
            i=s1.find(s2)
            while i!=-1:
                a=s1[:i]+s3+s1[i+len(s2):]
                s1=a
                i=s1.find(s2)
            return s1
        
        def split1(s1, s2):
            s=list()
            i=s1.find(s2)
            while i!=-1:
                s.append(s1[:i])
                s1=s1[i+len(s2):]
                i=s1.find(s2)
            s.append(s1)
            return s
        
        f = request.files['file']        
        filename = secure_filename(f.filename)
        f.save(app.config['UPLOAD_FOLDER'] + filename)
        f1 = open(app.config['UPLOAD_FOLDER']+filename,'r')
        lis = f1.read()
        lis = split1(lis,'\n')
        total=0;
        for lin in lis:
            lin1=lin.lower();
            if lin1.find("time log:")!=-1:
                lis.remove(lin);
                break;
            else:
                lis.remove(lin);
        for lin in lis:
            lin1=lin.lower();
            lin1=replace1(lin1," -","-")
            lin1=replace1(lin1,"- ","-")
            lin1=split1(lin1," ");
            for word in lin1:
                if word.find('-')!=-1:
                    time=split1(word,'-')
                    fat='%I:%M:%p'
                    time1=time[0];
                    time2=time[1];
                    try:
                        time1=time1[:-2]+':'+time1[-2:]
                        time1=datetime.strptime(time1,fat)
                        time2=time2[:-2]+':'+time2[-2:]
                        time2=datetime.strptime(time2,fat)
                    except:
                        continue;
                    total = total + (time2-time1).seconds/60
        output = "Total time spent by the author is"+str(int((total)/60))+"hours"+str(int((total)%60))+"mins"
        return render_template('index.html',prediction_text=output)
    return render_template('index.html')
                    

if __name__ == '__main__':
    app.run(debug = True)
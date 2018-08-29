from flask import Flask, redirect, request, url_for, render_template, g
import os, sqlite3
from model.load import init
import keras.models
import numpy as np 
from mido import MidiFile

global instruments
instruments = [0]*128 
instruments[0]=5
instruments[1]=5
instruments[2]=5
instruments[3]=5
instruments[4]=5
instruments[5]=18
instruments[6]=18
instruments[7]=15
instruments[8]=15
instruments[9]=11
instruments[10]=11
instruments[11]=11
instruments[12]=11
instruments[13]=11
instruments[14]=11
instruments[15]=11
instruments[16]=11
instruments[17]=18
instruments[18]=17
instruments[19]=18
instruments[20]=17
instruments[21]=17
instruments[22]=17
instruments[23]=17
instruments[24]=17
instruments[25]=16
instruments[26]=16
instruments[27]=0
instruments[28]=0
instruments[29]=0
instruments[30]=0
instruments[31]=0
instruments[32]=0
instruments[33]=19
instruments[34]=19
instruments[35]=19
instruments[36]=19
instruments[37]=19
instruments[38]=19
instruments[39]=19
instruments[40]=19
instruments[41]=7
instruments[42]=7
instruments[43]=7
instruments[44]=7
instruments[45]=7
instruments[46]=7
instruments[47]=7
instruments[48]=7
instruments[49]=8
instruments[50]=8
instruments[51]=8
instruments[52]=8
instruments[53]=2
instruments[54]=2
instruments[55]=2
instruments[56]=2
instruments[57]=6
instruments[58]=6
instruments[59]=6
instruments[60]=6
instruments[61]=6
instruments[62]=6
instruments[63]=6
instruments[64]=6
instruments[65]=3
instruments[66]=3
instruments[67]=3
instruments[68]=3
instruments[69]=10
instruments[70]=10
instruments[71]=10
instruments[72]=10
instruments[73]=10
instruments[74]=10
instruments[75]=10
instruments[76]=10
instruments[77]=12
instruments[78]=12
instruments[79]=12
instruments[80]=12
instruments[81]=4
instruments[82]=4
instruments[83]=4
instruments[84]=4
instruments[85]=4
instruments[86]=4
instruments[87]=4
instruments[88]=4
instruments[89]=14
instruments[90]=14
instruments[91]=14
instruments[92]=14
instruments[93]=14
instruments[94]=14
instruments[95]=14
instruments[96]=14
instruments[97]=9
instruments[98]=9
instruments[99]=9
instruments[100]=9
instruments[101]=9
instruments[102]=9
instruments[103]=9
instruments[104]=9
instruments[105]=13
instruments[106]=13
instruments[107]=13
instruments[108]=13
instruments[109]=13
instruments[110]=13
instruments[111]=7
instruments[112]=13
instruments[113]=1
instruments[114]=1
instruments[115]=1
instruments[116]=1
instruments[117]=1
instruments[118]=1
instruments[119]=1
instruments[120]=1
instruments[121]=9
instruments[122]=9
instruments[123]=9
instruments[124]=9
instruments[125]=9
instruments[126]=9
instruments[127]=9


app = Flask(__name__)
DATABASE = 'songs'

global model, graph
model, graph = init()

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

global_hit = 0
def reportstatus():
    if global_hit==-1:
        return "Invalid MIDI"
    elif global_hit==0:
        return "Not a Hit"
    else:
        return "Hit"

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/", methods=["POST", "GET"])
def server():
    global global_hit
    # Intercept a POSTed request
    if request.method == "POST":
        song = request.form['song-name'].strip().lower()
        mid  = request.form['midi-path']
        # hit = clf(mid, song)
        
        maxpad=32112
        Q=[]
        if os.path.exists(mid):
            try:
                fp = MidiFile(mid)
                data = [ [0]*maxpad for i in range(20) ] 
                appendat = [0 for i in range(20)]
                current_group = 0

                for i, track in enumerate(fp.tracks):
                    for msg in track:
                        if msg.type=='program_change':
                            current_group = instruments[msg.program]
                        if msg.type=='note_on':
                            data[current_group][ appendat[current_group] ]=msg.note
                            appendat[current_group] += 1
                Q= [np.reshape(np.asarray(data), 20*maxpad) ]
                Q=np.asarray(Q)
                Q = Q.reshape(Q.shape[0], maxpad, 20,1)

                with graph.as_default():
                    #perform the prediction
                    out = model.predict(Q)
                    if out[0][0]==0 and out[0][1]==1:
                        hit = 1
                    else:
                        hit = 0
                cursor=get_db().cursor()
                cursor.execute('''select song from chart where song=?;''', (song, ))
                result = cursor.fetchone()
                if result is None:
                    cursor.execute('''insert into chart values(?, ?, ?);''', (song, 0, 0))
                if hit==1:
                    global_hit=1
                    cursor.execute('''update chart set hits=hits+1 where song=?''', (song, ))
                else:
                    global_hit=0
                cursor.execute('''update chart set  searchs=searchs+1 where song=?''', (song, ))
                get_db().commit()
            except:
                # corrupted MIDI File
                global_hit=-1
                pass

        return redirect(url_for('server'))
    # for GETs
    cursor=get_db().cursor()
    cursor.execute('''select * from chart''')
    items = []
    for row in cursor:
        items += [row]
    #print(items)
    items.sort(key = lambda el: el[1])
    topTracks1 = [x for x in items if x[1]!=0][-1 * min(len(items), 5):][::-1]
    #print(topTracks1)
    items.sort(key = lambda el: el[2])
    mostSearched1 = items[-1 * min(len(items), 5):][::-1]
    #print(mostSearched1)
    return render_template('index.html',hit=reportstatus(), topTracks=topTracks1, mostSearched=mostSearched1)


if __name__ == "__main__":
    app.run()

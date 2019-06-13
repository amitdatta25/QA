import sys
sys.path.append('../')
from run_squad import fetchSquad
from flask import jsonify,Flask,request

import json

app = Flask(__name__)

@app.route('/get_pred', methods=['GET','POST'])
def get_pred():
    k_doc=2
    #predict_query = request.json

    input=r"/datadrive/amitbanik/bert-squad1/bert-master/data/dev-v1.3.json"

    with open(input) as jsonfile:
        temp = json.dumps(jsonfile.read())
        predict_query = json.loads(temp)
        predict_query1 = json.loads(json.loads(temp))
       # print(predict_query['data'])

    l1=[]
    l2=[]
    #predict_query = "{\"data\": [{\"title\": \"University_of_Notre_Dame\",\"paragraphs\": [{\"context\": \"As opposed to broadcasts of primetime series, CBS broadcast special episodes of its late night talk shows as its lead-out programs for Super Bowl 50, beginning with a special episode of The Late Show with Stephen Colbert following the game. Following a break for late local programming, CBS also aired a special episode of The Late Late Show with James Corden.\",\"qas\": [{\"question\": \"Which late night comedy host show played immediately after Super Bowl 50 ended?\",\"id\": \"56bf6f743aeaaa14008c9631\"}]}]}]}"
    pred,all_pred = fetchSquad(False,True,predict_query)
    for j in range(0,k_doc):
        p=str(j+1)
        a=predict_query1["data"][j]['paragraphs'][0]['score']
        b=all_pred[p][0]['score']
        c=float(a)+b
        q=predict_query1["data"][0]['paragraphs'][0]['qas'][0]['question']
        print(q)
        #print(float(a)+b)

        l1={p:{'Question':q,'Answer':pred[p],'Score':all_pred[p][0]['score'],'Total_Score':c,'Context':predict_query1["data"][j]['paragraphs'][0]['context']}}

        #print(l1)
        l2.append(l1)

        #print(predict_query1["data"][j]['paragraphs'][0]['score'])
    print(l2)
    l3=[]
    l5=[]
    for k in range(0,k_doc):
        d=str(k+1)
        l3.append(l2[k][d]['Total_Score'])
        l5.append(l2[k][d]['Total_Score'])
        #l3.append(l2[1]['2']['Total_Score'])

    #print(l3)



    l3.sort(reverse = True)

    index1=[]
    for element in l3:

        print(element)
        print(l5)

        index_order=(l5.index(element))
        print(index_order)
        index1.append(index_order)
    print(index1)
    final_list=[]
    for final_index in index1:
        index_final=str(final_index+1)
        print()
        final_list.append(l2[final_index][index_final])
    print(final_list)



    new_pred1=json.dumps(final_list)
    new_pred = {'1':{'Answer':pred['1'],'Score':all_pred['1'][0]['score'],}, '2':{'Answer':pred['2'], 'Score':all_pred['2'][0]['score']}}
    jsonify1 = jsonify({'pred': pred, 'all_pred': all_pred})
    #print({'Answer':pred['1'],'all_pred':all_pred['1'][0]['score']})
    # jsonify1


    return jsonify({'new_pred': new_pred1})
    #return jsonify1
    #return jsonify(predict_query[["data"][0]["score"]])



if __name__ == '__main__':
    app.run(debug=True)




import sys

#sys.path.append('..')
from run_squad import fetchSquad
from flask import jsonify, Flask, request
from flask import Flask
# from flask.ext.cache   import Cache
from flask_cache import Cache
from flask import request

cache = Cache()
CACHE_TYPE = 'simple'

import json

app = Flask(__name__)
cache.init_app(app)

# app.config['CACHE_TYPE'] = 'simple'
app.cache = Cache(app)


@app.route('/get_pred', methods=['POST'])
# @app.route('/get_pred', methods=['POST'])
@cache.cached(300, key_prefix='get_pred')
# @app.cache.cached(timeout=300)

def get_pred():
    #input = r"/datadrive/amitbanik/bert-squad1/bert-master/data/QArequest.json"
    # input1=request.get_json(force=True)
    # print(jsonify(input1))
    # input1=json.dumps(input1)
    data = json.dumps(request.get_json())
    print(data)
    pr1 = (json.loads(json.dumps(request.get_json())))
    #print(pr1)
    #print("pr1")
    input1 = request.get_json()
    #print(input1)
    #print("data is " + format(data))


    #with open(input, 'r', encoding='utf8', errors='ignore') as jsonfile:
        # with open(data) as jsonfile:
        # with open(input) as jsonfile:
        #temp = json.dumps(jsonfile.read())
        #predict_query = json.loads(temp)
        #predict_query2 = json.loads(json.loads(temp))
    predict_query1 = (json.loads(json.dumps(request.get_json())))
    print(predict_query1)
    #print("predict_query1")

    print(predict_query1)
    #print("predict_query2")
    #print(predict_query2)
    #print("mu")
    #print(predict_query1['mu'])

    # print(predict_query['data'])

    l1 = []
    l2 = []
    # predict_query = "{\"data\": [{\"title\": \"University_of_Notre_Dame\",\"paragraphs\": [{\"context\": \"As opposed to broadcasts of primetime series, CBS broadcast special episodes of its late night talk shows as its lead-out programs for Super Bowl 50, beginning with a special episode of The Late Show with Stephen Colbert following the game. Following a break for late local programming, CBS also aired a special episode of The Late Late Show with James Corden.\",\"qas\": [{\"question\": \"Which late night comedy host show played immediately after Super Bowl 50 ended?\",\"id\": \"56bf6f743aeaaa14008c9631\"}]}]}]}"

    # query=predict_query1["queryText"]
    mu = predict_query1['mu']
    # print(query)
    # print(mu)
    score_list = []
    context_list = []
    preview_list = []
    fileneme_list = []
    id_list = []
    pagei_list = []
    l1_k = []
    l2_k = []
    l4_k = []
    k_doc=predict_query1["doc_count"]
    for j in range(0, k_doc):
        p = str(j)
        # a=predict_query1["data"][j]['paragraphs'][0]['score']
        # b=all_pred[p][0]['score']
        # c=float(a)+b
        # q=predict_query1["data"][0]['paragraphs'][0]['qas'][0]['question']
        # print(q)
        # print(float(a)+b)
        score_list.append(predict_query1["docs"][j]["score"])
        context_list.append(predict_query1["docs"][j]["content_txt_en"])
        #l1_k = {j: {'query_text': predict_query1["queryText"], 'mu': predict_query1["mu"],
                    #'Score': predict_query1["docs"][j]["score"],
                    #'Context': predict_query1["docs"][j]["content_txt_en"]}}
        #l2_k.append(l1_k)
        # l3={"paragraphs":[{"context":predict_query1["docs"][j]["content_txt_en"]},{'qas':[{"question":predict_query1["queryText"],"id":p}]}]}
        l3 = {"paragraphs": [{"context": predict_query1["docs"][j]["content_txt_en"],
                              'qas': [{"question": predict_query1["queryText"], "id": p}]}]}
        l4_k.append(l3)
    # print(score_list)
    # print(context_list)
    # print(l2_k)
    # print(l4_k)
    final_list_k = []
    for item in l4_k:
        final_json = {"data": item}
        final_list_k.append(final_json)

    pred_k_doc = json.dumps(final_list_k)
    # print(pred_k_doc)
    json_data = json.dumps({"data": l4_k})
    print("JSON DATA")
    print(json_data)

    predict_query_k = json.loads(json_data)

    # predict_query = "{\"data\": [{\"title\": \"University_of_Notre_Dame\",\"paragraphs\": [{\"context\": \"As opposed to broadcasts of primetime series, CBS broadcast special episodes of its late night talk shows as its lead-out programs for Super Bowl 50, beginning with a special episode of The Late Show with Stephen Colbert following the game. Following a break for late local programming, CBS also aired a special episode of The Late Late Show with James Corden.\",\"qas\": [{\"question\": \"Which late night comedy host show played immediately after Super Bowl 50 ended?\",\"id\": \"56bf6f743aeaaa14008c9631\"}]}]}]}"
    # pred,all_pred = fetchSquad(False,True,json_data)
    # print(pred)
    # predict_query_k = json.loads(json)
    # predict_query = "{\"data\": [{\"title\": \"University_of_Notre_Dame\",\"paragraphs\": [{\"context\": \"As opposed to broadcasts of primetime series, CBS broadcast special episodes of its late night talk shows as its lead-out programs for Super Bowl 50, beginning with a special episode of The Late Show with Stephen Colbert following the game. Following a break for late local programming, CBS also aired a special episode of The Late Late Show with James Corden.\",\"qas\": [{\"question\": \"Which late night comedy host show played immediately after Super Bowl 50 ended?\",\"id\": \"56bf6f743aeaaa14008c9631\"}]}]}]}"
    pred, all_pred = fetchSquad(False, True, json_data)

    # print(all_pred)
    # print(predict_query_k['data'])

    # predict_query = request.json

    #l1 = []
    #l2 = []
    op_list = []
    doc = []

    for j in range(0, k_doc):
        p = str(j)
        # a=predict_query1["data"][j]['paragraphs'][0]['score']
        b = all_pred[p][0]['score']
        # print(b)
        # c=float(a)+b
        q = predict_query_k["data"][0]['paragraphs'][0]['qas'][0]['question']
        # print(q)
        # print(float(a)+b)
        d = mu * all_pred[p][0]['score'] + (1 - mu) * predict_query1["docs"][j]["score"]

        def read_squad_examples(input_data):
            """Read a SQuAD json file into a list of SquadExample."""

            # with tf.gfile.Open(input_file, "r") as reader:
            # temp = json.dumps(input_file)
            # input_data = input_data1

            def is_whitespace(c):
                if c == " " or c == "\t" or c == "\r" or c == "\n" or ord(c) == 0x202F:
                    return True
                return False

            examples = []
            # for entry in input_data:

            paragraph_text = input_data
            doc_tokens = []
            char_to_word_offset = []
            prev_is_whitespace = True
            for c in paragraph_text:
                if is_whitespace(c):
                    prev_is_whitespace = True
                else:
                    if prev_is_whitespace:
                        doc_tokens.append(c)
                    else:
                        doc_tokens[-1] += c
                    prev_is_whitespace = False
                char_to_word_offset.append(len(doc_tokens) - 1)
                # print(char_to_word_offset)

            return (doc_tokens)
        a = read_squad_examples(predict_query1["docs"][j]["content_txt_en"])
        s1 = ""
        for words in a:
            s1 += words + " "
        print(s1)
        ans_offset = s1.index(pred[p])
        ans_length=len(pred[p])


        #l1 = {p: {'Question': q, 'Answer': pred[p], 'Score': predict_query1["docs"][j]["score"],
                  #'preview_s': predict_query1["docs"][j]["preview_s"],
                  #'fileName_s': predict_query1["docs"][j]["fileName_s"],
                  #'content_txt_en': predict_query1["docs"][j]["content_txt_en"], 'id': predict_query1["docs"][j]["id"],
                  #'page_i': predict_query1["docs"][j]["page_i"], 'Total_Score': d}}
        #op_json = {p: {"queryText": q, "mu": mu, "docs": [
            #{'Answer': pred[p], 'Score': predict_query1["docs"][j]["score"],
             #'preview_s': predict_query1["docs"][j]["preview_s"], 'fileName_s': predict_query1["docs"][j]["fileName_s"],
             #'content_txt_en': predict_query1["docs"][j]["content_txt_en"], 'id': predict_query1["docs"][j]["id"],
             #'page_i': predict_query1["docs"][j]["page_i"], 'Bert_score': all_pred[p][0]['score'], 'Total_Score': d}]}}
        context=predict_query1["docs"][j]["content_txt_en"]
        doc.append({'ans_text': pred[p], 'score': predict_query1["docs"][j]["score"],
                    'preview_s': predict_query1["docs"][j]["preview_s"],
                    'fileName_s': predict_query1["docs"][j]["fileName_s"],
                    'content_txt_en': s1,
                    'id': predict_query1["docs"][j]["id"], 'page_i': predict_query1["docs"][j]["page_i"],
                    'bert_score': all_pred[p][0]['score'], 'total_Score': d,'ans_offset':ans_offset,'ans_length':ans_length})
        # print(l1)
        #l2.append(l1)
        #op_list.append(op_json)

        # print(predict_query1["data"][j]['paragraphs'][0]['score'])
    # print(l2)
    l3 = []
    l5 = []
    doc_score=[]
    for k in range(0, k_doc):
        d = str(k)

        #l3.append(l2[k][d]['Total_Score'])
        #l5.append(l2[k][d]['Total_Score'])
        l3.append(doc[k]['total_Score'])
        l5.append(doc[k]['total_Score'])

        # l3.append(l2[1]['2']['Total_Score'])

    # print(l3)

    l3.sort(reverse=True)

    index1 = []
    # print(l3)
    # print(l5)
    for element in l3:
        # print(element)

        index_order = (l5.index(element))
        # print(index_order)
        index1.append(index_order)
    # print(index1)
    final_list = []
    op_final_list1 = []
    for final_index in index1:
        index_final = str(final_index)
        # print()
        final_list.append(doc[final_index])
        op_final_list1.append(doc[final_index])
    # print(final_list)

        # a=predict_query1["data"][j]['paragraphs'][0]['score']

    q = predict_query_k["data"][0]['paragraphs'][0]['qas'][0]['question']
    new_pred1 = (json.dumps(final_list))
    # new_pred2=(json.dumps(op_final_list1))
    print(q)
    print(predict_query1["mu"])
    new_pred3 =  {"queryText": q, "mu": predict_query1["mu"], "doc_count":predict_query1["doc_count"],"docs":op_final_list1}
    print("new_pred3")
    #print(json.dumps(op_final_list1))
    # print(new_pred1)
    # print(type(new_pred1))
    # print(type(json_data))
    # new_pred = {'1':{'Answer':pred['1'],'Score':all_pred['1'][0]['score'],}, '2':{'Answer':pred['2'], 'Score':all_pred['2'][0]['score']}}
    # jsonify1 = jsonify({'pred': pred, 'all_pred': all_pred})
    # print({'Answer':pred['1'],'all_pred':all_pred['1'][0]['score']})
    # jsonify1
    #print(new_pred2[1:])
    print(new_pred3)

    # return jsonify({'new_pred1': new_pred1})
    # return  jsonify({'new_pred2': new_pred2})
    return jsonify(new_pred3)

    # return 0
    # return  jsonify1
    # return 1
    # return jsonify(predict_query[["data"][0]["score"]])


if __name__ == '__main__':
    app.run(debug=True)



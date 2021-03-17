import pickle
from flask import Flask, jsonify, request,render_template,Response
import flask



test_File = open('test_data.pkl','rb')
test_data2 = pickle.load(test_File)
test_File.close()

model_file = open('finalized_model5.sav','rb')
model = pickle.load(model_file)
model_file.close()

product_dict = pickle.load(open('product_id_name.pkl','rb'))

id = product_dict['product_id'].values
name = product_dict['product_name'].values

pro_name = dict()
for i in range(49677):
  pro_name[id[i]] = name[i]
    
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():

  to_predict_list = [int(x) for x in request.form.values()]
  order_id = to_predict_list[0]
  if order_id in test_data2.order_id.unique():
    test = test_data2[test_data2.order_id==order_id]
    predict = model.predict(test.drop(['order_id','product_id'],axis=1))
    test['predict'] = predict
    test = test[(test['predict']==1)]
    output = []
    for i in test.product_id:
      if i=='None':
        output.append('No items')
      else:
        output.append(pro_name[i])
    if len(output)==0:
      return Response(render_template('result.html',data=['No items']))
    else:
      return Response(render_template('result.html',data=output))
  else:
    return Response(render_template('result.html',data=['please enter order id from test data']))

    


if __name__ == '__main__':
    app.run(host='0.0.0.0',port = 5050 )
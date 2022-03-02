import json

def map(file_input, file_output):
    with open(file_input, "r") as f:
        newText = f.read().replace('][',',')


    js = json.loads(newText)

    new_js = []
    mapper = {}
    counter = 0
    reviews = 0
    for item in js:
        reviews = reviews + 1
        prod_id = item.get('product_id')
        dic = {'review_id' : item.get('review_id'), 'aspect_pairs' :  item.get('aspect_pairs')}

        if prod_id in mapper:
            index = mapper.get(prod_id)
            new_js[index][prod_id].append(dic)

        else:
            prod_dic = {prod_id : []}
            prod_dic[prod_id].append(dic)
            new_js.append(prod_dic)
            mapper.update({prod_id : counter})
            counter = counter + 1


    with open(file_output, "w") as f1:
        json.dump(new_js,f1)

    print(counter)
    print(reviews)






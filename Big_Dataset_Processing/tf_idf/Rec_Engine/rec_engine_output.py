import json
import sys
import ast
import sys, getopt, types

def main(argv):            
    arg_dict={}
    switches={'li':list,'di':dict,'tu':tuple}
    singles=''.join([x[0]+':' for x in switches])
    long_form=[x+'=' for x in switches]
    d={x[0]+':':'--'+x for x in switches}
    try:            
        opts, args = getopt.getopt(argv, singles, long_form)
    except getopt.GetoptError:          
        print("bad arg")                      
        sys.exit(2)       

    for opt, arg in opts:        
        if opt[1]+':' in d: o=d[opt[1]+':'][2:]
        elif opt in d.values(): o=opt[2:]
        else: o =''
        if o and arg:
            arg_dict[o]=ast.literal_eval(arg)

        if not o or not isinstance(arg_dict[o], switches[o]):    
            print(opt, arg, " Error: bad arg")
            sys.exit(2)

    with open('Small_Dataset_Processing/smaller_review_index_dict.json', 'r') as f:
        review_index_dict = json.load(f)
    with open('reviewid_businessid_dict.json', 'r') as g:
        business_id_dict = json.load(g)
    with open('businessid_business_name_dict.json', 'r') as h:
        business_name_dict = json.load(h)
    liked_review_ids = []
    recommended_review_ids = []
    for (review_id, index) in review_index_dict.items():
        for tup in arg_dict['li']:
            if index == int(tup[0]):
                liked_review_ids.append(review_id)
            elif index == int(tup[1]):
                recommended_review_ids.append(review_id)
    liked_businesses = []
    recommended_businesses = []
    for review_id in liked_review_ids:
        business_id = business_id_dict[review_id]
        business_name = business_name_dict[business_id]
        liked_businesses.append(business_name)
    for review_id in recommended_review_ids:
        business_id = business_id_dict[review_id]
        business_name = business_name_dict[business_id]
        recommended_businesses.append(business_name)
    for i in liked_businesses:
        ind = liked_businesses.index(i)
        s = 'Because you liked {}, we think you should try {}.'.format(\
            i, recommended_businesses[ind])
        print(s)

if __name__ == '__main__':
    main(sys.argv[1:])

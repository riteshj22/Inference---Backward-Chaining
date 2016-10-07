import sys
import copy
# function to add a clause to storage

i = 0

d = {}
kb = []
list1 = []
flag = False
imply_flag = False
output_file = open("output.txt", "w")
main_list = []
temp_list = []


def display(list):
    for item in list:
        print item
        print "\n"


def create_kb(kb, statement):
    d = {}
    if "=>" in statement:

        statement_split = statement.split("=>")
        if '&' in statement_split[0]:
            l = []
            premise = statement_split[0].split("&")

            pre = ""
            for rel in premise:
                p = 0
                pre = ''
                while rel[p] != "(":
                    pre += rel[p]
                    p += 1
                # print pre,
                rest = rel[p + 1:-1]
                parameters = rest.split(",")
                # print parameters,
                temp = {'predicate': pre, 'param': parameters, 'flag': False, 'list': [], 'sub': '', 'arg': 0}
                temp['arg'] = len(temp['param'])
                # if temp['param'][0] != 'x':
                #     temp['sub'] = temp['param'][0]
                l.append(temp)
            d['left'] = l
            # print l,

            q = 0
            pre = ""
            while statement_split[1][q] != "(":
                pre += statement_split[1][q]
                q += 1
            # print predicate
            rest = statement_split[1][q + 1:-1]
            parameters = rest.split(",")
            imply = {'predicate': pre, 'param': parameters, 'flag': False, 'list': [], 'sub': '', 'arg': 0}
            imply['arg'] = len(imply['param'])
            # if imply['param'][0] != 'x':
            #     imply['sub'] = imply['param'][0]
            d['right'] = imply
            # print imply
            kb.append(d)
        else:

            q = 0
            pre = ''
            d = {}
            l = []
            while statement_split[0][q] != "(":
                pre += statement_split[0][q]
                q += 1
            # print predicate
            rest = statement_split[0][q + 1:-1]
            parameters = rest.split(",")
            temp = {'predicate': pre, 'param': parameters, 'flag': False, 'list': [], 'sub': '', 'arg': 0}
            temp['arg'] = len(temp['param'])
            # if temp['param'][0] != 'x':
            #     temp['sub'] = temp['param'][0]
            l.append(temp)
            d['left'] = l

            # right
            pre = ''
            q = 0
            while statement_split[1][q] != "(":
                pre += statement_split[1][q]
                q += 1
            # print predicate
            rest = statement_split[1][q + 1:-1]
            parameters = rest.split(",")
            imply = {'predicate': pre, 'param': parameters, 'flag': False, 'list': [], 'sub': '', 'arg': 0}
            imply['arg'] = len(imply['param'])
            # if imply['param'][0] != 'x':
            #     imply['sub'] = imply['param'][0]
            d['right'] = imply
            kb.append(d)
    else:
        index = 0
        pre = ''
        t = {}
        while statement[index] != "(":
            pre += statement[index]
            index += 1
        # print predicate
        rest = statement[index + 1:-1]
        parameters = rest.split(",")
        t = {'predicate': pre, 'param': parameters, 'flag': False, 'list': [], 'arg': 0}
        t['arg'] = len(t['param'])
        kb.append(t)


sub = ''
count = 0
left_list = []
right_list = []
constant_index = -1


def evaluate(query, knowledge_base, sub, sub_index, arg):
    flag = False
    imply_flag = False
    global list1
    global left_list
    global right_list
    global output_file
    if arg > 1:
        if sub_index == 1:
            constant_index = 0
        if sub_index == 0:
            constant_index = 1
    l = ''
    global count
    p = (",".join(query['param']))
    print 'Query: ', query['predicate'] + '(' + p + ')'
    print_string = 'Query: ' + query['predicate'] + '(' + p + ')' + '\n'
    output_file.write(print_string)

    # if sub:
    for clause in knowledge_base:
        if 'right' not in clause:
            if arg == clause['arg']:
                tt = False
                if arg == 1:
                    if query['predicate'] == clause['predicate']:
                        tt = True
                else:
                    if query['predicate'] == clause['predicate'] and query['param'][constant_index] == clause['param'][
                                        constant_index]:
                        tt = True
                if tt:
                    s1flag = False
                    if (clause['param'][sub_index]) in sub:
                        s1flag = True
                    if s1flag:
                        flag = True
                        p = (",".join(query['param']))
                        str1 = query['predicate'] + '(' + p + '): '
                        list1.append(clause['param'][sub_index])
                        if imply_flag:
                            list1.reverse()
                        str1 += str(flag)
                        if flag and list1:
                            if not sub:
                                str1 += ':' + str(list1)
                        if "x" in main_query['param']:
                            str1 += ':' + str(list1)
                        print str1
                        output_file.write(str1 + "\n")
                        if sub:
                            if "x" not in query['param']:
                                list1 = clause['param']
                        return flag, list1, sub
        else:
            if query['predicate'] == clause['right']['predicate']:
                if "x" in clause['right']['param']:
                    sub_index = clause['right']['param'].index("x")
                if sub_index == 1:
                    constant_index = 0
                if sub_index == 0:
                    constant_index = 1
    for clause in knowledge_base:
        if 'right' in clause:
            if arg == clause['right']['arg']:
                # sflag = False
                # if sub_index != -1:
                    # if arg > 1:
                    #     if clause['right']['predicate'] == query['predicate'] and clause['right']['param'][constant_index] == \
                    #             query['param'][constant_index]:
                    #         sflag = 1
                    # else:
                if clause['right']['predicate'] == query['predicate']:
                    sflag = 1
                # else:
                #     if clause['right']['predicate'] == query['predicate']:
                #         sflag = 1
                # if sflag:
                    c = 0
                    list1 = []
                    left_list = []
                    right_list = []
                    n = len(clause['left'])
                    if 'x' in clause['right']['param']:
                        sub_index = clause['right']['param'].index("x")
                    if sub_index == 1:
                        constant_index = 0
                    if sub_index == 0:
                        constant_index = 1
                    for r in clause['left']:
                        c += 1
                        p = (",".join(r['param']))
                        l += r['predicate'] + '(' + p + ')'
                        if c != n and n != 1:
                            l += '&'
                        if n == 1:
                            l += '=>'
                    if n != 1:
                        l += '=>'
                    p = (",".join(clause['right']['param']))
                    l += clause['right']['predicate'] + '(' + p + ')'
                    print 'Query: ', l
                    t1 = 'Query: ' + l + '\n'
                    output_file.write(t1)
                    imply_flag = True
                    l1 = len(clause['left'])
                    count = 0
                    for relation in clause['left']:
                        list1 = []
                        count += 1

                        if sub:
                            relation['sub'] = sub
                        temp_index = sub_index
                        if 'x' in relation['param']:
                            sub_index = relation['param'].index("x")
                        a = relation['arg']
                        f, t2, sub1 = evaluate(relation, knowledge_base, relation['sub'], sub_index, a)
                        sub_index = temp_index
                        # if sub1 != sub:
                        #     sub = sub1
                        if not query['list']:
                            query['list'] = list1

                        list1 = list(set(query['list']).intersection(list1))

                        if f and list1:
                            query['flag'] = f
                            flag = True
                        else:
                            flag = False
                            break_flag = True
                            break
                        if not imply_flag:
                            list1.reverse()

                        query['list'] = list1
        else:
            if arg == clause['arg']:
                if clause['predicate'] == query['predicate']:
                    tt1 = False
                    if arg == 1:
                        tt1 = True
                    else:
                        if clause['param'][constant_index] == query['param'][constant_index]:
                            tt1 = True
                    if tt1:
                        if not sub:
                            if query['param'][sub_index] == 'x':
                                clause['flag'] = True
                                flag = True
                                clause['list'].append(clause['param'][sub_index])
                                if count == 1:
                                    left_list.append(clause['param'][sub_index])
                                if count == 2:
                                    right_list.append(clause['param'][sub_index])
                                if clause['param'][sub_index] not in list1:
                                    list1.insert(0, clause['param'][sub_index])
                        else:
                            m = 0
                            for pm in clause['param']:
                                if pm in sub:
                                    m = 1
                                    sub = [pm]
                                    list1.insert(0, pm)
                            if m == 0:
                                continue
                            else:
                                flag = True

    str1 = query['predicate'] + '('
    if arg > 1:
        if sub_index < constant_index:
            str1 += query['param'][sub_index] + ',' + query['param'][constant_index] + '): '
        else:
            str1 += query['param'][constant_index] + ',' + query['param'][sub_index] + '): '
    else:
        str1 += query['param'][sub_index] + '): '
    str1 += str(flag)
    if imply_flag:
        list1.reverse()
    t = sub
    if t != list1:
        if flag and list1:
            if not query['sub']:
                str1 += ': ' + str(list1)
    print str1
    output_file.write(str1 + "\n")
    return flag, list1, sub


# declaration

# ########################### opening the input file as a command line argument ###############################
input_file = open(sys.argv[-1], "r")
# ########################### reading the file ###############################
file_content = input_file.read().splitlines()

sindex = -1
for line_no, content in enumerate(file_content):

    # query to be evaluated

    if line_no == 0:
        predicate = ""
        i = 0
        query = content
        # Predicate for Main query
        if '&' in query:
            temp_list = query.split("&")
            # print 'mainlist', temp_list
            for item in temp_list:
                i = 0
                predicate = ''
                while item[i] != "(":
                    predicate += item[i]
                    i += 1
                # print predicate
                rest = item[i + 1:-1]
                parameters = rest.split(",")
                main_query = {'predicate': predicate, 'param': parameters, 'flag': False, 'list': [], 'sub': '', 'arg': 0}
                main_query['arg'] = len(main_query['param'])
                main_list.append(main_query)
                # print main_list
        else:
            i = 0
            while query[i] != "(":
                predicate += query[i]
                i += 1
            # print predicate
            rest = query[i + 1:-1]
            parameters = rest.split(",")
            main_query = {'predicate': predicate, 'param': parameters, 'list': [], 'flag': False, 'sub': '', 'arg': 0}
            main_query['arg'] = len(main_query['param'])
            if "x" in main_query['param']:
                sindex = main_query['param'].index("x")
            else:
                sub = main_query['param']
                # print query

    # Number of clauses
    if line_no == 1:
        no_of_clauses = int(content)
        # print clauses

    # clauses array

    if 1 < line_no <= no_of_clauses + 1:
        create_kb(kb, content)

# print len(kb)
# display(kb)

tflag = False
if main_list:
    print 'Query: ', query
    print_string = 'Query: ' + query + "\n"
    output_file.write(print_string)
    t_list = []
    temp_count = 0
    for i, item in enumerate(main_list):
        sindex = -1
        temp_count += 1
        main_query = copy.deepcopy(item)
        if "x" in item['param']:
            sindex = item['param'].index("x")
        else:
            sub = item['param']
        arg = item['arg']
        tflag, l, s1 = evaluate(item, kb, sub, sindex, arg)
        if tflag:
            if i == 0:
                t_list = l
            else:
                t_list = list(set(t_list).intersection(l))
            list1 = []
        else:
            tflag = False
            break
    if temp_count == len(main_list):
        if not t_list:
            tflag = False
    str1 = query + ': '
    str1 += str(tflag)

    if tflag and t_list:
        str1 += ': ' + str(t_list)
    # print str1
    # query['list'] = list1
    output_file.write(str1 + "\n")


else:
    evaluate(main_query, kb, sub, sindex, main_query['arg'])
# display(kb)
output_file.close()

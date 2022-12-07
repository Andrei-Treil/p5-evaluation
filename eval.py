import sys
from collections import defaultdict
import math

'''
inputFile - results of queries: [queryname,skip,play/sceneid,rank,score,description]
queryRel - relevancy of queries (0 for non-relevant, > 0 for relevant): [queryname,empty,docid,relevance]
outputFile - output evaluation here: [measure,querynum,score]
measure - NDCG@75 (there are multi-value relevance judgments in the data: 0,1,2), RR (reciprocal rank), P@15
          Recall@20, F1@25, Average Precision (AP)
'''
def main(inputFile,queryRel,outputFile):
    #NDCG_P = DCG_P/IDCG_P
    #DCG_P = rel_1 + sum_i=2 -> P(rel_i/log(i))
    #IDCG_P - DCG given a perfect ranking
    #RR - 1/rank of first rel doc
    #P@15 - # of rel docs in top 15 / 15
    #Recall@20 - # of rel docs in top 20 / total # of rel docs
    #F1@25 - 2RP/(R+P)
    #AP - average precision when a relevant doc is retrieved
    queries = defaultdict(list)
    only_rel = defaultdict(list)
    ap = defaultdict(int)
    with open(inputFile,'rt',encoding='utf-8') as f:

        for line in f.readlines():
            q_args = line.split()
            name = q_args[0]
            id = q_args[2]
            rank = q_args[3]
            score = q_args[4]

            queries[name].append((id,rank,score))
            if score > 0:
                only_rel[name].append((id,rank,score))
                ap[name] += len(only_rel[name])/rank

    for query,docs in queries.items():
        NDCG = get_dcg(docs[:75])/get_dcg(only_rel[query][:75])
        RR = 1/only_rel[query][0][1]
        P_15 = precision(docs[:15])
        R_20 = recall(docs[:20])
        P_25 = precision(docs[:25])
        R_25 = recall(docs[:25])
        F1_25 = 2*R_25*P_25 / (R_25+P_25)
        AP = ap[query]/len(ap[query])

        with open(outputFile,'a') as f:
            f.write("NDCG@75 {} {}\n".format(query,NDCG))
            f.write("RR {} {}\n".format(query,RR))
            f.write("P@15 {} {}\n".format(query,P_15))
            f.write("R@20 {} {}\n".format(query,R_20))
            f.write("F1@25 {} {}\n".format(query,F1_25))
            f.write("AP {} {}\n".format(query,AP))


        return

    def get_dcg(docs):
        dcg = docs[0][2]
        for i in range(1,len(docs)):
            dcg += docs[i][2]/math.log(i+1)


    def precision(docs):
        num_rel = 0
        for id,rank,score in docs:
            if score > 0:
                num_rel += 1
        return num_rel/len(docs)

    def recall(docs):
        num_rec = 0
        for id,rank,score in docs:
            if score > 0:
                num_rec += 1
        return num_rec/len(only_rel[id])

    return

if __name__ == '__main__':
    # Read arguments from command line, or use sane defaults for IDE.
    argv_len = len(sys.argv)
    inputFile = sys.argv[1] if argv_len >= 2 else 'runfile.trecrun'
    queryRel = sys.argv[2] if argv_len >= 3 else 'qrels'
    outputFile = sys.argv[3] if argv_len >= 4 else 'outputFile.eval'
    main(inputFile,queryRel,outputFile)
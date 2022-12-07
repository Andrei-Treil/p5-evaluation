import sys
from collections import defaultdict
import math
import os

'''
inputFile - results of queries: [queryname,skip,play/sceneid,rank,score,description]
queryRel - relevancy of queries (0 for non-relevant, > 0 for relevant): [queryname,empty,docid,relevance]
outputFile - output evaluation here: [measure,querynum,score]
measure - NDCG@75 (there are multi-value relevance judgments in the data: 0,1,2), RR (reciprocal rank), P@15
          Recall@20, F1@25, Average Precision (AP)
'''
def main(inputFile,queryRel,outputFile):
    ideal_rank = defaultdict(list)
    total_rel = defaultdict(int)
    relevance = defaultdict(int)
    with open(queryRel,'rt',encoding='utf-8') as f:
        for line in f.readlines():
            qname,skip,docid,rel = line.split()
            relevance[qname+docid] = int(rel)
            if int(rel) > 0:
                total_rel[qname] += 1
                ideal_rank[qname].append((docid,skip,int(rel)))
            
            
    #store only the relevant results for each query
    only_rel = defaultdict(list)
    #store qresults to each query
    queries = defaultdict(list)
    
    #store precision for each relevant result for each query
    ap = defaultdict(int)
    with open(inputFile,'rt',encoding='utf-8') as f:

        for line in f.readlines():
            q_args = line.split()
            name = q_args[0]
            id = q_args[2]
            rank = int(q_args[3])
            score = relevance[name+id]
            #score = float(q_args[4])

            queries[name].append((id,rank,score))
            if score > 0:
                only_rel[name].append((id,rank,score))
                ap[name] += len(only_rel[name])/rank

    ###################### helper functions ####################

    def get_dcg(docs):
        dcg = docs[0][2]
        for i in range(1,len(docs)):
            dcg += docs[i][2]/math.log(i+1,2)
        return dcg


    def precision(docs):
        if len(docs) == 0:
            return 0

        num_rel = 0
        for id,rank,score in docs:
            if score > 0:
                num_rel += 1

        return num_rel/len(docs)

    def recall(docs,query):
        if total_rel[query] == 0:
            return 0
            
        num_rec = 0
        for id,rank,score in docs:
            if score > 0:
                num_rec += 1
        return num_rec/total_rel[query]

    ############################################################

    #for all queries
    #TOTAL_NDCG,TOTAL_RR,TOTAL_P15,TOTAL_R20,TOTAL_F1,TOTAL_AP = [0]*6

    '''
    NDCG_P = DCG_P/IDCG_P
    DCG_P = rel_1 + sum_i=2 -> P(rel_i/log(i))
    IDCG_P - DCG given a perfect ranking
    RR - 1/rank of first rel doc
    P@15 - # of rel docs in top 15 / 15
    Recall@20 - # of rel docs in top 20 / total # of rel docs
    F1@25 - 2RP/(R+P)
    AP - average precision when a relevant doc is retrieved
    '''
    TOTAL_NDCG,TOTAL_RR,TOTAL_P15,TOTAL_R20,TOTAL_F1,TOTAL_AP = [0]*6
    for query,docs in queries.items():
        #only_rel[query].sort(key = lambda x: x[1])
        ideal_rank[query].sort(key = lambda x: x[2])
        NDCG = get_dcg(docs[:75])/get_dcg(ideal_rank[query][:75]) if total_rel[query] > 0 else 0
        TOTAL_NDCG += NDCG

        RR = 1/only_rel[query][0][1] if len(only_rel[query]) > 0 else 0
        TOTAL_RR += RR

        P_15 = precision(docs[:15])
        TOTAL_P15 += P_15
        
        R_20 = recall(docs[:20],query)
        TOTAL_R20 += R_20

        P_25 = precision(docs[:25])
        R_25 = recall(docs[:25],query)

        F1_25 = (2*R_25*P_25) / (R_25+P_25) if R_25+P_25 > 0 else 0
        TOTAL_F1 += F1_25

        AP = ap[query]/total_rel[query] if total_rel[query] > 0 else 0
        TOTAL_AP += AP


        
        with open(outputFile,'a') as f:
            f.write("NDCG@75".ljust(30) + "\t  {}\t{:.4f}\n".format(query,NDCG))
            f.write("RR".ljust(30) + "\t  {}\t{:.4f}\n".format(query,RR))
            f.write("P@15".ljust(30) + "\t  {}\t{:.4f}\n".format(query,P_15))
            f.write("R@20".ljust(30) + "\t  {}\t{:.4f}\n".format(query,R_20))
            f.write("F1@25".ljust(30) + "\t  {}\t{:.4f}\n".format(query,F1_25))
            f.write("AP".ljust(30) + "\t  {}\t{:.4f}\n".format(query,AP))
    
    with open(outputFile, 'a') as f:
        length = len(queries)
        f.write("NDCG@75".ljust(30) + "\t  all\t{:.4f}\n".format(TOTAL_NDCG/length))
        f.write("MRR".ljust(30) + "\t  all\t{:.4f}\n".format(TOTAL_RR/length))
        f.write("P@15".ljust(30) + "\t  all\t{:.4f}\n".format(TOTAL_P15/length))
        f.write("R@20".ljust(30) + "\t  all\t{:.4f}\n".format(TOTAL_R20/length))
        f.write("F1@25".ljust(30) + "\t  all\t{:.4f}\n".format(TOTAL_F1/length))
        f.write("MAP".ljust(30) + "\t  all\t{:.4f}\n".format(TOTAL_AP/length))

    return

if __name__ == '__main__':
    # Read arguments from command line, or use sane defaults for IDE.
    argv_len = len(sys.argv)
    inputFile = sys.argv[1] if argv_len >= 2 else 'simple.trecrun'
    queryRel = sys.argv[2] if argv_len >= 3 else 'qrels'
    outputFile = sys.argv[3] if argv_len >= 4 else 'mysimple.eval'
    if os.path.exists(outputFile):
        os.remove(outputFile)
    main(inputFile,queryRel,outputFile)
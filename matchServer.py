#!/usr/bin/env python
from http.server import BaseHTTPRequestHandler, HTTPServer
import hashlib
import numpy as np
from urllib.parse import urlparse
import json
import community
import pandas as pd
import networkx as nx
import requests
import statistics
from sklearn.feature_extraction.text import CountVectorizer
import matplotlib.pyplot as plt
import os

def get_query(queries):
    query='+'.join(queries)
    hash_query = hashlib.sha224(query.encode()).hexdigest()
    filepath = "images/" + hash_query + ".svg"
    api = '957b84a258254334bcaee1428e3e2d7d'

    url = ('https://newsapi.org/v2/everything?'
        'q='+query+
        '&language=en'
        '&apiKey='+api)
    response = requests.get(url)
    json = response.json()

    articles = json['articles']
    headline = [article['title'] for article in articles]
    description = [article['description'] for article in articles]

    all_text = headline + description

    cv = CountVectorizer(ngram_range=(1,1), stop_words = 'english')
    X = cv.fit_transform(all_text)
    names = cv.get_feature_names()

    Xc = (X.T * X) # This is the matrix manipulation step
    Xc.setdiag(0) # We set the diagonals to be zeroes as it's pointless to be 1

    links = []
    link_tuples = {}

    for x in range(0, Xc.shape[1]):
        for y in range(0, x-1):
            connection = Xc[x,y]
            if connection > 0:
                links.append((names[x], names[y]))
                if names[x] not in link_tuples:
                    link_tuples[names[x]] = [names[x], 0]
                link_tuples[names[x]][1] = link_tuples[names[x]][1] + 1
    sorted_nums = list(link_tuples.values())
    sorted_nums = sorted(sorted_nums, reverse=True, key=lambda tup: tup[1])

    # max = 0 if len(sorted_nums) == 0 else sorted_nums[0][1] if len(sorted_nums) < 50 else sorted_nums[50][1];

    # def filterEdges(edge):
    #     if edge[0] in link_tuples and edge[1] in link_tuples and link_tuples[edge[0]][1] > max and link_tuples[edge[1]][1] > max:
    #         return True
    #     else:
    #         return False
    # iltered_links = list(filter(filterEdges, links)) # get only edges that are bigger than the 50th highest degree node
    names = cv.get_feature_names() # This are the entity names (i.e. keywords)
    df = pd.DataFrame(data = Xc.toarray(), columns = names, index = names)
    #df.to_csv('bitcoin or dolphins.csv', sep = ',')
    df.to_csv(filepath + ".csv", sep = ',')
    Matrix=(filepath + ".csv")

    MatrixDF=pd.read_csv(Matrix, 
    sep=",", 
    header=0,
    index_col=False,
    error_bad_lines=True,
    warn_bad_lines=True,
    skip_blank_lines=True)
    MatrixPD=pd.DataFrame(MatrixDF)
    labsb=list(MatrixPD.columns.values)
    labsa=list(MatrixPD.columns.values)
    labs2b=labsb[1:]
    labs2a=labsa[1:]


    def check_element(labs, labs2a):
        return not set(labs).isdisjoint(labs2a)

    factor1=set(labsb)

    def check_element(labs, labs2b):
        return not set(labs).isdisjoint(labs2b)

    factor2=set(labsb)

    def check_element(labs2a, labs2b):
        return set(labs2a).isdisjoint(labs2b)


    #plot of the search query
    input_data = pd.read_csv(Matrix, index_col=0)
    G = nx.DiGraph(input_data.values)
    NodeImage=nx.draw(G,pos=nx.spring_layout(G), node_size=4) 

    A=np.matrix(MatrixPD)

    adjacency=A[1:,1:]
    rows, cols = np.where(adjacency == 1)
    edges = zip(rows.tolist(), cols.tolist())
    gr = nx.Graph()
    gr.add_edges_from(edges)
    part = community.best_partition(gr)
    mg = community.modularity(part,gr)
    if not os.path.isfile(filepath):
        plt.savefig(filepath)
        plt.clf()

    factorboth=set(labs2a)
    labels= ['Overlap', 'User A', 'User B']
    colors=['lavender', 'pink', 'azure']
    sizes= [len(factorboth), len(factor1), len(factor2)]

    plt.clf()
    plt.pie(sizes,labels=labels, colors=colors, startangle=90, autopct='%1.1f%%')

    piePath = filepath + ".2.svg"

    plt.axis('equal')
    plt.savefig(piePath)
    plt.clf()

    MatrixNum=[tuple(x) for x in MatrixDF.values]
    def cast_list(MatrixNum):
        if isinstance(MatrixNum, list):
            return map(cast_list, MatrixNum)
        else:
            return int(MatrixNum)
    MatrixPCA=pd.DataFrame(MatrixDF)
    Lab=MatrixPCA[MatrixPCA.columns[0]]
    MatrixPCAData=MatrixPCA.set_index(Lab)
    MatrixPCAData=MatrixPCA.drop(columns="Unnamed: 0")
    MatrixPCADataNew=MatrixPCAData.set_index(Lab)

    from sklearn.decomposition import PCA
    pca=PCA(n_components=2)
    PrincipalComponents=pca.fit_transform(MatrixPCADataNew)
    principalDF=pd.DataFrame(data=PrincipalComponents, columns=['principal component 1', 'principal component 2'])

    plt.scatter(principalDF['principal component 1'], principalDF['principal component 2'])
    pcafilepath = filepath + ".3.svg"

    plt.axis('equal')
    plt.savefig(pcafilepath)
    plt.clf()
    names = [i[0] for i in sorted_nums]

    return { 'filepath': filepath, 'names': names, 'relatedness': mg}

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-type', 'image/svg+xml')
        self.end_headers()

    def do_GET(self):
        query = urlparse(self.path)
        if query.path.startswith("/image") and os.path.isfile(query.path[1:]):
            file = open(query.path[1:],mode='r')
    
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-type', 'image/svg+xml')
            self.end_headers()
            # read all lines at once
            out = file.read()
    
            # close the file
            file.close()
            self.wfile.write(out.encode())
        else:
            query_components = dict(qc.split("=") for qc in query.query.split("&"))
            self.send_response(200)
            self.send_header('Access-Control-Allow-Origin', '*')
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            q = query_components["q"]
            data = get_query(q)
            dataString = json.dumps(data)
            self.wfile.write(dataString.encode())

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        self.wfile.write("".encode())
        
def run(server_class=HTTPServer, handler_class=S, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd...')
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()

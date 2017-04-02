import gensim
import load
import os
 
model_load = ['save/'+name for name in os.listdir('save') if name.endswith('doc2vec')]

if len(model_load)==0:
    documents = load.get_doc('docs')
    print ('Data Loading finished')
     
    print 'lendocuments: ',(len(documents),type(documents))
     
    # build the model
    model = gensim.models.Doc2Vec(documents, dm=1, alpha=0.025, size=100, min_alpha=0.025, min_count=1, window=5, sample=1e-3, negative=5)
     
    # start training
    for epoch in range(200):
        if epoch % 20 == 0:
            print ('Now training epoch %s'%epoch)
        model.train(documents)
        model.alpha -= 0.002  # decrease the learning rate
        model.min_alpha = model.alpha  # fix the learning rate, no decay
     
    model.save('save/trained.doc2vec')
else:
    # load the doc2vec
    model = gensim.models.Doc2Vec.load('save/trained.doc2vec')

    # shows the similar words
    print (model.most_similar('gatilh')),'\n'
     
    # shows the learnt embedding
    print (model['gatilh']),'\n'

    print model.n_similarity(['gatilh', 'atend'], ['tard', 'boa']),'\n'
     
    # shows the similar docs with id = 2
    #print (model.docvecs.most_similar(str(1)))

    new_doc = model.infer_vector([u'relat\xf3ri', u'hor', u'hor', u'pr\xf3pri', u'nom', u'diz', u'acompanh', u'quant', u'sess', u'realiz', u'hor', u'hor', u'vis', u'inform', u'ger', u'oper', u'set', u'statu', u'atend'])
    print 'most_similar: ',model.docvecs.most_similar([new_doc], topn = 30) #, topn = 5
import MySQLdb


class Record():
    #name = models.CharField(max_length=5000)
    
    class Meta:
        verbose_name = u'Record'
        verbose_name_plural = u'Records'

    def get_connection(self):
        return MySQLdb.connect(host='localhost', user='root', passwd='root',db='bd_test')

    def get_knowledgebases(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT text, title FROM knowledge_base")
        conn.close()
        return cursor

    def get_knowledge_validation(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        query = '''
                SELECT question
                FROM knowledge_bases_validation
                ORDER BY id_answer limit 1
                '''
        cursor.execute(query)
        conn.close()
        return cursor
        
    def __str__(self):
        return self.name
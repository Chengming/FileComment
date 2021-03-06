import json
import datetime
import unittest
import os
import shutil



class InvalidFileException(Exception):
    """
    """
    def __init__(self, filename):
        self._filename = filename

    def __str__(self):
        return self._filename+": No such file or directory"
        
        


class CFile(object):
    """
    """
    File = 0
    Folder = 1
    
    def __init__(self, filename):
        """
        """
        if os.path.exists(filename)==False:
            raise InvalidFileException(filename)
        if os.path.isfile(filename):
            self._type = CFile.File
        else:
            self._type = CFile.Folder
        # the abslute path name 
        self.abspath = os.path.abspath(filename)
        # the basename
        self.basename = os.path.basename(self.abspath)
        # the abslute path name of parient folder
        self.dirname = os.path.dirname(self.abspath)
                    
    def isFolder(self, ):
        return self._type==CFile.Folder

    def isFile(self,):
        return self._type==CFile.File




class CommentDB:
    _data_file_name_perfix = ".FileComment.json"
    def __init__(self, path):
        self._path = path
        self._comment_data_filename = os.path.join(self._path,CommentDB._data_file_name_perfix)
        if os.path.exists(self._comment_data_filename):
            with open(self._comment_data_filename,"r") as fd:
                self._comment_data = json.load(fd,encoding="UTF8")
        else:
            self._comment_data = {}
        
    def getAllComment(self,filename):
        ret = []
        if filename in self._comment_data:
            for comment in self._comment_data[filename]:
#                ret.append([comment["comment_data"],comment["timestamp"]])
                ret.append([comment["comment_string"],datetime.datetime.strptime(comment["timestamp"],"%Y-%m-%d %H:%M:%S")])
        ret.sort(key=lambda x: x[1],reverse=True)
        return ret
            
    def getLatestComment(self,filename):
        """
        ["comment string",timestamp]
        """
        ret = []
        latest_timestamp = datetime.datetime.strptime("1970-01-01 00:00:00","%Y-%m-%d %H:%M:%S")
        if filename in self._comment_data:
            for comment in self._comment_data[filename]:
                timestamp = datetime.datetime.strptime(comment["timestamp"],"%Y-%m-%d %H:%M:%S")
                if latest_timestamp<timestamp:
                    latest_timestamp = timestamp
                    ret = [comment["comment_string"],timestamp]
        return ret

    def addComment(self,filename,comment_string):
        if os.path.exists(self._comment_data_filename):
            newFileName = self._comment_data_filename+"~"
            shutil.copy(self._comment_data_filename,newFileName)
        comment = {}
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        comment["timestamp"] = timestamp
        comment["comment_string"] = comment_string
        if filename in self._comment_data:
            self._comment_data[filename].append(comment)
        else:
            self._comment_data[filename] = [comment]
        with open(self._comment_data_filename,"w") as fd:
            json.dump(self._comment_data,fd,encoding="UTF8")
        

class UT_CommentDB(unittest.TestCase):
    def setUp(self):
        shutil.copyfile("sample.json.test","sample.json")
        self._comment_db = CommentDB("sample.json")
    def tearDowm(self,):
        self._comment_db = None
        #os.remove("sample.json")
    def test_getAllComment_POS(self,):
        ret = self._comment_db.getAllComment("fileName1")
        result = [
            ["The comment data",datetime.datetime.strptime("2012-04-08 04:23:11","%Y-%m-%d %H:%M:%S")],
            ["The comment data 2",datetime.datetime.strptime("2012-04-03 05:23:11","%Y-%m-%d %H:%M:%S")]
        ]
        self.assertEqual(ret,result)

    def test_getAllComment_NEG(self,):
        ret = self._comment_db.getAllComment("none")
        self.assertEqual(ret,[])

    def test_getLatestComment_POS(self,):
        ret = self._comment_db.getLatestComment("fileName1")
        result = ["The comment data",datetime.datetime.strptime("2012-04-08 04:23:11","%Y-%m-%d %H:%M:%S")]
        self.assertEqual(ret,result)

    def test_getLatestComment_NEG(self,):
        ret = self._comment_db.getLatestComment("none")
        self.assertEqual(ret,[])
        
    def test_addComment(self,):
        self._comment_db.addComment("newfile","12345")
        cm = self._comment_db.getLatestComment("newfile")
        self.assertEqual(cm[0],"12345")


        
if __name__ == '__main__':
    comment_db = CommentDB("/home/chengming/workspace/github/pfcomment")
    comment_db.addComment("aaa","1234567")
   # suite = unittest.TestLoader().loadTestsFromTestCase(UT_CommentDB)

    #unittest.TextTestRunner(verbosity=2).run(suite)

    # 
    pass

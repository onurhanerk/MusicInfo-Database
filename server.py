import os
import pypyodbc
import cx_Oracle
import sys
from flask import Flask, render_template, request
app = Flask(__name__)



global connection,temp,table,number,fourth,value, updateID
nConnectString='Not Connected!'
connectString='Connected!'
first='You have to connect first!'
second='Tables created!' 
third='The tables were created earlier!'
fourth='You have to create table before!' 
fifth='.Item added to table!'
sixth='Please create a table.'
temp=0
table=0
number=1
value=1

@app.route("/") ##link uzantısı ve yönlendirme amacıyla bu tarz bir yapı kullanılıyor.
def main():
	return render_template('index.html')

@app.route('/send',methods=['GET','POST'])
def send():
	if request.method=='GET':
		return connectionDB(nConnectString,connectString) ##bağlantı sağlanması

@app.route('/createTable',methods=['GET','POST'])		
def createTable():
		global table,temp
		if temp==0:
			return connectionDB(first,first)
		else:
			statement1='CREATE TABLE GENRES(GENREID NUMBER, NAME VARCHAR2(50),PRIMARY KEY(GENREID))'
			statement2='CREATE TABLE ARTIST(ARTISTID NUMBER, NAME VARCHAR2(50), YEARS NUMBER, OTHERINFO VARCHAR2(50), PRIMARY KEY(ARTISTID))'
			statement3='CREATE TABLE ALBUMS (ALBUMID NUMBER, NAME VARCHAR2(50), RELEASEDATE NUMBER, GENREID NUMBER,ARTISTID NUMBER, PRIMARY KEY(ALBUMID), FOREIGN KEY(GENREID) REFERENCES GENRES, FOREIGN KEY(ARTISTID) REFERENCES ARTIST)'
			statement4='CREATE TABLE TRACKS (TRACKID NUMBER, ALBUMID NUMBER, NAME VARCHAR2(50), PLAYTIME VARCHAR2(10), INSTRUMENTS VARCHAR2(100), GENREID NUMBER, ARTISTID NUMBER, PRIMARY KEY(TRACKID), FOREIGN KEY(ALBUMID) REFERENCES ALBUMS,FOREIGN KEY(GENREID) REFERENCES GENRES, FOREIGN KEY(ARTISTID) REFERENCES ARTIST)'
			statement5="CREATE OR REPLACE TRIGGER T AFTER INSERT OR UPDATE OR DELETE ON ALBUMS DECLARE T_NAME ALBUMS.NAME%type; BEGIN FOR rec IN (SELECT DISTINCT A1.NAME FROM ALBUMS A1, ALBUMS A2 WHERE A1.NAME=A2.NAME AND A1.ARTISTID != A2.ARTISTID) LOOP DBMS_OUTPUT.PUT_LINE('Farklı sanatçılara ait ' || rec.NAME || ' isminde albüm saptandı!'); END LOOP;END;"
			statement6="CREATE OR REPLACE PROCEDURE SIMILAR_GENRE(TID IN NUMBER) IS temp_GENREID NUMBER; CURSOR C1 IS SELECT TRACKID FROM TRACKS WHERE TRACKID != TID AND GENREID=  (SELECT GENREID FROM TRACKS WHERE TRACKID=TID); BEGIN OPEN C1; LOOP FETCH C1 INTO temp_GENREID ; EXIT WHEN C1%NOTFOUND; dbms_output.put_line(temp_GENREID); END LOOP; CLOSE C1; END;"
			statement7="CREATE OR REPLACE PROCEDURE SIMILAR_ARTIST(TID IN NUMBER) IS temp_ARTISTID NUMBER; CURSOR C2 IS SELECT TRACKID FROM TRACKS WHERE TRACKID != TID AND ARTISTID =  (SELECT ARTISTID FROM TRACKS WHERE TRACKID=TID); BEGIN OPEN C2; LOOP FETCH C2 INTO temp_ARTISTID ; EXIT WHEN C2%NOTFOUND; dbms_output.put_line('ARTISTID: ' || temp_ARTISTID||';'); END LOOP; dbms_output.put_line('...'); CLOSE C2; END;"
			statement8="CREATE OR REPLACE PROCEDURE SIMILAR_INSTR(TID IN NUMBER) IS temp_ARTISTID NUMBER; temp_INSTR VARCHAR2(1000); CURSOR C3 IS SELECT TRACKID,INSTRUMENTS FROM TRACKS WHERE TRACKID != TID; BEGIN OPEN C3; LOOP FETCH C3 INTO temp_ARTISTID ,temp_INSTR ; EXIT WHEN C3%NOTFOUND; dbms_output.put_line(temp_ARTISTID); dbms_output.put_line(temp_INSTR ); END LOOP; CLOSE C3; END;"
			statement9=" CREATE OR REPLACE PROCEDURE SIMILAR_PLAYTIME(TID IN NUMBER) IS temp_ARTISTID NUMBER; temp_PTIME VARCHAR2(1000); CURSOR C4 IS SELECT TRACKID,PLAYTIME FROM TRACKS WHERE TRACKID != TID; BEGIN OPEN C4; LOOP FETCH C4 INTO temp_ARTISTID ,temp_PTIME ; EXIT WHEN C4%NOTFOUND; dbms_output.put_line(temp_ARTISTID); dbms_output.put_line(temp_PTIME); END LOOP; CLOSE C4; END;"
			temp=temp+1 ## Tablolar yaratıldığı için su anlık default
			c = connection.cursor()
			return connectionDB(first,third)
     ##Gerekli tablolarıın yaratılması

			if table==0:
				c.execute(statement1)
				c.execute(statement2)
				c.execute(statement3)
				c.execute(statement4)
				##c.execute(statement5)
				##c.execute(statement6)
				##c.execute(statement7)
				##c.execute(statement8)
				##c.execute(statement9)
				table+=1
				return connectionDB(first,second)
			else:
				return connectionDB(first,third)

@app.route('/insertDate',methods=['GET','POST'])     ## ilk öden için insert işlemi
def insertDate():
		global number,table,temp,value
		sentence=''
		if temp==0:
			return connectionDB(first,fourth)
		else:
			if table==0:
				return connectionDB(first,sixth)
			else:
				statement= "INSERT INTO TRACKS (TRACKID , ALBUMID , NAME , PLAYTIME)  values (:2, :3, :4, :5)"
				c = connection.cursor()
				c.execute(statement, ('TValue-' + str(value), 'AValue-' + str(value), 'NValue-'+str(value), 'PValue-'+str(value)))
				connection.commit()
				sentence=sentence+str(number)+'.record was added to the table!'
				number+=1
				value+=1
				return connectionDB(first,sentence)

@app.route('/addedTrack',methods=['GET','POST'])  ## Track ekleme 
def addedTrack():
	result = request.form   ## html üzerinden alınan id ve değeri
	list=[]
	b=0
	for anahtar, deger in result.items():   ## id ve değeri değişkenlere atıyoruz. Tuple olarak çektiği için işlem yapılmıyor.
		print("{} = {}".format(anahtar, deger))
		list.append(deger)
		b=b+1
	b=0
	statement="INSERT INTO TRACKS (TRACKID , ALBUMID , NAME , PLAYTIME, INSTRUMENTS, GENREID, ARTISTID)  values (:2, :3, :4, :5, :6, :7, :8)"
	c = connection.cursor()
	print(type(list[0]))
	print(type(list[1]))
	print(type(list[2]))
	print(type(list[3]))
	print(type(list[4]))
	print(type(list[5]))
	print(type(list[6]))
	c.execute(statement, (int(list[0]),int(list[1]),list[2],list[3],list[4],int(list[5]),int(list[6]))) ##sorguyu oracle üzerinden gerçekleştiriyoruz.
	connection.commit()   ## sorgunun tamamlanması ve dönüş
	print(type(result))
	print("ADDED TRACK")
	
	return render_template('ADD.html',result = result)
	
	
@app.route('/addedArtist',methods=['GET','POST'])
def addedArtist():
	result = request.form
	list=[]
	b=0
	for anahtar, deger in result.items():
		print("{} = {}".format(anahtar, deger))
		list.append(deger)
		b=b+1
	b=0
	statement="INSERT INTO ARTIST (ARTISTID , NAME , YEARS , OTHERINFO)  values (:2, :3, :4, :5)"
	c = connection.cursor()
	print(type(list[0]))
	print(type(list[1]))
	print(type(list[2]))
	print(type(list[3]))
	c.execute(statement, (int(list[0]),list[1],int(list[2]),list[3]))
	connection.commit()
	print(type(result))
	
	return render_template('ADD.html',result = result)
	
@app.route('/addedAlbum',methods=['GET','POST'])
def addedAlbum():
	result = request.form
	list=[]
	b=0
	for anahtar, deger in result.items():
		print("{} = {}".format(anahtar, deger))
		list.append(deger)
		b=b+1
	b=0
	statement="INSERT INTO ALBUMS (ALBUMID , NAME , RELEASEDATE , GENREID, ARTISTID)  values (:2, :3, :4, :5, :6)"
	c = connection.cursor()
	print(type(list[0]))
	print(type(list[1]))
	print(type(list[2]))
	print(type(list[3]))
	print(type(list[4]))
	c.execute(statement, (int(list[0]),list[1],int(list[2]),int(list[3]),int(list[4])))
	connection.commit()
	print(type(result))
	
	return render_template('ADD.html',result = result)

@app.route('/addedGenre',methods=['GET','POST'])
def addedGenre():
	result = request.form
	list=[]
	b=0
	for anahtar, deger in result.items():
		print("{} = {}".format(anahtar, deger))
		list.append(deger)
		b=b+1
	b=0
	statement="INSERT INTO GENRES (GENREID , NAME)  values (:2, :3)"
	c = connection.cursor()
	print(type(list[0]))
	print(type(list[1]))
	c.execute(statement, (int(list[0]),list[1]))
	connection.commit()
	print(type(result))
	
	return render_template('ADD.html',result = result)
				
def connectionDB(p1,p2):    ## bağlantı fonskyonu. Bağlantı sağlantı gibi uyarılar veriliyor. İlk ödevde kullanıldı.
		x=0
		global connection,fourth
		try:
			connection = cx_Oracle.connect('onurhanerk/pass@127.0.0.1',threaded=True)    
		except cx_Oracle.DatabaseError as e:
			x+=1
			return render_template('connect.html',deneme=p1)

		if x==0:
			global temp
			temp+=1
			print(temp)
			print (connection)
			c = connection.cursor()
			print (c)
			if p2==fourth:
				temp=0
			return render_template('connect.html',deneme=p2)

		


@app.route('/updateRequest',methods=['GET','POST'])  #update isteği. UPDATE ekranında butona basınca sayfa içeriği değiştirilerek işlem yaptırılıyor.
def updateRequest():
		result = request.form
		print(result)
		global updateID
		for anahtar, deger in result.items():
			print("{} = {}".format(anahtar, deger))
			id=anahtar
			updateID=deger
		if id=='arArtistID':
			statement="SELECT * FROM ARTIST WHERE ARTISTID="+str(deger)
		elif id=='GGenreID':
			statement="SELECT * FROM GENRES WHERE GENREID="+str(deger)
		elif id=='alAlbumID':
			statement="SELECT * FROM ALBUMS WHERE ALBUMID="+str(deger)
		else:
			statement="SELECT * FROM TRACKS WHERE TRACKID="+str(deger)
		c = connection.cursor() 
		c.execute(statement)
		row = c.fetchone() ## tüm çıktıyı yakalaması için kullanıldı.
		print(row)
		return render_template('UPDATED.html',idnumber=id,list=row)
		
@app.route('/updateDatas',methods=['GET','POST'])
def updateDatas():
		result = request.form
		print(result)
		global updateID
		list=[]
		listKey=[]
		b=0
		for anahtar, deger in result.items():
			print("{} = {}".format(anahtar, deger))
			listKey.append(anahtar)
			list.append(deger)
			b=b+1
		b=0
		if listKey[0]=='arName':
			print(list[0])
			print(list[1])
			print(list[2])
			print(updateID)
			statement="UPDATE ARTIST SET NAME='" + str(list[0]) + "',YEARS="+ str(list[1]) + ", OTHERINFO='" + str(list[2]) +"' WHERE ARTISTID=" + str(updateID)
		elif listKey[0]=='GName':
			statement="UPDATE GENRES SET NAME='" + str(list[0]) + "' WHERE GENREID=" + str(updateID)
		elif listKey[0]=='alName':
			statement="UPDATE ALBUMS SET NAME='" + str(list[0]) + "',RELEASEDATE="+ str(list[1]) + " WHERE ALBUMID=" + str(updateID)
		elif listKey[0]=='ttrackid':
			print(list[0])
			print(list[1])
			print(list[2])
			print(list[3])
			statement="UPDATE TRACKS SET TRACKID=" + str(list[0]) + ",NAME='"+ str(list[1]) + "', PLAYTIME='" + str(list[2]) + "', INSTRUMENTS='" + str(list[3]) + "' WHERE TRACKID=" + str(updateID)
		else:
			pass
		c = connection.cursor()
		c.execute(statement)
		connection.commit()
		print(type(result))
	
		return render_template('UPDATE.html')
		
@app.route('/deleteRequest',methods=['GET','POST'])
def deleteRequest():		
		result = request.form
		print(result)
		for anahtar, deger in result.items():
			print("{} = {}".format(anahtar, deger))
			id=anahtar
			updateID=deger
			
		c = connection.cursor()
		if id=='arArtistID':
			statement1="DELETE FROM TRACKS WHERE ARTISTID="+str(deger)
			statement2="DELETE FROM ARTIST WHERE ARTISTID="+str(deger)
			c.execute(statement1)
			c.execute(statement2)
			
		elif id=='GGenreID':
			statement1="DELETE FROM ALBUMS WHERE GENREID="+str(deger)
			statement2="DELETE FROM TRACKS WHERE GENREID="+str(deger)
			statement3="DELETE FROM GENRES WHERE GENREID="+str(deger)
			c.execute(statement1)
			c.execute(statement2)
			c.execute(statement3)
			
		elif id=='alAlbumID':
			statement1="DELETE FROM TRACKS WHERE ALBUMID="+str(deger)
			statement2="DELETE FROM ALBUMS WHERE ALBUMID="+str(deger)
			c.execute(statement1)
			c.execute(statement2)
			
		else:
			statement1="DELETE FROM TRACKS WHERE TRACKID="+str(deger)
			c.execute(statement1)
		
		rowList=[]
		connection.commit()	
		c.callproc("dbms_output.enable",(None,))   ## oracle üzerinden print fonkyonu çalıştırıldı ve çıktıyı yakalayabilmek için kullanıldı.
		triggerText="DECLARE EVENTS VARCHAR2(1000); BEGIN FOR rec IN (SELECT DISTINCT A1.NAME FROM ALBUMS A1, ALBUMS A2 WHERE A1.NAME=A2.NAME AND A1.ARTISTID != A2.ARTISTID) LOOP DBMS_OUTPUT.PUT_LINE('Farklı sanatçılara ait ' || rec.NAME || ' isminde albüm saptandı!'); END LOOP; END;"
		row=c.execute(triggerText)  ## yakalanan çıktı işlem yapılmak üzere triggerText e atandı
		print(row)
		statusVar = c.var(cx_Oracle.NUMBER)
		lineVar = c.var(cx_Oracle.STRING)
		
		p=0
		while True:
			row=c.callproc("dbms_output.get_line", (lineVar, statusVar))   ## database uzerinde boş satıra gelinceye kadar yazdırılan printi oku ve bunu rowList e at.
			if statusVar.getvalue() != 0:
				break
			else:
				rowList.append(str(row[0]))
				print(rowList[p])
				p=p+1
				
		return render_template('DELETE.html',deneme=rowList)

@app.route('/searchRequest',methods=['GET','POST'])
def searchRequest():
		row1=""
		row2=""
		row3=""
		row4=""
		result = request.form
		print(result)
		for anahtar, deger in result.items():
			print("{} = {}".format(anahtar, deger))
			id=anahtar
			updateID=deger
		
		c = connection.cursor()
		if id=='ttrackid':
			statement1="SELECT * FROM TRACKS WHERE TRACKID="+str(deger)
			c.execute(statement1)
			row1 = c.fetchall()
			print(row1)
		elif id=='tAlbumID':
			statement1="SELECT * FROM TRACKS WHERE ALBUMID="+str(deger)
			c.execute(statement1)
			row1 = c.fetchall()
			print(row1)
		elif id=='tName':
			statement1="SELECT * FROM TRACKS WHERE NAME='"+str(deger)+"'"
			c.execute(statement1)
			row1 = c.fetchall()
			print(row1)
		elif id=='tGenreID':
			statement1="SELECT * FROM TRACKS WHERE GENREID='"+str(deger)+"'"
			c.execute(statement1)
			row1 = c.fetchall()
			print(row1)
		elif id=='tArtistID':
			statement1="SELECT * FROM TRACKS WHERE ARTISTID='"+str(deger)+"'"
			c.execute(statement1)
			row1 = c.fetchall()
			print(row1)
		
		
				
		elif id=='arArtistID':
			statement1="SELECT * FROM ARTIST WHERE ARTISTID="+str(deger)
			c.execute(statement1)
			row2 = c.fetchall()
			print(row2)
		elif id=='arName':
			statement1="SELECT * FROM ARTIST WHERE NAME='"+str(deger)+"'"
			c.execute(statement1)
			row2 = c.fetchall()
			print(row2)
		elif id=='arYears':
			statement1="SELECT * FROM ARTIST WHERE YEARS="+str(deger)
			c.execute(statement1)
			row2 = c.fetchall()
			print(row2)		
		
		
		
		elif id=='GGenreID':
			statement1="SELECT * FROM GENRES WHERE GENREID="+str(deger)
			c.execute(statement1)
			row3 = c.fetchall()
			print(row3)
		elif id=='GName':
			statement1="SELECT * FROM GENRES WHERE NAME='"+str(deger)+"'"
			c.execute(statement1)
			row3 = c.fetchall()
			print(row3)



		elif id=='alAlbumID':
			statement1="SELECT * FROM ALBUMS WHERE ALBUMID="+str(deger)
			c.execute(statement1)
			row4 = c.fetchall()
			print(row4)
		elif id=='alName':
			statement1="SELECT * FROM ALBUMS WHERE NAME='"+str(deger)+"'"
			c.execute(statement1)
			row4 = c.fetchall()
			print(row4)
		elif id=='alRelease':
			statement1="SELECT * FROM ALBUMS WHERE RELEASEDATE="+str(deger)
			c.execute(statement1)
			row4 = c.fetchall()
			print(row4)				
		elif id=='alGenreID':
			statement1="SELECT * FROM ALBUMS WHERE GENREID="+str(deger)
			c.execute(statement1)
			row4 = c.fetchall()
			print(row4)	
		elif id=='alArtıstID':
			statement1="SELECT * FROM ALBUMS WHERE ARTISTID="+str(deger)
			c.execute(statement1)
			row4 = c.fetchall()
			print(row4)	
		
		else:
			pass
		
		return render_template('SEARCHED.html', trackText=row1, artistText=row2, genreText=row3, albumText=row4 )  
		## serched ekranına git ve girilen parametreleri html sayfasında gerekli yerleri doldurmak için kullan.

@app.route('/UPDATE',methods=['GET','POST'])
def UPDATE():
		return render_template('UPDATE.html')
		
@app.route('/SHOW',methods=['GET','POST'])  ## show tablosunu göstermek için 
def SHOW():
		statement1="SELECT * FROM ARTIST"
		statement2="SELECT * FROM GENRES"
		statement3="SELECT * FROM ALBUMS"
		statement4="SELECT * FROM TRACKS"
		c = connection.cursor()
		c.execute(statement1)
		artist = c.fetchall()    ##tüm row
		##row = c.fetchone()    ##tek row


		c.execute(statement2)
		genres = c.fetchall()

		c.execute(statement3)
		albums = c.fetchall()

		c.execute(statement4)
		tracks = c.fetchall()
	
		return render_template('SHOW.html',artistText=artist,genreText=genres,albumText=albums,trackText=tracks)


@app.route('/similarRequest',methods=['GET','POST'])  ## aynı şarkıları puanlamak için 
def similarRequest():
		result = request.form
		print (result)
		c = connection.cursor()
		
		for anahtar, deger in result.items():
			print("{} = {}".format(anahtar, deger))
			id=anahtar
			similarID=deger
		
		c.callproc("dbms_output.enable", (None,))
		statusVar = c.var(cx_Oracle.NUMBER)        ## bu iki satır producera değer gönderebilmek için kullanıldı.
		lineVar = c.var(cx_Oracle.STRING)
		SGENREList=[] ## Similar Genre List
		SARTISTtList=[] ## Similar Artist List
		SINSTRList=[] ## Similar Instrement List
		SPTimeList=[] ## Similar PlayTime List
		
		statementTemp="SELECT TRACKID FROM TRACKS" 
		c.execute(statementTemp)
		artistIDTemp = c.fetchall()  ## TRACKS tablosundaki tüm idleri getirir.
		listPoint = []
		artistIDList=[]
		
		statementTemp="SELECT INSTRUMENTS FROM TRACKS WHERE TRACKID=" + str(similarID)  
		c.execute(statementTemp)
		ınstrTemp = c.fetchone() 
		ınstrTemp=list(ınstrTemp) ## tupple to list (INSTRUMNT getirdi)
		
		statementTemp="SELECT PLAYTIME FROM TRACKS WHERE TRACKID=" + str(similarID)  
		c.execute(statementTemp)
		timeTemp = c.fetchone() 
		timeTemp=list(timeTemp) ## tupple to list (PlayTime getirdi)
		
		
		for i in range(0,len(artistIDTemp)):   ## list  in (Tuple to list)
			artistIDTemp[i]=list(artistIDTemp[i])
			artistIDList.append(artistIDTemp[i][0])  
			listPoint.append(0)  ## point için bir list oluşturur.

		print(artistIDList)
		
		statement1="BEGIN SIMILAR_GENRE("  + str(deger) + "); END;"
		getSimList(SGENREList,lineVar,statusVar,statement1)
		
		
		if SGENREList != []:
			SGENREList[0]=int(SGENREList[0])  ## değeri int yaptı
			for i in range(0,len(SGENREList)):    ## artistIDList içerisinde SGENREList' in indislerini buluyor. Aynı tür olduğu için 1 ekliyor ve point listesine yazıyor.
				indis=artistIDList.index(int(SGENREList[i]))
				listPoint[indis]=listPoint[indis]+1	
			print(listPoint)	
		
		
		
		statement2="BEGIN SIMILAR_ARTIST("  + str(deger) + "); END;"
		getSimList(SARTISTtList,lineVar,statusVar,statement2)
		print("******")
		print(SARTISTtList)
		
		if SARTISTtList!=[]:  ## eğer null değil ise
			SARTISTtList[0]=int(SARTISTtList[0])  ## değeri int yaptı
			for i in range(0,len(SARTISTtList)):    ## artistIDList içerisinde SARTISTtList' in indislerini buluyor. Aynı artist olduğu için 1 ekliyor ve point listesine yazıyor.
				indis=artistIDList.index(int(SARTISTtList[i]))
				listPoint[indis]=listPoint[indis]+1

			print(listPoint)
		
		
		
	
		
		statement3="BEGIN SIMILAR_INSTR("  + str(deger) + "); END;"
		getSimList(SINSTRList,lineVar,statusVar,statement3)
		ınstrTempSTR=ınstrTemp[0] ##list to string
		print("*******")
		ınstrTempSTR=ınstrTempSTR.split(", ")  ## search için liste yaptı
		print(ınstrTempSTR)
		
		
		if ınstrTempSTR!=[]:  ##eğer null değil ise
			i=0
			while True:
				numberOfEleman=len(SINSTRList)		
				SINSTRListSTR=SINSTRList[i+1]
				SINSTRListSTR=SINSTRListSTR.split(", ")
				for j in ınstrTempSTR:
					for k in SINSTRListSTR:
						if j==k:  ## entrumanlar eşitse 1 arttırıcak
							indis=artistIDList.index(int(SINSTRList[i]))
							listPoint[indis]=listPoint[indis]+1
				i=i+2
				if i==numberOfEleman:
					break
			print(listPoint)
		
		
		
		statement4="BEGIN SIMILAR_PLAYTIME("  + str(deger) + "); END;"
		getSimList(SPTimeList,lineVar,statusVar,statement4)
		
		timeTempSTR=timeTemp[0] ##list to string
		timeTempSTR=timeTempSTR.split(":")
		totalTime= int(timeTempSTR[0])*60 + int(timeTempSTR[1])
		print( totalTime)
		
		
		i=0
		while True:
			numberOfEleman=len(SPTimeList)		
			SPTimeSTR=SPTimeList[i+1]
			SPTimeSTR=SPTimeSTR.split(":")
			similarTime=int(SPTimeSTR[0])*60 + int(SPTimeSTR[1])
			if abs(totalTime - similarTime) <= 10:    ## şarkılar arasındaki fark 0-10 sn arasında ise (abs = mutlak)
					indis=artistIDList.index(int(SINSTRList[i]))
					listPoint[indis]=listPoint[indis]+5
			elif abs(totalTime - similarTime) >=11 and abs(totalTime - similarTime) <=65:
					indis=artistIDList.index(int(SINSTRList[i]))
					listPoint[indis]=listPoint[indis]+3
			else:
					indis=artistIDList.index(int(SINSTRList[i]))
					listPoint[indis]=listPoint[indis]+1		
			
			i=i+2
			if i==numberOfEleman:
				break
		print(listPoint)
		
		
		show="SELECT * FROM TRACKS ORDER BY TRACKID ASC"
		c.execute(show)
		similarSongPoint = c.fetchall() 
		tempSongPoint=[]
		appendedList=[]
		
		for i in range(0, len(similarSongPoint)):  
			print(list(similarSongPoint[i]))
			appendedList=list(similarSongPoint[i])
			appendedList.append(listPoint[i])
			tempSongPoint.append(appendedList)
		
		print(tempSongPoint)
		return render_template('similarSongs.html', similarT=tempSongPoint, point=listPoint)	
		
def getSimList(rowList,lineVar,statusVar,statement):   ##print Similar Lists  
		p=0
		c = connection.cursor()
		c.execute(statement)
		while True:
			c.callproc("dbms_output.get_line", (lineVar,statusVar))
			if not lineVar.getvalue():
				break
			else:
				rowList.append(lineVar.getvalue())
				p=p+1
		connection.commit()
		print (rowList)
		return rowList
		
@app.route('/ADD',methods=['GET','POST'])    ## buton sayfaları. Butonlar ile otomatik olarak yönlendirmeyi sağlamak için kullanıldı.
def ADD():
		return render_template('ADD.html')

@app.route('/SIMILAR',methods=['GET','POST'])
def SIMILAR():
		return render_template('SIMILAR.html')		
@app.route('/SEARCH',methods=['GET','POST'])
def SEARCH():
		return render_template('SEARCH.html')
@app.route('/DELETE',methods=['GET','POST'])
def DELETE():
		return render_template('DELETE.html')		
@app.route('/UDAS',methods=['GET','POST'])
def udas():
		return render_template('UDAS.html')
		
@app.route('/searchArtist',methods=['GET','POST'])
def searchArtist():
		return render_template('searchArtist.html')
@app.route('/searchGenre',methods=['GET','POST'])
def searchGenre():
		return render_template('searchGenre.html')
@app.route('/searchAlbum',methods=['GET','POST'])
def searchAlbum():
		return render_template('searchAlbum.html')
@app.route('/searchTrack',methods=['GET','POST'])
def searchTrack():
		return render_template('searchTrack.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('Error.html'), 404  

@app.errorhandler(500)
def page_not_found(e):
    return render_template('Error.html'), 500
	
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000)) ## port adresi ataması
    app.run(host='0.0.0.0', port=port)	
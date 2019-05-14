# MusicInfo-Database

I wrote this project using Flask on Python, HTML and ORACLE also this project includes CSS and JS<br />
To run the program, edit line 182 in server.py<br /><br />


```Run server.py and then enter http: // localhost: 5000 /```

1) Separate screens are designed for updating, deleting, adding and searching.
2) When a user selects the group on a separate screen, the group's member information is automatically brought to the group's albums.
3) It gives warning when different artists have songs with the same name. This was done using Trigger.
4) A screen listing similar songs should be designed. Songs similar to the song selected by the user are shown in sequence on the screen by calculating a score. Points are calculated as follows.
   - If the song is of the same style, 1 point, if not 0 points
   - If the song is told by the same vocalist 1 point, if not 0 points
   - If the difference between the duration of the songs is between 0-10 sec, it is 5 points, between 11-65 sec.
   - The number of the same instruments used in the two songs is added to the total likelihood score.

![alt text](https://i.ibb.co/ZBLDStd/1.png)
![alt text](https://i.ibb.co/Mcv8dpS/2.png)
![alt text](https://i.ibb.co/Cz6h2sj/3.png)
![alt text](https://i.ibb.co/xH8tsLk/4.png)
![alt text](https://i.ibb.co/qDxw0xT/5.png)

# Data-Stream
An example for data stream saving and retrieval (fake-y database)<br>
<br>
Example usage<br>
$ ./query -s TITLE,REV,DATE -o DATE,TITLE<br>
<br>
the matrix,4.00,2014-04-01<br>
the hobbit,8.00,2014-04-02<br>
the matrix,4.00,2014-04-02<br>
unbreakable,6.00,2014-04-03<br>
<br>
$ ./query -s TITLE,REV,DATE -f DATE=2014-04-01<br>
<br>
the matrix,4.00,2014-04-01<br>
<br>
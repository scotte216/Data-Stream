# Data-Stream
An example for data stream saving and retrieval (fake-y database)

Example usage
$ ./query -s TITLE,REV,DATE -o DATE,TITLE

the matrix,4.00,2014-04-01
the hobbit,8.00,2014-04-02
the matrix,4.00,2014-04-02
unbreakable,6.00,2014-04-03

$ ./query -s TITLE,REV,DATE -f DATE=2014-04-01

the matrix,4.00,2014-04-01
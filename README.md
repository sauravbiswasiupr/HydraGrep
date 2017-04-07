Introduction
============

Welcome to HydraParser. HydraParser is a grep like utility that lets you search for patterns 
in single files or directories containing files. It is by no means a distributed log search engine
(atleast as of now). It uses a threaded approach if requested whereby it can speed up the search time.


Caveats
-------

One important point to remember is that these searches (using Threads) is not parallel but concurrent. The
GIL or the Global Interpreter Lock in standard cPython doesn't let more than one thread get a hold of the 
interpreter at an instant. Concurrency is achieved by the GIL performing context switches whenever it gets
a free thread.

HydraParser doesn't do a lot of CPU intensive tasks, being mostly involved in I/O which results in the CPU
being idle most of the time, mostly waiting for the I/O to complete. Consequently, thread switching makes
more sense in the case of HydraParser's operation.

Inspiration
-----------

The name HydraParser is inspired by the Greek Mythological beast called Hydra which was a serpentine monster
with many heads. The heads are analogous to the many threads it uses to run the scans.

TODO:
-----

Implement multiprocessing based approach when CPU intensive operations are involved.
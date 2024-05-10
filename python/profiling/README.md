# Profiling in Python

A collection of examples for time and memory profiling options for python.

## Dependencies

We'll examine 3 options for profiling:

1. The `cProfile` module (builtin in most python distributions).
2. The [`kernprof`](https://kernprof.readthedocs.io/en/stable/_modules/kernprof.html) module (can be found in the `line_profiler` package).
3. The [`memory_profiler`]('https://github.com/pythonprofilers/memory_profiler') module.

The recommended way is to setup a virtual environment and install the dependencies there. E.g. in linux:

> $ python -m venv profiler-env
> $ source profiler-env/bin/activate
> $ pip install --upgrade pip && pip install -r requirements.txt

## Time profiling

We'll examine time profiling through two example scripts: `slow.py` and `linalg.py`. Both can be found under the 'time' directory. Feel free to execute the scripts to see their output and execution times. 
We will try to use several profiling methods to examine bottlenecks in these scripts and see how we can make them faster.

*Note: The examples below assume we are working from inside the `profiling/time/` directory*

### Slow

This example utilizes an artificial way of slowing down the script (i.e. through `time.sleep`). If we run the script we can get the feeling that `func3` is slower than `func2` which is slower than `func1`. We'll try to quantify this through a profiler. 

The lowest level of profiling we can accomplish is through the built-in cProfile module. Usually we run this as follows:

![]()

In our example this would look like:

![]()

The output lists all function calls (both user-defined and built-in) with all their execution time stats (total time, cumulative time, etc.). E.g. we can tell how in terms of execution time `func3` > `func2` > `func1`. Through this we can in theory identify possible bottlenecks in our program.

![]()

The issue with `cProfile` is that in real world programs it can be very noisy with low-level information (we'll see this in the next example). A more convenient way to profile our code is through **line profilers**. These list line-by-line the execution stats of our program. The catch is that we'll need to specify exactly what we want the profiler to track. We'll use `kernprof` which requires us to decorate any function we want to track with the `@profile` decorator. In `slow_kern.py` we have made these changes to the script, in order to track all 3 user-defined functions.

To run kernprof:

![]()

The output of kernprof:

### Linalg

Let's apply the methods we learned in another example, `linalg.py`. This example simulates a script that performs several linear algebra computations, some of which are fairly slow, especially for larger matrices (e.g. matrix exponential, inverse, etc.). In brief, we create two matrices, A and B, we make them sparse by randomly making 95% of their elements 0, then we do several linear algebra steps and finally we compute stats on the output matrix.

Our goal here is to try to see if there is a performance bottleneck and to try and make it faster! 

We'll try using the `cProfile` module first:

```
python -m cProfile -s tottime linalg.py
```

The result might not be what we expected. It isn't the linear algebra operations, or the computation of the statistics that takes up the most time, but the user defined, `make_sparse` function!

![]()

Also it's worth to note how noisy this output can be, it's so granular that even in this simple example it takes up ~1400 lines!

Let's try to use `kernprof` to see what actually takes up the most time. Since we know that `make_sparse` takes up the most time, we'll focus on this function and see how we can improve it. 'linalg\_kern.py` is a script that has added a `@profile` decorator to the `make_sparse` function.


```
kernprof -v -l linalg_kern.py
```

From the output we can see that the poor implementation of the function is what is the problem. Notice how most of the time is taken up inside the double for loop and more specifically in the membership condition inside the innermost loop. Needless to say that this a very inefficient implementation.

With a better implementation that doesn't rely on for loops, we can achieve a much better performance. Feel free to play around with `linalg_solution.py` to see for yourselves.

## Memory Profiling

Another topic that we'll discuss is memory profiling. Sometimes the performance of a script isn't hindered by computational time, but memory constraints. To investigate this we need a different kind of profiling. The example we have for this can be found under the `memory` directory. 

`mem.py` is a script that starts off by creating 100 lists, then deletes 50 of them and finally creates 100 more. Our goal here is two-fold: first we want to see how memory consumption progresses as the script runs and secondly we want to see, again, which part of the code is responsible for allocating this memory.

Let's start off with the first. Given how we wrote the script, we might expect the memory consumption to progress like this:

![]()

To check if in reality it is as we expect we'll use the 'memory_profiler' package mentioned above.

```
mprof run mem.py
```

This doesn't output any report immediately, but we can generate a graph of how memory consumption progresses.

```
mprof plot
```

This will pop up a window with the following figure:

![]()

Turns out it wasn't as we expected. The python garbage collector took its time to deallocate the memory, while the second iteration for list creation wasn't as memory consuming as the first! This functionality is also helpful to detect possible memory leaks, i.e. cases where some function is continuously taking more and more memory as execution progresses. 

If we want to detect where the leak is, we'll need a line profiler! The 'memory_profiler' package also includes this functionality, as long as we add the `@profile` decorator.

```
python -m memory_profiler mem_kern.py
```

We need to be a bit careful, though, of where we place our `@profile` decorator! In this case, because the function is an internal one, we won't get any information from it!

![]()

To solve this, we need to refactor the code a bit and place the decorator, where it's a bit more relevant. Let's re-run.


```
python -m memory_profiler mem_kern_refactored.py
```

Which will output:

![]()


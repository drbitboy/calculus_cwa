## Estimate the derivative of a ratio of two functions from plot images

* R(x) = g(x) / f(x)
```
   % python cwa.py images/g.png 40 images/f.png 40 .5

   (1.3853286136321994, 1.6099748142017734, -0.6136960634421801, 0.3441565875070963)
   R'(0.5) = -3.889315642265257
   R'(0.5,dx=1/1) = -4.15753777420767
   R'(0.5,dx=1/4) = -3.902159936627285
   R'(0.5,dx=1/16) = -3.8901055943399214
   R'(0.5,dx=1/64) = -3.889364964709472
   R'(0.5,dx=1/256) = -3.8893187247244896
   R'(0.5,dx=1/1024) = -3.889315834917852
```


* R(x) = f(x) / g(x)
```
   % python cwa.py images/f.png 40 images/g.png 40 -1

   (-1.235988024447348, 0.43862948933049384, -1.3853014087576057, 1.4842948180306388)
   R'(-1.0) = 0.6393424774372419
   R'(-1.0,dx=1/1) = 1.2316995523520744
   R'(-1.0,dx=1/4) = 0.6612240423647728
   R'(-1.0,dx=1/16) = 0.6406763348885942
   R'(-1.0,dx=1/64) = 0.6394257152564364
   R'(-1.0,dx=1/256) = 0.6393476793007267
   R'(-1.0,dx=1/1024) = 0.6393428025520507
```

### Data fit results:

![](https://github.com/drbitboy/calculus_cwa/blob/master/images/g.png?raw=true)
→![](https://github.com/drbitboy/calculus_cwa/blob/master/images/g_fit.png?raw=true)

![](https://github.com/drbitboy/calculus_cwa/blob/master/images/f.png?raw=true)
→![](https://github.com/drbitboy/calculus_cwa/blob/master/images/f_fit.png?raw=true)

![](https://github.com/drbitboy/calculus_cwa/blob/master/images/f_over_g.png?raw=true)

![](https://github.com/drbitboy/calculus_cwa/blob/master/images/f_over_g_inset.png?raw=true)

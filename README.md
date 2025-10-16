## Estimate the derivative of a ratio of two functions from plot images

* R(x) = g(x) / f(x)
```
   % python cwa.py images/g.png 40 images/f.png 40 .5

   (1.3853286136321994, 1.6099748142017734, -0.6136960634421801, 0.3441565875070963)
   R'(0.5) = -3.889315642265257
```


* R(x) = f(x) / g(x)
```
   % python cwa.py images/f.png 40 images/g.png 40 -1

   (-1.235988024447348, 0.43862948933049384, -1.3853014087576057, 1.4842948180306388)
   R'(-1.0) = 0.639342477437241
```

### Data fit results:

![](https://github.com/drbitboy/calculus_cwa/blob/master/images/g.png?raw=true)
→![](https://github.com/drbitboy/calculus_cwa/blob/master/images/g_fit.png?raw=true)

![](https://github.com/drbitboy/calculus_cwa/blob/master/images/f.png?raw=true)
→![](https://github.com/drbitboy/calculus_cwa/blob/master/images/f_fit.png?raw=true)

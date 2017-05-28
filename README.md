# python-game-of-life
Conway's Game of Life written with python and SDL2 

## perview
<img src="http://i.imgur.com/p9Rs1H2.gif">

## requirements
- SDL 2.0
- pysdl2

[SDL installation](https://wiki.libsdl.org/Installation)

[Useful guide on ubuntu forums](https://askubuntu.com/a/344528)

pysdl2 installation:

``` sudo pip install pysdl2 ```

## usage
```
./life.py 64 48
```

## controls
```
WASD        - move map                                                             
mouse drag  - move map                                                             
mouse click - toggle cell                                                          
+ or "-"    - change zoom level                                                    
mouse wheel - change zoom level                                                   
r           - clear map                                                            
c           - fill map with random                                                 
n           - toggle grid                                                         
f           - toggle fingerprint display                                           
p           - toggle evolution                                                     
Enter       - toggle evolution                                                     
> / <       - change speed
```
## interesting patterns

![exploders](http://imgur.com/zIQ8bJCl.png)

![more patterns](http://imgur.com/Ga8rC1El.png)

[more info on wiki](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life)

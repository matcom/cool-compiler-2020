class Silly 
{
    a : Silly;
    copy() : Silly {
        a
    };
};
    
class Sally inherits Silly { 

};

class Main {
    x:Sally<-(new Sally).copy();
    main() : Sally { x };
};
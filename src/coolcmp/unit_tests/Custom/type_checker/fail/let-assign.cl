class Main inherits IO {
    main(): Int {
        {
            let x: String <- (let y: Int <- 5 in y + 2) in 1;
        }
    };
};
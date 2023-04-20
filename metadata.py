menu_options = {1 : 'configure line-space',
                2 : 'configure book',
                3 : 'navigate to new line',
                4 : 'alter what books / line-spaces display'}



line_space_config_options = {1 : 'remove a line-space from the appearing line-spaces',
                             2 : 'add a line-space to the appearing line-spaces'}



chess_data = ['''[Event "Live Chess"]
    [Site "Chess.com"]
    [Date "2022.11.06"]
    [Round "?"]
    [White "209joey"]
    [Black "TheRealYzb25"]
    [Result "0-1"]
    [ECO "A00"]
    [WhiteElo "533"]
    [BlackElo "706"]
    [TimeControl "600"]
    [EndTime "11:53:54 PST"]
    [Termination "TheRealYzb25 won by checkmate"]

    1. g4 e5 2. Bg2 Bb4 3. Nc3 Nf6 4. a3 Ba5 5. g5 Ng4 6. f3 Qxg5 7. fxg4 Qxg4 8. h3
    Qxg2 9. Rh2 Qxg1# 0-1''',
    
    '''[Event "Live Chess"]
    [Site "Chess.com"]
    [Date "2023.03.22"]
    [Round "?"]
    [White "TheRealYzb25"]
    [Black "ihategambinos"]
    [Result "0-1"]
    [ECO "A40"]
    [WhiteElo "1005"]
    [BlackElo "1042"]
    [TimeControl "600"]
    [EndTime "11:52:21 PDT"]
    [Termination "ihategambinos won by resignation"]

    1. d4 e5 2. dxe5 Nc6 3. Nf3 Qe7 4. Bf4 Qb4+ 5. Qd2 Qxb2 6. Qc3 Bb4 0-1''',
    
    '''[Event "Live Chess"]
    [Site "Chess.com"]
    [Date "2023.04.03"]
    [Round "?"]
    [White "GigaChadVlad"]
    [Black "TheRealYzb25"]
    [Result "0-1"]
    [ECO "E00"]
    [WhiteElo "960"]
    [BlackElo "987"]
    [TimeControl "600"]
    [EndTime "6:35:03 PDT"]
    [Termination "TheRealYzb25 won by resignation"]

    1. d4 d5 2. c4 e6 3. a3 Nf6 4. Nc3 Bd6 5. f3 O-O 6. e4 dxe4 7. fxe4 Be7 8. e5
    Nfd7 9. Nf3 b6 10. Bd3 c5 11. O-O cxd4 12. Nxd4 Bb7 13. Bf4 Nc6 14. Re1 Nxd4 0-1''',
    
    '''[Event "Live Chess"]
    [Site "Chess.com"]
    [Date "2023.03.22"]
    [Round "?"]
    [White "ButMob21"]
    [Black "TheRealYzb25"]
    [Result "1-0"]
    [ECO "C24"]
    [WhiteElo "1061"]
    [BlackElo "1014"]
    [TimeControl "600"]
    [EndTime "8:24:58 PDT"]
    [Termination "ButMob21 won by checkmate"]

    1. e4 e5 2. Bc4 Nf6 3. d4 Nxe4 4. dxe5 Bc5 5. Bxf7+ Kf8 6. Qf3 Nxf2 7. Be6+ Ke7
    8. Qf7# 1-0''',
    
    '''[Event "Live Chess"]
    [Site "Chess.com"]
    [Date "2023.03.22"]
    [Round "?"]
    [White "KindredLocks"]
    [Black "TheRealYzb25"]
    [Result "0-1"]
    [ECO "C45"]
    [WhiteElo "1001"]
    [BlackElo "1013"]
    [TimeControl "600"]
    [EndTime "11:48:56 PDT"]
    [Termination "TheRealYzb25 won by checkmate"]

    1. e4 e5 2. Nf3 Nc6 3. d4 exd4 4. Nxd4 Bc5 5. Nxc6 Qf6 6. Qd2 dxc6 7. Nc3 Bb4 8.
    a3 Ba5 9. b4 Bb6 10. Bc4 Bd4 11. Bb2 Ne7 12. O-O O-O 13. Rad1 Be5 14. Qd8 Bh3
    15. Qd3 Bg4 16. f3 Qh4 17. fxg4 Bxh2+ 18. Kh1 Bg3+ 19. Kg1 Qh2# 0-1''',
    
    '''[Event "Live Chess"]
    [Site "Chess.com"]
    [Date "2023.03.22"]
    [Round "?"]
    [White "010121abc"]
    [Black "TheRealYzb25"]
    [Result "0-1"]
    [ECO "C20"]
    [WhiteElo "951"]
    [BlackElo "1013"]
    [TimeControl "600"]
    [EndTime "7:32:57 PDT"]
    [Termination "TheRealYzb25 won by checkmate"]

    1. e4 e5 2. d3 Nf6 3. Be3 Bb4+ 4. c3 Ba5 5. b4 Bb6 6. Nf3 O-O 7. Nbd2 Nc6 8. Bg5
    d6 9. Be2 Bd7 10. Nh4 h6 11. Bxf6 Qxf6 12. g3 g5 13. Nf5 Bxf5 14. exf5 Qxf5 15.
    g4 Qxf2# 0-1''',
    
    '''[Event "Live Chess"]
    [Site "Chess.com"]
    [Date "2023.03.22"]
    [Round "?"]
    [White "CelestialCenturion"]
    [Black "TheRealYzb25"]
    [Result "1-0"]
    [ECO "C62"]
    [WhiteElo "998"]
    [BlackElo "1005"]
    [TimeControl "600"]
    [EndTime "11:34:17 PDT"]
    [Termination "CelestialCenturion won by resignation"]

    1. e4 e5 2. Nf3 Nc6 3. Bb5 d6 4. Bxc6+ bxc6 5. Nc3 Nf6 6. d4 exd4 7. Nxd4 c5 8.
    Nf3 Bb7 9. Qe2 Be7 10. O-O O-O 11. h3 Rb8 12. e5 Nd7 13. e6 Nf6 14. Ng5 fxe6 15.
    Nxe6 1-0''',
    
    '''[Event "Live Chess"]
    [Site "Chess.com"]
    [Date "2023.03.21"]
    [Round "?"]
    [White "TheRealYzb25"]
    [Black "Colmena1"]
    [Result "1-0"]
    [ECO "D20"]
    [WhiteElo "1025"]
    [BlackElo "967"]
    [TimeControl "600"]
    [EndTime "10:14:25 PDT"]
    [Termination "TheRealYzb25 won by checkmate"]

    1. d4 d5 2. c4 dxc4 3. e3 e6 4. Nc3 a6 5. Qa4+ c6 6. Qxc4 Nd7 7. Qb3 Ngf6 8. Nf3
    h6 9. Bd3 Bd6 10. O-O g5 11. Nd2 h5 12. e4 g4 13. e5 Nxe5 14. dxe5 Bxe5 15. Qc2
    h4 16. Nde4 Nxe4 17. Bxe4 h3 18. g3 Qd4 19. Be3 Qd7 20. Rad1 Qe7 21. Bd4 Bxd4
    22. Rxd4 Qf6 23. Rfd1 e5 24. Rd6 Qg5 25. Qd2 Qg7 26. Rd8+ Ke7 27. Qd6# 1-0''']
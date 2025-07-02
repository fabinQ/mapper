def main():
    C1L = [(81253,81996),(82116,82125),(83500,83800),(84200,84350),(85150,85340),(86180,86280)]
    C1P = [(81870,82120),(82707,83015),(86110,86300)]
    C2L = [(86410,86650),(86700,87030),(87070,87650),(88090,88203)]
    C2P = [(86300,86650),(86700,87030),(87070,87200)]
    C3L = [(88584,89995),(90050,90310),(90985,91146),(91517,91963),(92063,92113),(92303,92359),(92550,92620),(93415,93472),(93640,93670),(94412,94615),(95370,95855),(96150,96580),(96590,96900)]
    C3P = [(88580,88892),(90193,90310),(91083,91150),(91626,91772),(92050,92280),(93450,93472),(93640,93670),(94065,94115),(94410,94645),(95345,95371),(95443,95505),(95550,95855),(95945,96250),(96485,96560),(96590,96870)]
    C4L = [(96900,96952),(97495,97800),(99000,99050),(99215,99300)]
    C4P = [(97517,97788),(99100,99300)]
    C5L = [(99300,99325),(100150,100215),(100325,100452),(100690,100823),(100856,100975),(101250,101436),(101475,102236),(102750,103275),(103550,103855),(103865,104700),(105200,105540),(107250,107600),(108170,108300),(108520,109400),(109600,109700),(109990,110200),(110325,110425),(110600,110725),(111040,111300)]
    C5P = [(99300,99399),(100150,100208),(100320,100460),(100620,100820),(100855,101055),(101500,102235),(102750,103325),(103572,103855),(103865,104225),(105200,105540),(107310,107430),(107975,108025),(108110,108170),(108470,109400),(109600,110280),(110430,110530),(110600,110725),(111085,111100)]
    C6L = [(111300,111550),(113490,113550)]
    C6P = [(111550,111850),(113500,113550)]
    trenchRange = [C1L,C1P,C2L,C2P,C3L,C3P,C4L,C4P,C5L,C5P,C6L,C6P]

    ZC1L = [(81325,81472),(81625,81996),(83500,83798),(84200,84350),(85150,85340),(86180,86279)]
    ZC1P = [(81870,82116),(82707,83015),(86101,86300)]
    ZC2L = [(87015,87030),(88090,88191)]
    ZC2P = [(86300,86418),(86413,86418)]
    ZC3L = [(88583,88985)]
    ZC3P = [(88580,88892),(90193,90310),(91083,91150),(91626,91772),(92050,92280),(93450,93472),(93640,93670),(94065,94115),(94410,94645),(95345,95371),(95443,95505),(95550,95855),(95945,96250),(96485,96560),(96590,96870)]
    whatWasDone = [ZC1L,ZC1P,ZC2L,ZC2P,ZC3L,ZC3P]

    def generate_set_from_intervals(intervals):
        """
        Generuje zbiór liczb na podstawie listy przedziałów.
        Każdy przedział to krotka (start, end), która reprezentuje liczby od start do end włącznie.
        """
        result_set = set()
        for start, end in intervals:
            result_set.update(range(start, end + 1))
        return result_set

    def calculate_set_difference(set_A_intervals, set_B_intervals):
        """
        Oblicza różnicę zbiorów A - B, gdzie każdy zbiór jest zdefiniowany przez listę przedziałów.
        """
        set_A = generate_set_from_intervals(set_A_intervals)
        set_B = generate_set_from_intervals(set_B_intervals)
        
        difference = set_A - set_B
        return difference

    def print_result_ranges(difference_set):
        """
        Formatuje wynik jako listę przedziałów liczbowych dla bardziej zwięzłej prezentacji.
        """
        if not difference_set:
            return []
        
        sorted_numbers = sorted(difference_set)
        ranges = []
        start = sorted_numbers[0]
        end = start
        
        for num in sorted_numbers[1:]:
            if num == end + 1:
                end = num
            else:
                ranges.append((start, end))
                start = num
                end = num
        
        ranges.append((start, end))
        return ranges

    # Dane wejściowe
    A = [(81253,81996), (82116,82125), (83500,83800), (84200,84350), (85150,85340), (86180,86280)]
    B = [(81325,81472), (81625,81996), (83500,83798), (84200,84350), (85150,85340), (86180,86279)]

    # Obliczenie różnicy A - B
    difference = calculate_set_difference(A, B)

    # Wyświetlenie wyników
    print(f"Liczba elementów w zbiorze A - B: {len(difference)}")
    print("Elementy zbioru A - B jako przedziały:")
    result_ranges = print_result_ranges(difference)
    for start, end in result_ranges:
        if start == end:
            print(f"  {start}")
        else:
            print(f"  ({start},{end})")

    # Opcjonalnie, można również wypisać wszystkie elementy różnicy
    print("\nElementy różnicy A - B:")
    print(sorted(difference))
    
if __name__ == "__main__":
    main()
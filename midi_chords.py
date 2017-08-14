   '''
    switcher = {

        Tonic_Scale: Major_Chord,
        Fourth: Major_Chord,
        Fifth: Major_Chord,
        Second: Minor_Chord,
        Third_major: Minor_Chord,
        Sixth_major: Minor_Chord,
        Seventh_major: Dim_Chord,
        Tonic_octaveUP: Sus4_Chord,
        Fifth_octaveUP: Sus4_Chord,
        Fourth_octaveUP: Minor_6th,
        Second_octaveUP: Major_Dominant_7th_Chord,
        Third_major_octaveUP: Major_Dominant_7th_Chord,
        Sixth_major_octaveUP: Major_Dominant_7th_Chord,
        Seventh_major_octaveUP: Major_Dominant_7th_Chord,
    }
    '''

    switcher = {

        Tonic_Scale or Fourth or Fifth: Major_Chord,
        Second: Minor_Chord,
        Third_major: Minor_Chord,
        Sixth_major: Minor_Chord,
        Seventh_major: Dim_Chord,
        Tonic_octaveUP: Sus4_Chord,
        Fifth_octaveUP: Sus4_Chord,
        Fourth_octaveUP: Minor_6th,
        Second_octaveUP: Major_Dominant_7th_Chord,
        Third_major_octaveUP: Major_Dominant_7th_Chord,
        Sixth_major_octaveUP: Major_Dominant_7th_Chord,
        Seventh_major_octaveUP: Major_Dominant_7th_Chord,
    }

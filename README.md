# Regex->DFA
Implementarea un program care primește o expresie regulată și construiește un automat finit determinist (DFA) echivalent. Implementarea este bazata pe urmatorii pasi:
1. Scrieți un convertor de expresii regulate în notație postfixată.
2. Implementați construcția NFA folosind postfixul și algoritmul lui Thompson.
3. Implementați conversia NFA → DFA prin subset construction.
4. Implementați un simulant de DFA (verifică dacă un cuvânt este acceptat de DFA).

Codul se ruleaza folosind comanda, dar trebuie sa avem grija ca fisierul json sa fie in acelasi director ca fisierul regtoDfa.py

    python3 .\regtoDfa.py
    
Codul va returna Corect daca Dfa-ul rezultat din conversia expresiei are aceleasi expectev value pentru cuvintele pe care le testeaza testele din json 

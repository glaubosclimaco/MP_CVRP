


for K in 3 5
do
    for P in 2 3
    do
        for percentualCAP in 0.7 0.9
        do
            for percentualAtendimentoMin in 0.7 0.9
            do
                echo "K = $K, P = $P, percentualCAP = $percentualCAP, percentualAtendimentoMin = $percentualAtendimentoMin"
                python3 vrp.py norte.csv $K $P $percentualCAP $percentualAtendimentoMin > results/norte-$K-$P-$percentualCAP-$percentualAtendimentoMin.txt
            done
        done
    done

done
for i in {10..1000..50}
do
    python3 main.py load ../vendors/gr24.tsp genetic 500,0.2,0.7,$i,100,35
done
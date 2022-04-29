for file in "/home/radikey/studia/Metaheurystyczne/vendors"/*; do
  echo "$file"
  python3 main.py load $file tabu 1000,10,20,1
done
for count in $(seq 0 9); do mkdir RUN_"$count"; done
for count in $(seq 0 9); do mv *_run_"$count"* RUN_"$count"; done
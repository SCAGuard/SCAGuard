file="./src0.c.out"

perf record -c 1 -e intel_pt//u --filter "filter * @./$file"   -e branch-misses -e cache-misses   -e L1-dcache-load-misses   -e L1-dcache-loads    -e L1-dcache-stores    -e L1-icache-load-misses -e LLC-load-misses -e LLC-loads -e LLC-store-misses -e  LLC-stores -e branch-load-misses     -- ./$file

perf script --itrace=oe >./$file.txt
rm -rf ./perf.data
rm -rf ./perf.data.old

